PWD		= $(shell pwd)
EXTRA_CFLAGS:= -I$(M)/include
EXTRA_CFLAGS+= -Wall
SUB_BUILD_DIR = $(PWD)/build
SERVICE_DIR = $(PWD)/service
SUBDIRS:=$(shell pwd)/app
INSTALL_DIR = $(SUB_BUILD_DIR)/$(KERNEL_SRC)/$(INSTALL_MOD_DIR)
INSTALL_SCRIPT_DIR = $(SUB_BUILD_DIR)/usr/local/bin
INSTALL_LIB_DIR = $(SUB_BUILD_DIR)/usr/lib/python2.7/dist-packages
INSTALL_SERVICE_DIR = $(SUB_BUILD_DIR)/lib/systemd/system
COMMON_RJ_OUTPUT := $(shell pwd)/build
export SUB_BUILD_DIR COMMON_RJ_OUTPUT

all : CHECK SUBDIRS_OBJ
CHECK : 
	@if [ ! -d ${INSTALL_LIB_DIR} ]; then mkdir -p ${INSTALL_LIB_DIR} ;fi
	@if [ -d $(PWD)/lib/ ]; then cp -r $(PWD)/lib/* ${INSTALL_LIB_DIR} ;fi
	@if [ ! -d ${COMMON_RJ_OUTPUT} ]; then mkdir -p ${COMMON_RJ_OUTPUT} ;fi
	@if [ ! -d ${INSTALL_SCRIPT_DIR} ]; then mkdir -p ${INSTALL_SCRIPT_DIR} ;fi
	@if [ -d $(PWD)/script/ ]; then cp -r $(PWD)/script/* ${INSTALL_SCRIPT_DIR} ;fi
	@if [ -d $(INSTALL_SCRIPT_DIR) ]; then chmod +x $(INSTALL_SCRIPT_DIR)/* ;fi
	@if [ ! -d ${INSTALL_SERVICE_DIR} ]; then mkdir -p ${INSTALL_SERVICE_DIR} ;fi
	cp -r $(SERVICE_DIR)/*  $(INSTALL_SERVICE_DIR)

SUBDIRS_OBJ :
	@if [ -d ${SUBDIRS} ]; then make -C $(SUBDIRS); fi
	

clean:
	rm -rf $(SUB_BUILD_DIR)
