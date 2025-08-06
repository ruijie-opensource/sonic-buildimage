# -*- coding: UTF-8 -*-

import sys
import os
import glob
import subprocess
    
NULL_VALUE = "NA"
ACCESS_FAILED = "ACCESS FAILED"

def write_sysfs(location, value):
    try:
        if not os.path.isfile(location):
            return False, ("location[%s] not found !" % location)
        with open(location, 'w') as fd1:
            fd1.write(value)
    except Exception as e:
        return False, (str(e)+" location[%s]" % location)
    return True, ("set location[%s] %s success !" % (location, value))

if sys.version_info[0] < 3:
    def read_sysfs(location):
        try:
            locations = glob.glob(location)
            with open(locations[0], 'rb') as fd1:
                retval = fd1.read()
            retval = retval.rstrip('\r\n')
            retval = retval.lstrip(" ")
            if retval == NULL_VALUE or retval == ACCESS_FAILED:
                return False, retval
        except Exception as e:
            return False, (str(e)+" location[%s]" % location)
        return True, retval

    def exec_os_cmd(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
        stdout = proc.communicate()[0]
        proc.wait()
        return proc.returncode, stdout
else:
    # python3 字节转字符串
    def byteTostr(val):
        strtmp = ''
        for i in range(len(val)):
            strtmp += chr(val[i])
        return strtmp
    
    def typeTostr(val):
        strtmp = ''
        if isinstance(val, bytes):
            strtmp = byteTostr(val)
        return strtmp
    
    def read_sysfs(location):
        try:
            locations = glob.glob(location)
            with open(locations[0], 'rb') as fd1:
                retval = fd1.read()
            retval = typeTostr(retval)
            retval = retval.rstrip('\r\n')
            retval = retval.lstrip(" ")
            if retval == NULL_VALUE or retval == ACCESS_FAILED:
                return False, retval
        except Exception as e:
            return False, (str(e) + "location[%s]" % location)
        return True, retval
    
    def exec_os_cmd(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
        stdout = proc.communicate()[0]
        proc.wait()
        stdout = typeTostr(stdout)
        return proc.returncode, stdout