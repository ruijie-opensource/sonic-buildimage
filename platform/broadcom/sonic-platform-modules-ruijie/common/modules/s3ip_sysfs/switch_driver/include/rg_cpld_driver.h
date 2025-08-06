#ifndef _RG_CPLD_DRIVER_H_
#define _RG_CPLD_DRIVER_H_

/**
 * dfd_get_cpld_name - 获取CPLD名称
 * @main_dev_id: 主板:0 子卡:5
 * @index:CPLD的编号,从0开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_cpld_name(uint8_t main_dev_id, unsigned int cpld_index, char *buf, size_t count);

/**
 * dfd_get_cpld_type - 获取CPLD型号
 * @main_dev_id: 主板:0 子卡:5
 * @index:CPLD的编号,从0开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_cpld_type(uint8_t main_dev_id, unsigned int cpld_index, char *buf, size_t count);

/**
 * dfd_get_cpld_fw_version - 获取CPLD固件版本号
 * @main_dev_id: 主板:0 子卡:5
 * @index:CPLD的编号,从0开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_cpld_fw_version(uint8_t main_dev_id, unsigned int cpld_index, char *buf, size_t count);

/**
 * dfd_get_cpld_hw_version - 获取CPLD硬件版本号
 * @main_dev_id: 主板:0 子卡:5
 * @index:CPLD的编号,从0开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_cpld_hw_version(uint8_t main_dev_id, unsigned int cpld_index, char *buf, size_t count);

/**
 * dfd_set_cpld_testreg - 设置CPLD测试寄存器值
 * @main_dev_id: 主板:0 子卡:5
 * @cpld_index：CPLD编号,从0开始
 * @value:   写入测试寄存器的值
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_set_cpld_testreg(uint8_t main_dev_id, unsigned int cpld_index, int value);

/**
 * dfd_get_cpld_testreg - 读取CPLD测试寄存器值
 * @main_dev_id: 主板:0 子卡:5
 * @cpld_index: CPLD编号,从0开始
 * @value:   读到的测试寄存器值
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_get_cpld_testreg(uint8_t main_dev_id, unsigned int cpld_index, int *value);

/**
 * dfd_get_cpld_testreg_str - 读取CPLD测试寄存器值
 * @main_dev_id: 主板:0 子卡:5
 * @cpld_index: CPLD编号,从0开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_cpld_testreg_str(uint8_t main_dev_id, unsigned int cpld_index,
            char *buf, size_t count);

#endif /* _RG_CPLD_DRIVER_H_ */
