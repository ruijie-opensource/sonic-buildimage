#ifndef _RG_SLOT_DRIVER_H_
#define _RG_SLOT_DRIVER_H_

/**
 * dfd_get_slot_status_str - 获取子卡状态
 * @slot_index: 子卡的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_slot_status_str(unsigned int slot_index, char *buf, size_t count);

/**
 * dfd_get_slot_info - 获取子卡信息
 * @slot_index: 子卡的编号,从1开始
 * @cmd: 子卡信息类型,子卡名称:2, 子卡序列号:3,子卡硬件版本号:5
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_slot_info(unsigned int slot_index, uint8_t cmd, char *buf, size_t count);

/**
 * dfd_get_slot_power_status_str - get power status of slot
 * @slot_index: 子卡的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_slot_power_status_str(unsigned int slot_index, char *buf, size_t count);

/**
 * dfd_set_slot_power_status_str - set power status of slot
 * @slot_index: 子卡的编号,从1开始
 * @value: Power status of slot
 * return: 成功：返回0
 *       ：失败：返回负值
 */
int dfd_set_slot_power_status_str(unsigned int slot_index, int value);

#endif /* _RG_SLOT_DRIVER_H_ */
