#!/bin/bash

result=$(cat /host/machine.conf | grep onie_platform | cut -d = -f 2)
echo $result

if [ $result == "x86_64-ruijie_b6580-24dc8qc-r0" ];
then
    sdkmsg=1
elif [ $result == "x86_64-ruijie_b6580-48cq8qc-r0" ];
then
    sdkmsg=1;
elif [ $result == "x86_64-tencent_tcs8400-r0" ];
then
    sdkmsg=1;
elif [ $result == "x86_64-ruijie_b6980-64qc-r0" ];
then
    sdkmsg=1;
elif [ $result == "x86_64-tencent_tcs9400-r0" ];
then
    sdkmsg=1;
else
    sdkmsg=0;
fi

if [ $sdkmsg -eq 1 ];
then
    if [ -e /sonic_baresdk/baresdk_running.sh ];
	then
        /sonic_baresdk/baresdk_running.sh sdkmsg
    else
        echo "sctipt baresdk_running.sh miss"
        exit 0
    fi
else
    exit 0
fi
