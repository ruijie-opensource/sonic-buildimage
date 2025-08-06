/* lpc_debug.h */
#ifndef __LPC_DEBUG_H__
#define __LPC_DEBUG_H__

#define ETH_CMD_SIZE       16
#define ETH_HELP_SIZE      64
#define MSG_BUF_SIZE       256

#define NETLINK_TEST 17
#define MSG_LEN 256

typedef struct eth_nl_msg {
    struct nlmsghdr hdr;
    char data[MSG_LEN];
} eth_nl_msg_t;

typedef enum {
    ETH_START = 1,
    ETH_SHOW,
    ETH_SET,
    ETH_TEST,
    ETH_MAC_REG,
    ETH_PHY_REG,
} ether_dbg_top_cmd_t;

typedef enum {
    ETH_MAC_REG_READ = 1,
    ETH_MAC_REG_WRITE,
    ETH_MAC_REG_CHECK,
    ETH_MAC_REG_DUMP_ALL,
    ETH_MAC_REG_DUMP_PCI_CFG_ALL,
} ether_mac_reg_cmd_t;

#define ETH_DBG_TYPE(cmd1, cmd2, cmd3, cmd4) \
    ((cmd1) | ((cmd2) << 8) | ((cmd3) << 16) | ((cmd4) << 24))    
#define ETH_DBG_PARSE_TYPE(type, cmd1, cmd2, cmd3, cmd4) \
    do {\
        (cmd1) = (type) & 0xff;\
        (cmd2) = ((type) >> 8) & 0xff;\
        (cmd3) = ((type) >> 16) & 0xff;\
        (cmd4) = ((type) >> 24) & 0xff;\
    } while (0)

typedef struct {
    int type;
    int length;
    unsigned char value[128];
} ether_msg_t;

typedef struct eth_cmd_node eth_cmd_node_t;

struct eth_cmd_node {
    int is_last_node;                   /* 是否最后节点 */
    int have_arg;                       /* 命令是否带参数 */
    char cmd[ETH_CMD_SIZE];             /* 命令关键字 */
    int cmd_id;                         /* 命令类型 */
    eth_cmd_node_t *sub_cmd_arr;        /* 子节点，没有则为NULL */
    void (* help_func)(void);           /* 帮助信息 */
    void (* func)(int, char **, int);   /* 实现接口 */
};

#endif
