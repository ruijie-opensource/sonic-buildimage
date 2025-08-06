#ifndef _RG_SFF_DRIVER_H_
#define _RG_SFF_DRIVER_H_

/**
 * dfd_set_sff_cpld_info - 设置光模块CPLD寄存器状态
 * @sff_index: 光模块编号，从1开始
 * @cpld_reg_type: 光模块CPLD寄存器类型
 * @value: 写入寄存器的值
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_set_sff_cpld_info(unsigned int sff_index, int cpld_reg_type, int value);

/**
 * dfd_get_sff_cpld_info - 获取光模块CPLD寄存器状态
 * @sff_index: 光模块编号，从1开始
 * @cpld_reg_type: 光模块CPLD寄存器类型
 * @buf: 光模块E2信息接收buf
 * @count：buf长度
 * return: 成功：返回填充buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_sff_cpld_info(unsigned int sff_index, int cpld_reg_type, char *buf, size_t count);

/**
 * dfd_get_eth_optoe_type - 获取光模块optoe类型
 * @sff_index: 光模块编号，从1开始
 * @optoe_type: 光模块optoe类型
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_get_eth_optoe_type(unsigned int sff_index, int *optoe_type);

/**
 * dfd_set_eth_optoe_type - 设置光模块optoe类型
 * sff_index: start with 1
 * @optoe_type: optoe_type received
 */
int dfd_set_eth_optoe_type(unsigned int sff_index, int optoe_type);

#endif /* _RG_SFF_DRIVER_H_ */
