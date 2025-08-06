#!/bin/bash
ip_addr="1.1.1.2"
str_erase="clear"
str_file=$3
str_flash=$4
BMC_VERSION_FLAG="202"
BMC_VERSION_TAG="207"
BMC_VERSION_USB0="212"

function usages()
{
  echo "USAGE:"
  echo "  e.g.: $0 upgrade [bmc|bios] file-path [master|slave|both]"
  echo " erase: update and erase config---only for upgrade bmc)"
  exit 1
}

# parameter parse
if [ "$1"x != "upgrade"x ];then
  usages
fi

if [ $# -lt 4 ] || [ $# -gt 5 ] ; then
  usages
fi

if [ ! -s $str_file ]; then
  echo "$3 does not exist"
  exit 1
fi

if [ "$str_flash"x != "master"x -a "$str_flash"x != "slave"x -a "$str_flash"x != "both"x ] ; then
  echo "Warning : $4 parameter error."
  exit 2
fi

version_bmc=""
version_bmc_num=""
function get_bmc_version()
{
  version_bmc=$(ipmitool mc info | grep "Firmware Revision" | awk 'NR==1{print $4}')
  version_bmc_num=$(echo "${version_bmc}"|sed "s/\.*//g")
  if [[ ! -z "$(echo $version_bmc_num | sed 's#[0-9]##g')" ]] || [[ -z $version_bmc_num ]]; then
      echo "Get BMC version failed----$version_bmc"
      exit 1
  fi
}

function upgrade_bios()
{
  case $str_flash in
    "master")
      /usr/local/bin/bios_upgrade ${ip_addr} $str_file 0
    ;;
    "slave")
      /usr/local/bin/bios_upgrade ${ip_addr} $str_file 1
    ;;
    "both")
      /usr/local/bin/bios_upgrade ${ip_addr} $str_file 1
      sleep 10
      /usr/local/bin/bios_upgrade ${ip_addr} $str_file 0
    ;;
    *)
      echo "Warning : $str_flash parameter error. failed to update bios"
    ;; # help
  esac
}

function upgrade_bmc_flash()
{
  if [ "${str_erase}"x == "erase"x ]; then
    /usr/local/bin/bmc_upgradev6.0 ${ip_addr} $str_file ${str_flash} ${str_erase}
  else
    /usr/local/bin/bmc_upgradev6.0 ${ip_addr} $str_file ${str_flash}
  fi
}

function upgrade_bmc6()
{
  if [ "${str_flash}"x == "master"x -o "${str_flash}"x == "slave"x ]; then
    timer_value=480
  elif [ "${str_flash}"x == "both"x ]; then
    timer_value=840
  else
    usages
    exit 0
  fi
  upgrade_bmc_flash
  sleep $timer_value
  # get bmc version
  version_bmc_num=""
  version_bmc_new=$(get_bmc_version)
  result_version=$(echo $?)
  count=10
  while [ $count -gt 0 ]
  do
    if [[ "$result_version"x == "1"x ]]; then
      let count=count-1
        version_bmc_new=$(get_bmc_version)
        result_version=$(echo $?)
      sleep 3
      continue
    fi
    echo "succeeded to upgrade bmc"
    return 0
  done
  #get bmc version failed
  if [ $count -eq 0 ]; then
    echo "get bmc version failed, try again"
  fi
}

function upgrade_bmc5()
{
  if [ "${str_erase}"x == "erase"x ]; then
    /usr/local/bin/bmc_upgradev5.0 ${ip_addr} $str_file ${str_flash} ${str_erase}
  else
    /usr/local/bin/bmc_upgradev5.0 ${ip_addr} $str_file ${str_flash}
  fi
}

function upgrade_bmc()
{
  if [ "${version_bmc_num}" -le "${BMC_VERSION_FLAG}" ]; then
    /usr/local/bin/bmc_upgradev2.0 $ip_addr $str_file
    exit 0
  elif [ "${version_bmc_num}" -le "${BMC_VERSION_TAG}" ]; then
    if [ "${str_erase}"x == "erase"x ]; then
      /usr/local/bin/bmc_upgradev4.0 ${ip_addr} $str_file ${str_erase}
    else
      /usr/local/bin/bmc_upgradev4.0 ${ip_addr} $str_file
    fi
    exit 0
  elif [ "${version_bmc_num}" -lt "${BMC_VERSION_USB0}" ]; then
    upgrade_bmc5
    exit 0
  elif [ "${version_bmc_num}" -ge "${BMC_VERSION_USB0}" ]; then
    upgrade_bmc6
    exit 0
  else
      exit 0
  fi
}

case $2 in
  "bios")
    if [ $# -ge 5 ]; then
      usages
    fi
    upgrade_bios
  ;;
  "bmc")
    get_bmc_version
    if [ $# -eq 5 ]; then
      if [ "$5"x != "erase" ]; then
        str_erase="erase"
      else
        usages
      fi
    fi
    upgrade_bmc
  ;;
  *)
    usages
  ;; # help
esac