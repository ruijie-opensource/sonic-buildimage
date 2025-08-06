#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <unistd.h>
#include "rd_spd.h"

static int debug_on;

static unsigned int spd_read(void *map_base, int reg)
{
    void *virt_addr;

    virt_addr = map_base + reg;
    return *((unsigned int *) virt_addr);
}

static void spd_write(void *map_base, int reg, unsigned int val)
{
    void *virt_addr;

    virt_addr = map_base + reg;
    *((unsigned int *) virt_addr) = val;
}

static int intel_d1500_spd_set_page(int spd_page, void *map_base)
{
    unsigned int write_val;
    unsigned int smb_sa;
    int timeout;

    timeout = 0;
    smb_sa = (spd_page == 0) ? INTEL_D1500_EE_PAGE_SEL0 : INTEL_D1500_EE_PAGE_SEL1;
    /* Send CMD one */
    write_val = INTEL_D1500_CLOCK_OVERRIDE | INTEL_D1500_DTI_WP_EEPROM;
    spd_write(map_base, INTEL_D1500_SMB_CNTL, write_val);
    dbg_print(debug_on, "INTEL_D1500_SMB_CNTL 0x%x\n", write_val);
    /* Send CMD two */
    write_val = INTEL_D1500_CMD_SEND | INTEL_D1500_CMD_SMB_WRITE | (smb_sa & 0x7) << 24;
    dbg_print(debug_on, "INTEL_D1500_SMB_CMD 0x%x\n", write_val);
    spd_write(map_base, INTEL_D1500_SMB_CMD, write_val);
    usleep(100);
    while (!(spd_read(map_base, INTEL_D1500_SMB_STAT) >> 31)) {
        if (timeout > WAIT_TIME) {
            printf("operation timeout\n");
            return -1;
        }
        usleep(SLEEP_TIME);
        timeout++;
    }
    return 0;
}

static int intel_d1500_smb_read_byte(void *map_base, int type, int reg_offset, int slot_id, unsigned int *spd_result)
{
    unsigned int write_val, read_val;
    int timeout, ret, spd_page;

    timeout = 0;
    spd_page = 0;
    if ((reg_offset > 0xFF) && (type == SMB_EEPROM)) {
        reg_offset = reg_offset - 0x100;
        spd_page = 1;
    }
    if (type == SMB_EEPROM) {
        ret = intel_d1500_spd_set_page(spd_page, map_base);
        if (ret < 0) {
            printf("SPD set page %d failed\n", spd_page);
            return -1;
        }
    }
    /* Send CMD one */
    write_val = INTEL_D1500_CLOCK_OVERRIDE;
    write_val = (type == SMB_EEPROM) ? write_val | INTEL_D1500_SELECT_EEPROM : write_val | INTEL_D1500_SELECT_TSOD;
    spd_write(map_base, INTEL_D1500_SMB_CNTL, write_val);
    read_val = spd_read(map_base, INTEL_D1500_SMB_CNTL);
    dbg_print(debug_on, "SMB_CNTL: 0x%08X\n", read_val);
    /* Send CMD two */
    write_val = INTEL_D1500_CMD_SEND | (reg_offset & MASK_16) << 16 | (slot_id & 0x7) << 24;
    write_val = (type == SMB_EEPROM) ? write_val : write_val | INTEL_D1500_CMD_WORD_MODE;
    dbg_print(debug_on, "0x%x\n", write_val);
    spd_write(map_base, INTEL_D1500_SMB_CMD, write_val);
    read_val = spd_read(map_base, INTEL_D1500_SMB_CMD);
    dbg_print(debug_on, "SMB_CMD: 0x%08X\n", read_val);
    /* Wait instruction exec */
    while (!(spd_read(map_base, INTEL_D1500_SMB_STAT) >> 31)) {
        if (timeout > WAIT_TIME) {
            printf("operation timeout\n");
            return -1;
        }
        usleep(SLEEP_TIME);
        timeout++;
    }
    /* Read SPD/TSOD  */
    read_val = spd_read(map_base, INTEL_D1500_SMB_STAT);
    dbg_print(debug_on, "SMB_STAT: 0x%X\n", read_val);
    if (read_val & INTEL_D1500_SMBUS_ERROR) {
        printf("SMBUS Error\n");
        return -1;
    }
    *spd_result = read_val;
    return 0;
}

