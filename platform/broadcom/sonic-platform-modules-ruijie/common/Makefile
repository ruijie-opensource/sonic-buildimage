PWD		= $(shell pwd)
CC ?=gcc
INSTALL_MOD_DIR ?=extra
KVERSION   ?= $(shell uname -r)
KERNEL_SRC ?=  /lib/modules/$(KVERSION)
EXTRA_CFLAGS:= -I$(M)/include
EXTRA_CFLAGS+= -Wall
ifdef ENABLE_GCOV
ifeq ($(ENABLE_GCOV), y)
EXTRA_CFLAGS+= -fprofile-arcs -ftest-coverage -lgcov
endif
endif # ENABLE_GCOV
SUB_BUILD_DIR = $(PWD)/build
DIR_KERNEL_SRC = $(PWD)/modules
SCRIPT_DIR = $(PWD)/script
SERVICE_DIR = $(PWD)/service
BLACK_DRIVER_CONF_DIR = $(PWD)/modprobe_conf
MODULE_FIRMWARE = $(PWD)/module_firmware

app_dir = $(PWD)/app
app_build_dir = $(app_dir)/build
modules_build_dir = $(DIR_KERNEL_SRC)/build

INSTALL_MODULE_DIR = $(SUB_BUILD_DIR)/$(KERNEL_SRC)/$(INSTALL_MOD_DIR)
INSTALL_SCRIPT_DIR = $(SUB_BUILD_DIR)/usr/local/bin
INSTALL_SERVICE_DIR = $(SUB_BUILD_DIR)/lib/systemd/system
INSTALL_LIB_DIR = $(SUB_BUILD_DIR)/usr/lib/python3/dist-packages
INSTALL_BLACK_DRIVER = $(SUB_BUILD_DIR)/etc/modprobe.d
INSTALL_MODULE_FIRMWARE = $(SUB_BUILD_DIR)/lib/firmware

all:
	$(MAKE) -C $(app_dir)
	$(MAKE) -C $(DIR_KERNEL_SRC)
	@if [ ! -d ${INSTALL_MODULE_DIR} ]; then mkdir -p ${INSTALL_MODULE_DIR} ;fi
	@if [ ! -d ${INSTALL_SCRIPT_DIR} ]; then mkdir -p ${INSTALL_SCRIPT_DIR} ;fi
	@if [ ! -d ${INSTALL_SERVICE_DIR} ]; then mkdir -p ${INSTALL_SERVICE_DIR} ;fi
	@if [ ! -d ${INSTALL_LIB_DIR} ]; then mkdir -p ${INSTALL_LIB_DIR} ;fi
	@if [ -d $(PWD)/lib/ ]; then cp -r $(PWD)/lib/* ${INSTALL_LIB_DIR} ;fi
	@if [ -d $(PWD)/sonic_platform/ ]; then cp -rf $(PWD)/sonic_platform ${INSTALL_LIB_DIR} ;fi
	@if [ -d $(PWD)/self_detect/ ]; then cp -rf $(PWD)/self_detect ${INSTALL_SCRIPT_DIR} ;fi
	python3 setup.py bdist_wheel -d $(SUB_BUILD_DIR)
	cp -r $(app_build_dir)/module/*.ko $(INSTALL_MODULE_DIR)
	cp -r $(modules_build_dir)/*.ko $(INSTALL_MODULE_DIR)
	cp -r $(app_dir)/build/app/*  $(INSTALL_SCRIPT_DIR)
	cp -r $(SCRIPT_DIR)/*  $(INSTALL_SCRIPT_DIR)
	cp -r $(SERVICE_DIR)/*  $(INSTALL_SERVICE_DIR)
	@if [ -d $(INSTALL_SCRIPT_DIR) ]; then chmod +x $(INSTALL_SCRIPT_DIR)/* ;fi
	@if [ ! -d ${INSTALL_BLACK_DRIVER} ]; then mkdir -p ${INSTALL_BLACK_DRIVER} ;fi
	cp -r  $(BLACK_DRIVER_CONF_DIR)/*  $(INSTALL_BLACK_DRIVER)
	@if [ ! -d ${INSTALL_MODULE_FIRMWARE} ]; then mkdir -p ${INSTALL_MODULE_FIRMWARE} ;fi
	cp -r  $(MODULE_FIRMWARE)/*  $(INSTALL_MODULE_FIRMWARE)
clean:
	rm -rf $(SUB_BUILD_DIR)
