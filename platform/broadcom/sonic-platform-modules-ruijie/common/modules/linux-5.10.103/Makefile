PWD		= $(shell pwd)

EXTRA_CFLAGS:= -I$(M)/include
EXTRA_CFLAGS+= -Wall

obj-m := rg_lm75.o
obj-m += rg_tmp401.o
obj-m += rg_i2c_mux_pca9641.o
obj-m += rg_i2c_mux_pca954x.o
obj-m += rg_i2c_i801.o
obj-m += rg_spi_gpio.o
obj-m += rg_i2c_algo_bit.o
obj-m += rg_i2c_gpio.o
obj-m += rg_i2c_gpio_device.o
obj-m += mdio-bitbang.o
obj-m += rg_mdio_gpio.o
obj-m += rg_intel_spi.o
obj-m += intel_spi_pci.o
obj-m += intel_spi_platform.o

all :
	$(MAKE) -C $(KERNEL_SRC)/build M=$(PWD) modules
	@if [ ! -d $(module_out_put_dir) ]; then mkdir -p $(module_out_put_dir) ;fi
	cp -p  $(PWD)/*.ko $(module_out_put_dir)

.PHONY : clean
clean :
	rm -f ${PWD}/*.o ${PWD}/*.ko ${PWD}/*.mod.c ${PWD}/.*.cmd ${PWD}/.*.o.d 
	rm -f ${PWD}/Module.markers ${PWD}/Module.symvers ${PWD}/modules.order 
	rm -rf ${PWD}/.tmp_versions  
