#ifndef _RG_FAN_DRIVER_H_
#define _RG_FAN_DRIVER_H_

/**
 * dfd_get_fan_status_str - 获取风扇状态
 * @index: 风扇的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_fan_status_str(unsigned int fan_index, char *buf, size_t count);

/**
 * dfd_get_fan_info - 获取风扇信息
 * @index: 风扇的编号,从1开始
 * @cmd: 风扇信息类型,风扇名称:2, 风扇序列号:3,风扇硬件版本号:5
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_fan_info(unsigned int fan_index, uint8_t cmd, char *buf, size_t count);

/**
 * dfd_get_fan_speed - 获取风扇转速
 * @fan_index: 风扇的编号,从1开始
 * @motor_index: 马达的编号,从1开始
 * @speed: 转速值
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_get_fan_speed(unsigned int fan_index, unsigned int motor_index,unsigned int *speed);

/**
 * dfd_get_fan_speed_str - 获取风扇转速
 * @fan_index: 风扇的编号,从1开始
 * @motor_index: 马达的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
ssize_t dfd_get_fan_speed_str(unsigned int fan_index, unsigned int motor_index,
            char *buf, size_t count);

/**
 * dfd_set_fan_pwm - 设置风扇转速占空比
 * @fan_index: 风扇的编号,从1开始
 * @pwm:   占空比
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_set_fan_pwm(unsigned int fan_index, int pwm);

/**
 * dfd_get_fan_pwm - 获取风扇转速占空比
 * @fan_index: 风扇的编号,从1开始
 * @pwm:   占空比
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_get_fan_pwm(unsigned int fan_index, int *pwm);

/**
 * dfd_get_fan_pwm_str - 获取风扇转速占空比
 * @fan_index: 风扇的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
ssize_t dfd_get_fan_pwm_str(unsigned int fan_index, char *buf, size_t count);

/**
 * dfd_get_fan_motor_speed_tolerance_str - 获取风扇转速公差
 * @fan_index: 风扇的编号,从1开始
 * @motor_index: 马达的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
ssize_t dfd_get_fan_motor_speed_tolerance_str(unsigned int fan_index, unsigned int motor_index,
            char *buf, size_t count);

/**
 * dfd_get_fan_speed_target - 获取风扇标准转速
 * @fan_index
 * @motor_index
 * @value 标准转速值
 * @returns: 0成功，负值：失败
 */
int dfd_get_fan_speed_target(unsigned int fan_index, unsigned int motor_index, int *value);

/**
 * dfd_get_fan_motor_speed_target_str - 获取风扇标准转速
 * @fan_index: 风扇的编号,从1开始
 * @motor_index: 马达的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
ssize_t dfd_get_fan_motor_speed_target_str(unsigned int fan_index, unsigned int motor_index,
            char *buf, size_t count);

/**
 * dfd_get_fan_direction_str - 获取风扇风道类型
 * @fan_index：风扇偏移，从1开始
 * @buf ：风道类型接收buf
 * @count ：风道类型接收buf长度
 * @returns: 成功：风道类型字符串长度
 *           失败：负值
 */
ssize_t dfd_get_fan_direction_str(unsigned int fan_index, char *buf, size_t count);

/**
 * dfd_get_fan_motor_speed_max_str - 获取风扇标准转速
 * @fan_index: 风扇的编号,从1开始
 * @motor_index: 马达的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
ssize_t dfd_get_fan_motor_speed_max_str(unsigned int fan_index, unsigned int motor_index,
            char *buf, size_t count);

/**
 * dfd_get_fan_motor_speed_min_str - 获取风扇标准转速
 * @fan_index: 风扇的编号,从1开始
 * @motor_index: 马达的编号,从1开始
 * @buf: 接收buf
 * @count: 接收buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
ssize_t dfd_get_fan_motor_speed_min_str(unsigned int fan_index, unsigned int motor_index,
            char *buf, size_t count);

#endif /* _RG_FAN_DRIVER_H_ */
