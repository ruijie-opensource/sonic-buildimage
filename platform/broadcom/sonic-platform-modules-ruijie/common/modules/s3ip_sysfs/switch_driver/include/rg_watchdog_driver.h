#ifndef _RG_WATCHDOG_DRIVER_H_
#define _RG_WATCHDOG_DRIVER_H_

/**
 * dfd_get_watchdog_info - 获取看门狗信息
 * @type: 看门狗信息类型
 * @buf: 接收buf
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_watchdog_info(uint8_t type, char *buf, size_t count);

ssize_t dfd_watchdog_get_status_str(char *buf, size_t count);
ssize_t dfd_watchdog_get_status(char *buf, size_t count);
ssize_t dfd_watchdog_set_status(int value);
ssize_t dfd_watchdog_get_timeout(char *buf, size_t count);
ssize_t dfd_watchdog_set_timeout(int value);
ssize_t dfd_watchdog_set_reset(int value);

#endif /* _RG_WATCHDOG_DRIVER_H_ */
