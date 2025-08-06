#ifndef _RG_EEPROM_DRIVER_H_
#define _RG_EEPROM_DRIVER_H_

/**
 * dfd_get_eeprom_size - 获取eeprom的数据大小
 * @e2_type: 区分E2类型，包括整机、电源、风扇、模块E2
 * @index: E2的编号
 * return: 成功: 返回eeprom的数据大小
 *       : 失败: 返回负值
 */
int dfd_get_eeprom_size(int e2_type, int index);

/**
 * dfd_read_eeprom_data - 读取eeprom数据
 * @e2_type: 区分E2类型，包括整机、电源、风扇、模块E2
 * @index: E2的编号
 * @buf: eeprom数据接收buf
 * @offset: 读取的偏移地址
 * @count：读取的长度
 * return: 成功：返回填充buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_read_eeprom_data(int e2_type, int index, char *buf, loff_t offset, size_t count);

/**
 * dfd_write_eeprom_data - 写eeprom数据
 * @e2_type: 区分E2类型，包括整机、电源、风扇、模块E2
 * @index: E2的编号
 * @buf: eeprom数据buf
 * @offset: 写入的偏移地址
 * @count：写入的长度
 * return: 成功：返回写入的数据长度
 *       ：失败：返回负值
 */
ssize_t dfd_write_eeprom_data(int e2_type, int index, char *buf, loff_t offset, size_t count);
#endif /* _RG_EEPROM_DRIVER_H_ */
