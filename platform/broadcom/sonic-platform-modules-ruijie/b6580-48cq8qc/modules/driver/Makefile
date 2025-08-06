MAKEFILE_FILE_PATH = $(abspath $(lastword $(MAKEFILE_LIST)))
MODULES_DIR = $(abspath $(MAKEFILE_FILE_PATH)/../../../../common/modules)
KERNEL_MODULES_DIR = $(abspath $(MAKEFILE_FILE_PATH)/../../../../common/modules/linux-5.10.103)
FIRMWARE_UPGRADE_PATH = $(abspath $(MAKEFILE_FILE_PATH)/../../../../common/app/firmware_upgrade/firmware_driver/include)

EXTRA_CFLAGS+= -I$(MODULES_DIR)
EXTRA_CFLAGS+= -I$(FIRMWARE_UPGRADE_PATH)
EXTRA_CFLAGS+= -I$(KERNEL_MODULES_DIR)

obj-m += rg_pcie_dev_device.o
obj-m += rg_fpga_i2c_bus_device.o
obj-m += rg_fpga_pca954x_device.o
obj-m += rg_lpc_drv_device.o
obj-m += rg_i2c_dev_device.o
obj-m += rg_io_dev_device.o
obj-m += rg_firmware_upgrade_device.o
obj-m += rg_wdt_device.o
obj-m += rg_ssd_power_device.o
