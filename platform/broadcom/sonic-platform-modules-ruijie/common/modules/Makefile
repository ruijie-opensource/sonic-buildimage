PWD		= $(shell pwd)
EXTRA_CFLAGS:= -I$(M)/include
EXTRA_CFLAGS+= -Wall
KVERSION   ?= $(shell uname -r)
KERNEL_SRC ?=  /lib/modules/$(KVERSION)

module_out_put_dir := $(PWD)/build
export module_out_put_dir

KERNEL_MODULES_SRC = $(PWD)/linux-5.10.103

RG_PLAT_SYSFS_DIR = $(PWD)/rg_plat_sysfs
S3IP_SYSFS_DIR = $(PWD)/s3ip_sysfs

export RG_PLAT_SYSFS_DIR
export S3IP_SYSFS_DIR

ruijie_common-objs := ruijie_common_module.o dfd_tlveeprom.o
obj-m += rg_fan.o
obj-m += rg_psu.o
obj-m += ruijie_platform.o
obj-m += rg_pmbus_core.o
obj-m += rg_csu550.o
obj-m += ruijie_common.o
obj-m += rg_ina3221.o
obj-m += rg_mac_bsc.o
obj-m += rg_tps53622.o
obj-m += rg_fpga_pcie.o
obj-m += rg_pcie_dev.o
obj-m += rg_fpga_i2c_bus_drv.o
obj-m += rg_fpga_pca954x_drv.o
obj-m += rg_lpc_drv.o
obj-m += rg_i2c_dev.o
obj-m += rg_io_dev.o
obj-m += rg_spi_ocores.o
obj-m += rg_spi_dev.o
obj-m += rg_eeprom_93xx46.o
obj-m += rg_ucd9000.o
obj-m += rg_spi_93xx46.o
obj-m += rg_gpio_d1500.o
obj-m += rg_gpio_device.o
obj-m += rg_wdt.o
obj-m += rg_optoe.o
obj-m += rg_spi_gpio_device.o
obj-m += rg_spi_gpio_d1700_device.o
obj-m += rg_xdpe132g5c.o
obj-m += rg_xdpe12284.o
obj-m += rg_i2c_gpio_device.o
obj-m += rg_i2c_gpio_d1700_device.o
obj-m += rg_mdio_gpio_device.o
obj-m += rg_platform_i2c_dev.o
obj-m += rg_xdpe132g5c_pmbus.o
obj-m += rg_isl68137.o
obj-m += rg_spi_gpio.o
obj-m += rg_spi_nor_device.o
obj-m += rg_ssd_power.o

all :
	$(MAKE) -C $(KERNEL_MODULES_SRC)
	$(MAKE) -C $(RG_PLAT_SYSFS_DIR)
	$(MAKE) -C $(S3IP_SYSFS_DIR)
	$(MAKE) -C $(KERNEL_SRC)/build M=$(PWD) modules
	@if [ ! -d $(module_out_put_dir) ]; then mkdir -p $(module_out_put_dir) ;fi
	cp -p  $(PWD)/*.ko $(module_out_put_dir)

clean :
	rm  -rf $(module_out_put_dir)
	rm -f ${PWD}/*.o ${PWD}/*.ko ${PWD}/*.mod.c ${PWD}/.*.cmd ${PWD}/.*.o.d
	rm -f ${PWD}/Module.markers ${PWD}/Module.symvers ${PWD}/modules.order
	rm -rf ${PWD}/.tmp_versions
