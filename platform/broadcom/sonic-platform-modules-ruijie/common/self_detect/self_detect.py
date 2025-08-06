#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
from faclib.all import *

## 生产测试主程序
if __name__ == '__main__':
    os.system("sudo chmod 775 /usr/local/bin/self_detect/patrol_factest.py")

    sde_init = TESTCASE.get("sde_init", 0)
    if sde_init == 1:
        os.system("sudo cp /tmp/self_detect/bfcmd /usr/local/bin/bfcmd")
        os.system("sudo chmod 775 /usr/local/bin/bfcmd")
        os.system("pkill -9 bf_switch")
        os.system("export SDE_INSTALL=/root/onl-bf-sde/install/ && sudo /root/onl-bf-sde/install/bin/bf_kdrv_mod_load $SDE_INSTALL")
        os.system("cd /root/onl-bf-sde && export SDE=/root/onl-bf-sde && export SDE_INSTALL=/root/onl-bf-sde/install/ && nohup ./run_switchd.sh -p diag > /dev/null 2>&1 & ")
        time.sleep(10)

    ip_netns_exec = TESTCASE.get("ip_netns_exec", 1)
    if ip_netns_exec == 1:
        commands = "sudo ip netns exec mgmt /usr/local/bin/self_detect/patrol_factest.py "
    else:
        commands = "/usr/local/bin/self_detect/patrol_factest.py "
    first_cmd = 1
    for command in sys.argv:
        if first_cmd == 1:
            first_cmd = 0
            continue
        commands += command
        commands += " "
    commands += "< /dev/null"
    self_detect_ret = os.system(commands)

    if sde_init == 1:
        os.system("pkill -9 bf_switch")
        time.sleep(1)
        os.system("export SDE_INSTALL=/root/onl-bf-sde/install/ && sudo /root/onl-bf-sde/install/bin/bf_kdrv_mod_unload $SDE_INSTALL")
        os.system("rm -f /usr/local/bin/bfcmd")

    if self_detect_ret == 0:
        sys.exit(0)
    else:
        sys.exit(1)

