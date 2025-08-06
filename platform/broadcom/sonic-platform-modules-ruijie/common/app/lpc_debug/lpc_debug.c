/*
 * Copyright(C) 2012 Ruijie Network. All rights reserved.
 */
/*
 * eth_demo.c
 * Original Author:  sonic_rd@ruijie.com.cn, 2012-1-10
 * 
 * 以太口驱动模块调试命令
 *
 * History 
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <linux/netlink.h>
#include "lpc_debug.h"

static int g_sockfd = -1;
static struct sockaddr_nl g_local;

static void eth_start_help(void)
{
    printf("\n");
    printf("do nothing!\n");
}

static void eth_mac_reg_help(void)
{
    printf("\n");
    printf("%-20s - read a CPLD reg\n",       "read");
    printf("%-20s - write a CPLD reg\n",      "write");
    printf("%-20s - CPLD reg check test\n",   "check");
    printf("%-20s - dump all CPLD regs\n",    "dump");
    printf("%-20s - dump all lpc cfg regs\n", "lpccfg");
}

static void eth_mac_reg_read_help(void)
{
    printf("\n");
    printf("read cpld registers\n");
    printf("    format: lpc_debug cpld_reg read 0x0\n");
}

static void eth_mac_reg_write_help(void)
{
    printf("\n");
    printf("write cpld registers\n");
    printf("    format: lpc_debug cpld_reg write 0x0 0x55\n");
}

static void eth_mac_reg_check_help(void)
{
    printf("\n");
    printf("check cpld registers\n");
    printf("    format: lpc_debug cpld_reg check\n");
}

int eth_nl_create_socket(void)
{
    g_sockfd = socket(PF_NETLINK, SOCK_RAW, NETLINK_TEST);
    if(g_sockfd < 0){
        printf("can not create a netlink socket\n");
        return -1;
    }

    memset(&g_local, 0, sizeof(struct sockaddr_nl));
    g_local.nl_family = AF_NETLINK;
    g_local.nl_pid = getpid();
    g_local.nl_groups = 0;
    if(bind(g_sockfd, (struct sockaddr *)&g_local, sizeof(g_local)) != 0){
        close(g_sockfd);
        g_sockfd = -1;
        printf("bind() error\n");
        return -1;
    }
    
    return 0;
}

void eth_nl_destroy_socket(void)
{
    close(g_sockfd);
    g_sockfd = -1;
}

int eth_nl_send_to_kernel(void *data, int len)
{
    struct sockaddr_nl kpeer;
    eth_nl_msg_t message;
    int retval;

    if (g_sockfd == -1) {
        printf("must create a netlink socket first\n");
        return -1;
    }

    //kpeerlen = sizeof(struct sockaddr_nl);

    memset(&kpeer, 0, sizeof(kpeer));
    kpeer.nl_family = AF_NETLINK;
    kpeer.nl_pid = 0;
    kpeer.nl_groups = 0;

    memset(&message, 0, sizeof(eth_nl_msg_t));
    message.hdr.nlmsg_len = NLMSG_SPACE(len);
    message.hdr.nlmsg_flags = 0;
    message.hdr.nlmsg_type = 0;
    message.hdr.nlmsg_seq = 0;
    message.hdr.nlmsg_pid = g_local.nl_pid;

    memcpy(NLMSG_DATA(&message), data, len);
    retval = sendto(g_sockfd, &message, message.hdr.nlmsg_len, 0, (struct sockaddr *)&kpeer, 
                sizeof(kpeer));
    if(retval == -1){
        perror("send error:\n");
        return -1;
    }

    return 0;
}

int eth_nl_recv_from_kernel(void *data, int len)
{
    struct sockaddr_nl kpeer;
    eth_nl_msg_t info;
    int kpeerlen, retval;

    if (g_sockfd == -1) {
        printf("must create a netlink socket first\n");
        return -1;
    }

    kpeerlen = sizeof(struct sockaddr_nl);

    memset(&kpeer, 0, sizeof(kpeer));
    kpeer.nl_family = AF_NETLINK;
    kpeer.nl_pid = 0;
    kpeer.nl_groups = 0;
    
recv_resp:
    retval = recvfrom(g_sockfd, &info, sizeof(eth_nl_msg_t), 0, (struct sockaddr *)&kpeer, 
        (unsigned int *)&kpeerlen);
    if(retval <= 0){
        goto recv_resp;
    }

    if ((unsigned int)len < retval - sizeof(struct nlmsghdr)) {
        return -1;
    }
    memcpy(data, info.data, retval - sizeof(struct nlmsghdr));

    return 0;
}

static ether_msg_t *eth_create_msg(int size)
{
    ether_msg_t *msg;

    msg = (ether_msg_t *)malloc(sizeof(ether_msg_t) + size);
    if (msg == NULL) {
        return NULL;
    }
    memset(msg, 0, sizeof(ether_msg_t) + size);

    msg->length = size;
    return msg;
}

static void eth_destroy_msg(ether_msg_t *msg)
{
    free(msg);
}

static void eth_send_msg_to_kernel(int argc, char **argv, int type)
{
    ether_msg_t *msg;
    int i, buf_len;
    char buf[MSG_BUF_SIZE];

    buf_len = 0;
    if (argc == 0) { /* 不带任何参数 */
        msg = eth_create_msg(0);
        if (msg == NULL) {
            printf("%s alloc memory fail!\n", __func__);
            return;
        }
    } else {
        memset(buf, 0, MSG_BUF_SIZE);
        for (i = 0; i < argc; i++) {
            buf_len += sprintf(buf + buf_len, "[%s]", argv[i]);  /* XXX:FIX ME */
        }
    
        msg = eth_create_msg(buf_len);
        if (msg == NULL) {
            printf("%s alloc memory fail!\n", __func__);
            return;
        }

        memcpy(msg->value, buf, buf_len);
    }
    msg->type = type;
    if (eth_nl_create_socket() != 0) {
        printf("%s create socket fail!\n", __func__);
        eth_destroy_msg(msg);
        return;
    }
    
    (void)eth_nl_send_to_kernel((void *)msg, buf_len + sizeof(ether_msg_t));
    eth_nl_destroy_socket();
    eth_destroy_msg(msg);
}

