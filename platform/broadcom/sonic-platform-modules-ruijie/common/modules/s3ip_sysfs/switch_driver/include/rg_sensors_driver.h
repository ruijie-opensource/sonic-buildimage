#ifndef _RG_SENSORS_DRIVER_H_
#define _RG_SENSORS_DRIVER_H_

/**
 * dfd_get_temp_info - 获取温度信息
 * @main_dev_id: 主板:0 电源:2 子卡:5
 * @dev_index: 不存在设备索引则为0, 1表示slot1/psu1
 * @temp_index: 温度索引,从1开始
 * @temp_type: 读取类型,1:alias 2:type 3:max 4:max_hyst 5:min 6:input
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_temp_info(uint8_t main_dev_id, uint8_t dev_index, uint8_t temp_index,
            uint8_t temp_attr, char *buf, size_t count);

/**
 * dfd_get_voltage_info - 获取电压信息
 * @main_dev_id: 主板:0 子卡:5
 * @dev_index: 不存在设备索引则为0, 1表示slot1
 * @in_index: 电压索引,从1开始
 * @in_type: 电压类型,1:alias 2:type 3:max 4:max_hyst 5:min 6:input
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_voltage_info(uint8_t main_dev_id, uint8_t dev_index, uint8_t in_index,
            uint8_t in_attr, char *buf, size_t count);

/**
 * dfd_get_current_info - 获取电流信息
 * @main_dev_id: 主板:0 子卡:5
 * @dev_index: 不存在设备索引则为0, 1表示slot1
 * @in_index: 电流索引,从1开始
 * @in_type: 电流类型,1:alias 2:type 3:max 4:max_hyst 5:min 6:input
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_current_info(uint8_t main_dev_id, uint8_t dev_index, uint8_t curr_index,
            uint8_t curr_attr, char *buf, size_t count);

/**
 * dfd_get_psu_sensor_info - 获取电源PMBUS信息
 * @psu_index: 电源索引, 从1开始
 * @sensor_type: 获取的pmbus信息类型
 * @buf: pmbus结果存放buf
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_psu_sensor_info(uint8_t psu_index, uint8_t sensor_type, char *buf, size_t count);

#endif /* _RG_SENSORS_DRIVER_H_ */
