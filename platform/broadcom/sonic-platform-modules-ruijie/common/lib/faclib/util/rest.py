#!/usr/bin/python3
# -*- coding: utf-8 -*-
import redis
import json
import ssl
import requests
import time
import os
import re
import collections
import pickle
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {'Content-type': 'application/json'}
context = ssl._create_unverified_context()
__DEBUG__ = "N"
LOGIN_TRY_TIME = 3


def d_print(debug_info):
    if(__DEBUG__ == "Y"):
        print(debug_info)


class HttpRest:
    RESTRETURNKEY = "status"
    RESTRETURNSUCCESSKEY = "ok"
    _session = None

    def __init__(self):
        pass

    def unicode_convert(self, input):
        if isinstance(input, dict):
            return {self.unicode_convert(key): self.unicode_convert(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.unicode_convert(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def isReturnSuccess(self, val):
        if self.RESTRETURNKEY in json.loads(val) and json.loads(val)[self.RESTRETURNKEY] == self.RESTRETURNSUCCESSKEY:
            return True
        else:
            return False

    def __init__(self):
        d_print("bmcmessage init...")
        self.session = requests.session()
        self.session.keep_alive = False

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, val):
        self._session = val

    @property
    def session(self):
        return self._session

    def uploadfile(self, url, filename, timeout=90):
        d_print(url)
        try:
            for i in range(3):
                files = {'file': open(filename, 'rb')}
                response = self.session.post(url, files=files, timeout=timeout)
                val_t = ""
                print(response.text)
                if isinstance(response.text, unicode):
                    val_t = response.text.encode("UTF-8").replace("'", '"')
                if self.isReturnSuccess(val_t):
                    return self.unicode_convert(json.loads(val_t)['data'])
                else:
                    d_print("error return")
                    return None
                return None
        except Exception as e:
            print("error", str(e))
            return None

    def Get(self, url, timeout=80):
        """
        self.Get(url,data）
        :param url:
        :param data:
        :return:
        """
        d_print(url)
        try:
            for i in range(3):
                response = self.session.get(url, verify=False, timeout=timeout)
                val_t = ""
                if isinstance(response.text, unicode):
                    val_t = response.text.encode("UTF-8")
                if self.isReturnSuccess(val_t):
                    return self.unicode_convert(json.loads(val_t)['data'])
                else:
                    d_print("error return")
                    return None
                return None
        except Exception as e:
            print("error", str(e))
            return None
