#ifndef _RG_LED_DRIVER_H_
#define _RG_LED_DRIVER_H_

/**
 * dfd_get_led_status - 获取LED等状态
 * @led_id: led灯类型
 * @led_index: led灯偏移
 * @buf: LED灯状态接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_led_status(uint16_t led_id, uint8_t led_index, char *buf, size_t count);

/**
 * dfd_set_led_status - 设置LED灯状态
 * @led_id: led灯类型
 * @led_index: led灯偏移
 * @value: LED灯状态值
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_set_led_status(uint16_t led_id, uint8_t led_index, int value);

#endif /* _RG_LED_DRIVER_H_ */
