#ifndef _RG_FPGA_DRIVER_H_
#define _RG_FPGA_DRIVER_H_

/**
 * dfd_get_fpga_name - 获取FPGA名称
 * @main_dev_id: 主板:0 子卡:5
 * @index:FPGA的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_fpga_name(uint8_t main_dev_id, unsigned int fpga_index, char *buf, size_t count);

/**
 * dfd_get_fpga_type - 获取FPGA型号
 * @main_dev_id: 主板:0 子卡:5
 * @index:FPGA的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_fpga_type(uint8_t main_dev_id, unsigned int fpga_index, char *buf, size_t count);

/**
 * dfd_get_fpga_fw_version - 获取FPGA固件版本号
 * @main_dev_id: 主板:0 子卡:5
 * @index:FPGA的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_fpga_fw_version(uint8_t main_dev_id, unsigned int fpga_index, char *buf, size_t count);

/**
 * dfd_get_fpga_hw_version - 获取FPGA硬件版本号
 * @main_dev_id: 主板:0 子卡:5
 * @index:FPGA的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_fpga_hw_version(uint8_t main_dev_id, unsigned int fpga_index, char *buf, size_t count);

/**
 * dfd_set_fpga_testreg - 设置FPGA测试寄存器值
 * @main_dev_id: 主板:0 子卡:5
 * @fpga_index：FPGA编号,从1开始
 * @value:   写入测试寄存器的值
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_set_fpga_testreg(uint8_t main_dev_id, unsigned int fpga_index, int value);

/**
 * dfd_get_fpga_testreg - 读取FPGA测试寄存器值
 * @main_dev_id: 主板:0 子卡:5
 * @fpga_index: FPGA编号,从1开始
 * @value:   读到的测试寄存器值
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_get_fpga_testreg(uint8_t main_dev_id, unsigned int fpga_index, int *value);

/**
 * dfd_get_fpga_testreg_str - 读取FPGA测试寄存器值
 * @main_dev_id: 主板:0 子卡:5
 * @fpga_index: FPGA编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_fpga_testreg_str(uint8_t main_dev_id, unsigned int fpga_index,
            char *buf, size_t count);

#endif /* _RG_FPGA_DRIVER_H_ */
