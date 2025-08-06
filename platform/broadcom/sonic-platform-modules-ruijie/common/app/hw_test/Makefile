pes_parent_dir:=$(shell pwd)/$(lastword $(MAKEFILE_LIST))
pes_parent_dir:=$(shell dirname $(pes_parent_dir)) 

SUBDIRS=$(shell ls -l | grep ^d | awk '{if($$9 != "build") print $$9}')
INC = -I./inc

all : CHECK $(SUBDIRS)
CHECK : 
	@echo $(pes_parent_dir)
    
$(SUBDIRS):ECHO
#编译子目录
	make -C $@

ECHO:
	@echo $(SUBDIRS)
