#ifndef _RG_PSU_DRIVER_H_
#define _RG_PSU_DRIVER_H_

/**
 * dfd_get_psu_info - 获取电源信息
 * @index: 电源的编号,从1开始
 * @cmd: 电源信息类型,电源名称:2, 电源序列号:3,电源硬件版本号:5
 * @buf: 接收buf
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_psu_info(unsigned int psu_index, uint8_t cmd, char *buf, size_t count);

/**
 * dfd_get_psu_present_status_str - 获取电源状态
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_present_status_str(unsigned int psu_index, char *buf, size_t count);

/**
 * dfd_get_psu_out_status_str - 获取输出电源状态
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_out_status_str(unsigned int psu_index, char *buf, size_t count);

/**
 * dfd_get_psu_status_pmbus_str - 获取电源pmbus寄存器上的值
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_status_pmbus_str(unsigned int psu_index, char *buf, size_t count);

/**
 * dfd_get_psu_in_status_str - 获取输入电源状态
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_in_status_str(unsigned int psu_index, char *buf, size_t count);

/**
 * dfd_get_psu_input_type - 获取电源输入类型
 * @index: 电源的编号,从1开始
 * @buf: 接收buf
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_psu_input_type(unsigned int psu_index, char *buf, size_t count);

/**
 * dfd_get_psu_output_status - 获取电源输出状态
 * @index: 电源的编号,从1开始
 * return: 成功：return psu output status
 *       ：失败：返回负值
 */
ssize_t dfd_get_psu_output_status(unsigned int psu_index);

/**
 * dfd_get_psu_alert_status - 获取电源告警状态
 * @index: 电源的编号,从1开始
 * return: 成功：return psu output status
 *       ：失败：返回负值
 */
ssize_t dfd_get_psu_alert_status(unsigned int psu_index);

/**
 * dfd_get_psu_alarm_status - 获取电源PMBUS WORD STATUS状态
 * @index: 电源的编号,从1开始
 * return: 成功：return psu output status
 *       ：失败：返回负值
 */
ssize_t dfd_get_psu_alarm_status(unsigned int psu_index, char *buf, size_t count);

/**
 * dfd_get_psu_fan_ratio_str - 获取风扇目标转率
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_fan_ratio_str(unsigned int psu_index, char *buf, size_t count);

#endif /* _RG_PSU_DRIVER_H_ */
