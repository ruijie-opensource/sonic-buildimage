#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import sys
import json
import cgi
from time import sleep
import hashlib
import os
from factest_bmc import *
if sys.version_info >= (3, 0):
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from http.server import *
from socketserver import ThreadingMixIn
import urllib.parse


class Restful(BaseHTTPRequestHandler):  # 所有rest的父类
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.dp = None
        self.router = None

    def basepath(self):
        pass

    def getresetlet(self):
        pass

    def send(self, src):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        src = bytes(src, encoding='UTF-8')
        self.wfile.write(src)
        self.wfile.write(b"\n")
        #self.wfile.close()

    def done(self):
        self.dp = self.basepath()
        self.router = self.getrestlet()



class Factest(Restful):
    def deal(self, cases, params):
        func = eval(cases) #cases1.get(cases)
        if params is None:
            RET = func()
        else:
            RET = func(params)
        return {"status": "ok", "data": RET}

    def getmsg(self, val):
        msg = ""
        cases = val.get('case', None)
        params = val.get('param', None)
        if cases == None:
            msg = "no such case"
            ret = {"status": "null", "data": msg}
            return json.dumps(ret)
        ret = self.deal(cases, params)
        return json.dumps(ret, ensure_ascii = False)

    def do_GET(self):
        self.done()
        query_dict = dict(urllib.parse.parse_qsl(
            urllib.parse.urlsplit(self.path).query))
        if 'getmsg' in self.path:
            self.send(self.router['/getmsg'](query_dict))
        elif 'uploadfile' in self.path:
            self.send(self.router['/uploadfile'](query_dict))
        else:
            self.send("{}")

    def do_POST(self):
        self.done()
        if 'uploadfile' in self.path:
            self.send(self.router['/uploadfile']())
        else:
            self.send("{}")

    def basepath(self):
        return "/factest"

    def updatemsg(self):
        pass

    def delmsg(self):
        pass

    def GetFileMd5(self, filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    def uploadfile(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )
        for field in list(form.keys()):
            field_item = form[field]
            filename = field_item.filename
            filevalue = field_item.value
            filesize = len(filevalue)  # 文件大小(字节)
            filetowr = "/tmp/%s" % filename
            with open(filetowr, 'wb') as f:
                f.write(filevalue)
            md5new = self.GetFileMd5(filetowr)
        return {"status": "ok", "data": {"md5": md5new}}

    def getrestlet(self):
        rr = {}
        rr['/getmsg'] = self.getmsg
        rr['/updatemsg'] = self.updatemsg
        rr['/delmsg'] = self.delmsg
        rr['/uploadfile'] = self.uploadfile
        return rr


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    try:
        server = ThreadedHTTPServer(('', 8084), Factest)
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
