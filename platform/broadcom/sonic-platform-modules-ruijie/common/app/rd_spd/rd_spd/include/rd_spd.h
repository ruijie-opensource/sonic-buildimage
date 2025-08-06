#ifndef _RD_SPD_H_
#define _RD_SPD_H_

#define dbg_print(debug, fmt, arg...)  \
    if (debug == DEBUG_APP_ON || debug == DEBUG_ALL_ON) \
        { do {printf(fmt,##arg);} while (0); }

#define MAP_SIZE                    (4096)
#define BASE_ADDR                   (0x80000000)
#define PCI_VENDER_DEVICE_OFFSET    (0x00)
#define SMB_EEPROM                  (0)
#define SMB_TSOD                    (1)
#define MEM_INFO                    (11)
#define BIT(n)                      (1 << n)
/* Intel D1500 */
#define INTEL_D1500_SMB             (0x6fa88086)
#define INTEL_D1500_SELECT_EEPROM   (0xA0000000)
#define INTEL_D1500_SELECT_TSOD     (0x30000000)
#define INTEL_D1500_CMD_SEND        BIT(31)
#define INTEL_D1500_CMD_WORD_MODE   BIT(29)
#define INTEL_D1500_SMBUS_ERROR     BIT(29)
#define INTEL_D1500_CLOCK_OVERRIDE  BIT(27)
#define INTEL_D1500_SMBUS_BUSY      BIT(30)
#define INTEL_D1500_DTI_WP_EEPROM   (0x06 << 28)
#define INTEL_D1500_CMD_SMB_READ    (0x00 << 27)
#define INTEL_D1500_CMD_SMB_WRITE   (0x01 << 27)
#define INTEL_D1500_EE_PAGE_SEL0    (0x06)
#define INTEL_D1500_EE_PAGE_SEL1    (0x07)

#define INTEL_D1500_SMB_CNTL        (0x188)
#define INTEL_D1500_SMB_CMD         (0x184)
#define INTEL_D1500_SMB_STAT        (0x180)
/* Intel D1700 */
#define INTEL_D1700_SMB             (0x34488086)
#define INTEL_D1700_SELECT_EEPROM   (0x00005000)
#define INTEL_D1700_SELECT_TSOD     (0x00001800)
#define INTEL_D1700_CLOCK_OVERRIDE  BIT(29)
#define INTEL_D1700_CMD_SEND        BIT(19)
#define INTEL_D1700_CMD_WORD_MODE   BIT(17)
#define INTEL_D1700_CMD_SMB_READ    (0x00 << 15)
#define INTEL_D1700_CMD_SMB_WRITE   (0x01 << 15)
#define INTEL_D1700_DTI_WP_EEPROM   (0x06 << 11)
#define INTEL_D1700_EE_PAGE_SEL0    (0x06)
#define INTEL_D1700_EE_PAGE_SEL1    (0x07)

#define INTEL_D1700_SMBUS_ERROR     BIT(1)
#define INTEL_D1700_SMBUS_BUSY      BIT(0)
#define INTEL_D1700_SMBUS_TSOD_EN   BIT(20)
#define INTEL_D1700_SMB_CMD_CFG     (0x80)
#define INTEL_D1700_SMB_STAT_CFG    (0x84)
#define INTEL_D1700_SMB_DATA_CFG    (0x88)

#define MASK_16         0xFF
#define MASK_32         0xFFFF
#define MAX_REG         0x1FF
#define WAIT_TIME       100
#define SLEEP_TIME      50
#define MAX_LENGTH      256

#define DEBUG_INFO_LEN  20
#define DEBUG_FILE      "/.rd_spd_debug"
#define DEBUG_ON_ALL    "3"
#define DEBUG_ON_KERN   "2"
#define DEBUG_ON_INFO   "1"
#define DEBUG_OFF_INFO  "0"

enum debug_s {
    DEBUG_OFF = 0,
    DEBUG_APP_ON,
    DEBUG_KERN_ON,
    DEBUG_ALL_ON,
    DEBUG_IGNORE,
};

struct spd {
    int pci_id;
    int (*smb_read_byte)(void *map_base, int type, int reg_offset, int slot_id, unsigned int *spd_result);
};

#define SPD_PCIE_DEVICE(id, fn) \
    {   \
        .pci_id = id, \
        .smb_read_byte = fn, \
    }

extern int spd_debug(void);

#endif  /* _RD_SPD_H_ */