static int intel_d1700_spd_set_page(int spd_page, void *map_base)
{
    unsigned int write_val;
    unsigned int smb_sa;
    int timeout;

    timeout = 0;
    smb_sa = (spd_page == 0) ? INTEL_D1700_EE_PAGE_SEL0 : INTEL_D1700_EE_PAGE_SEL1;
    write_val = INTEL_D1700_CLOCK_OVERRIDE | (smb_sa & 0x7) << 8 | INTEL_D1700_CMD_SEND | (INTEL_D1700_CMD_SMB_WRITE) | INTEL_D1700_DTI_WP_EEPROM;
    dbg_print(debug_on, "setpage value 0x%x\n", write_val);
    spd_write(map_base, INTEL_D1700_SMB_DATA_CFG, 0x00);
    spd_write(map_base, INTEL_D1700_SMB_CMD_CFG, write_val);
    usleep(100);
    while ((spd_read(map_base, INTEL_D1700_SMB_STAT_CFG) & INTEL_D1700_SMBUS_BUSY)) {
        if (timeout > WAIT_TIME) {
            printf("operation timeout\n");
            spd_write(map_base, INTEL_D1700_SMB_CMD_CFG, spd_read(map_base, INTEL_D1700_SMB_CMD_CFG) | INTEL_D1700_SMBUS_TSOD_EN);
            return -1;
        }
        usleep(SLEEP_TIME);
        timeout++;
    }
    spd_write(map_base, INTEL_D1700_SMB_CMD_CFG, spd_read(map_base, INTEL_D1700_SMB_CMD_CFG) | INTEL_D1700_SMBUS_TSOD_EN);
    return 0;
}

static int intel_d1700_smb_read_byte(void *map_base, int type, int reg_offset, int slot_id, unsigned int *spd_result)
{
    unsigned int write_val, read_val;
    int timeout, ret, spd_page;

    timeout = 0;
    spd_page = 0;
    if ((reg_offset > 0xFF) && (type == SMB_EEPROM)) {
        reg_offset = reg_offset - 0x100;
        spd_page = 1;
    }
    if (type == SMB_EEPROM) {
        ret = intel_d1700_spd_set_page(spd_page, map_base);
        if (ret < 0) {
            printf("SPD set page %d failed\n", spd_page);
            return -1;
        }
    }
    /* Send CMD one */
    write_val = INTEL_D1700_CLOCK_OVERRIDE | (slot_id & 0x7) << 8 | (reg_offset & MASK_16) | INTEL_D1700_CMD_SEND;
    write_val = (type == SMB_EEPROM) ?  write_val | INTEL_D1700_SELECT_EEPROM: write_val | INTEL_D1700_SELECT_TSOD | INTEL_D1700_CMD_WORD_MODE;
    dbg_print(debug_on, "0x%x\n", write_val);
    spd_write(map_base, INTEL_D1700_SMB_CMD_CFG, write_val);
    read_val = spd_read(map_base, INTEL_D1700_SMB_CMD_CFG);
    dbg_print(debug_on, "SMB_CMD_CFG: 0x%08X\n", read_val);
    while ((spd_read(map_base, INTEL_D1700_SMB_STAT_CFG) & INTEL_D1700_SMBUS_BUSY)) {
        if (timeout > WAIT_TIME) {
            printf("operation timeout\n");
            spd_write(map_base, INTEL_D1700_SMB_CMD_CFG, spd_read(map_base, INTEL_D1700_SMB_CMD_CFG) | INTEL_D1700_SMBUS_TSOD_EN);
            return -1;
        }
        usleep(SLEEP_TIME);
        timeout++;
    }
    if ((spd_read(map_base, INTEL_D1700_SMB_STAT_CFG) & INTEL_D1700_SMBUS_ERROR)) {
        printf("SMBUS Error\n");
        spd_write(map_base, INTEL_D1700_SMB_CMD_CFG, spd_read(map_base, INTEL_D1700_SMB_CMD_CFG) | INTEL_D1700_SMBUS_TSOD_EN);
        return -1;
    }
    read_val = spd_read(map_base, INTEL_D1700_SMB_DATA_CFG);
    dbg_print(debug_on, "SMB_DATA: 0x%X\n", read_val);
    *spd_result = read_val;
    spd_write(map_base, INTEL_D1700_SMB_CMD_CFG, spd_read(map_base, INTEL_D1700_SMB_CMD_CFG) | INTEL_D1700_SMBUS_TSOD_EN);
    dbg_print(debug_on, "smb_config_mode %x\n", write_val);
    return 0;
}