static void eth_cmd_start(int argc, char **argv, int type)
{
    argc = argc;
    argv = argv;
    type = type;
    /* to do... */
}

static eth_cmd_node_t mac_reg_cmd[] = {
    {0, 1, "read", ETH_MAC_REG_READ, NULL, eth_mac_reg_read_help, eth_send_msg_to_kernel},
    {0, 1, "write", ETH_MAC_REG_WRITE, NULL, eth_mac_reg_write_help, eth_send_msg_to_kernel},
    {0, 0, "check", ETH_MAC_REG_CHECK, NULL, eth_mac_reg_check_help, eth_send_msg_to_kernel},
    {0, 0, "dump", ETH_MAC_REG_DUMP_ALL, NULL, NULL, eth_send_msg_to_kernel},
    {0, 0, "lpccfg", ETH_MAC_REG_DUMP_PCI_CFG_ALL, NULL, NULL, eth_send_msg_to_kernel},
    {1, 0, " ", 0, NULL, NULL, NULL},
};

static eth_cmd_node_t top_cmd[] = {
    {0, 0, "start", ETH_START, NULL, eth_start_help, eth_cmd_start},
    {0, 0, "cpld_reg", ETH_MAC_REG, mac_reg_cmd, eth_mac_reg_help, NULL},
    {1, 0, " ", 0, NULL, NULL, NULL},
};

static void eth_cmd_help(void)
{
    printf("\n");
    printf("%-20s - \n", "start");
    printf("%-20s - read/write cpld reg \n", "cpld_reg");
}

int main(int argc, char *argv[])
{
    eth_cmd_node_t *node;
    char **param;
    int i, type, res;
    int param_num;

    if (argc == 1) {
        eth_cmd_help();
        return 0;
    }

    node = top_cmd;
    type = 0;
    for (i = 1; i < argc; i++) {
        while ((node != NULL) && (node->is_last_node != 1)) {
            res = strncmp(node->cmd, argv[i], strlen(node->cmd));
            if (res == 0) {
                type |= (node->cmd_id << ((i - 1) * 8)); /* 设置下类型 */
                if (node->sub_cmd_arr != NULL) {
                    if (i == argc - 1) {    /* 明显命令没敲完，打印下帮助信息 */
                        if (node->help_func != NULL) {
                            node->help_func();
                            return 0;
                        }
                    }
                    node = node->sub_cmd_arr;
                    break;
                } else if (node->func != NULL) { /* 找到节点 */
                    if (i == argc - 1) {
                        if (node->have_arg == 0) {
                            param = NULL;
                            param_num = 0;
                        } else {    /* 明显命令没敲完，打印下帮助信息 */
                            if (node->help_func != NULL) {
                                node->help_func();
                            }
                            return 0;
                        }
                    } else {
                        param = argv + i + 1;
                        param_num = argc - i - 1;
                    }
                    node->func(param_num, param, type);
                    return 0;
                } else {
                    if (node->help_func != NULL) {
                        node->help_func();
                        return 0;
                    }
                }
            }
            node++;
        }
    }

    return 0;
}
