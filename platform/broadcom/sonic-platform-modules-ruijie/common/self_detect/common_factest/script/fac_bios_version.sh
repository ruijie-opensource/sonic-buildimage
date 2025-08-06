#!/bin/bash

target_dir="/host/sonic"
target_file="/host/sonic/bios_info"
config_file="/usr/local/bin/fac_bios_version_device.conf"

if [ ! -d $target_dir ];then
    mkdir $target_dir
fi

if [ ! -f $target_file ];then
    echo "master:" > $target_file
    echo "slave:" >> $target_file
fi

if [ ! -f $config_file ];then
    logger -t fac_bios_version.sh -p info "error:no file ${config_file}"
    exit -1
fi

general_common_command=`which cmdx.py`
if [ -z "$general_common_command" ]; then
    logger -t fac_bios_version.sh -p info "no cmdx.py command"
fi

device_machine=`grep onie_platform /host/machine.conf`
if [ -z "$device_machine" ]; then
    logger -t fac_bios_version.sh -p info "error:get onie_platform failed"
    exit -1
fi
machine_tmp=${device_machine##*_}
machine=${machine_tmp%-*}
echo ${machine}

device_name_config=`grep ${machine} ${config_file}`
echo ${device_name_config}
device_name=${device_name_config%_*}
echo ${device_name}
if [ -z "$device_name" ]; then
    logger -t fac_bios_version.sh -p info "error:get current device failed"
    exit -1
fi
. ${config_file}

cycle_count=0
while true
        do
            BIOS_VER=`dmidecode | grep -Po 'Version[" :]+\K[^"]+'|head -n 1`
            if [ -z "$BIOS_VER" ]; then
                logger -t fac_bios_version.sh -p info "error:get bios version failed"
                sleep 30
                continue
            fi
            # device lpc:"b6920-4c" "tcs83-100f" "b6510-32cq" "tcs82-100f" "bs100r0"
            # device i2c bus 0:"tcs81-100f" "b6510-48vs8cq"
            # device i2c bus 2:"BT2575" "BC10072" "b6520-64cq"

            bios_version_cmd=${device_name}"_cmd"
            cur_cmd=`eval echo \\$${bios_version_cmd}`
            ret=`${cur_cmd}`
            if [ "${ret}" = `eval echo \\$${device_name}"_master"` ];then
                echo "master"
                sed -i "s/^master:.*/master:$BIOS_VER/" $target_file && break
            elif [ "${ret}" = `eval echo \\$${device_name}"_slave"` ];then
                echo "slave"
                sed -i "s/^slave:.*/slave:$BIOS_VER/" $target_file && break
            else
                logger -t fac_bios_version.sh -p info "error:get flash failed:${cur_cmd} ${ret}"
                echo "error"
            fi

            #let cycle_count +=1
            cycle_count=$(( $cycle_count + 1 ))
            if [ ${cycle_count} -lt 15 ];then
                logger -t fac_bios_version.sh -p info "error:please check device"
                sleep 3
            else
                break
            fi

        done