struct spd supported_dev_id[] = {
    SPD_PCIE_DEVICE(INTEL_D1500_SMB, intel_d1500_smb_read_byte),
    SPD_PCIE_DEVICE(INTEL_D1700_SMB, intel_d1700_smb_read_byte),
};

static int spd_tsod_read(int bus_num, int dev_id, int slot_id, int func_id, unsigned int reg_offset, int size, int type,  unsigned int *value)
{
    int fd;
    void *map_base;
    unsigned int read_val, write_val, pci_id, spd_result;
    off_t target;
    int ret, i;
    struct spd *supported_dev;

    ret = -1;
    target = BASE_ADDR | (bus_num << 20) | (dev_id << 15) | (func_id << 12);
    dbg_print(debug_on, "map address %x\n", target);

    if ((fd = open("/dev/mem", O_RDWR | O_SYNC)) == -1) {
        printf("open /dev/mem failed\n");
        return -1;
    }
    dbg_print(debug_on, "/dev/mem opened.\n");

    map_base = mmap(0, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, target);
    if (map_base == MAP_FAILED) {
        close(fd);
        printf("map /dev/mem failed\n");
        return -1;
    }
    dbg_print(debug_on, "Memory mapped at address %p.\n", map_base);
    /* Identify the pci device */
    pci_id = spd_read(map_base, PCI_VENDER_DEVICE_OFFSET);
    for (i = 0; i < (sizeof(supported_dev_id) /sizeof((supported_dev_id)[0])); i++) {
        if (pci_id == supported_dev_id[i].pci_id) {
            supported_dev = &supported_dev_id[i];
            break;
        }
    }

    if (supported_dev == NULL) {
        printf("get support dev failed\n");
        goto exit;
    }

    for (i = 0; i < size; i++) {
        ret = supported_dev->smb_read_byte(map_base, type, reg_offset + i, slot_id, &spd_result);
        if (ret < 0) {
            goto exit;
        }
        value[i] = spd_result  & MASK_32;
    }
exit:
    if (munmap(map_base, MAP_SIZE) == -1) {
        close(fd);
        printf("unmap /dev/mem failed\n");
        return -1;
    }
    close(fd);
    return (ret < 0) ? -1:0;
}

static void usage(void)
{
    printf("Uasge: rd_spd [spd/tsod] [bus] [device_id] [function] [reg offset] [size]\n");

}

int main(int argc, char **argv)
{
    int fd, ret;
    int bus_num, dev_id, slot_id, func_id, type, size, i;
    unsigned int reg_offset;
    unsigned int value[MAX_LENGTH];

    debug_on = spd_debug();

    if (argc < 7 || argc > 8) {
        usage();
        return -1;
    }

    if (strcmp(argv[1], "spd") == 0) {
        type = SMB_EEPROM;
    } else if (strcmp(argv[1], "tsod") == 0) {
        type = SMB_TSOD;
    } else {
        printf("Select spd or tsod mode\n");
        return -1;
    }
    size = 1;
    bus_num = strtoul(argv[2], 0, 0);
    dev_id = strtoul(argv[3], 0, 0);
    func_id = strtoul(argv[4], 0, 0);
    slot_id = strtoul(argv[5], 0, 0);
    reg_offset = strtoul(argv[6], 0, 0);
    if (argc == 8) {
        size = strtoul(argv[7], 0, 0);
    }

    if (reg_offset > MAX_REG) {
        printf("Wrong reg select\n");
        return -1;
    }

    if (size > MAX_LENGTH) {
        printf("Size %d not suppported\n", size);
        return -1;
    }

    ret = spd_tsod_read(bus_num, dev_id, slot_id, func_id, reg_offset, size, type, value);
    if (ret == -1) {
        printf("Read Fail\n");
        return -1;
    }

    for (i = 0; i < size; i++) {
        printf("0x%04x\n", value[i]);
    }

    return 0;
}
