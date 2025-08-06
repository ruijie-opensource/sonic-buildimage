#!/bin/bash

#platform init script for B6580-48CQ8QC

install_python_api_package() {
    device="/usr/share/sonic/device"
    platform=$(/usr/local/bin/sonic-cfggen -H -v DEVICE_METADATA.localhost.platform)

    rv=$(pip3 install $device/$platform/sonic_platform-1.0-py3-none-any.whl)
}

remove_python_api_package() {
    rv=$(pip3 show sonic-platform > /dev/null 2>/dev/null)
    if [ $? -eq 0 ]; then
        rv=$(pip3 uninstall -y sonic-platform > /dev/null 2>/dev/null)
    fi
}

if [[ "$1" == "init" ]]; then
    echo "b6580-48cq8qc init"
    install_python_api_package

elif [[ "$1" == "deinit" ]]; then
    remove_python_api_package
else
     echo "b6580-48cq8qc_platform : Invalid option !"
fi
