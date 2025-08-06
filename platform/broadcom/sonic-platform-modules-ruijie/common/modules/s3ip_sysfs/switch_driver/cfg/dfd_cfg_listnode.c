/*
 * Copyright(C) 2001-2015 Ruijie Network. All rights reserved.
 */
/*
 * dfd_cfg_listnode.c
 * Original Author: sonic_rd@ruijie.com.cn 2020-02-17
 *
 * 链表结构模块，节点按插入先后顺序组织，链表创建只有查询操作，无锁保护
 * 内核模块使用，用户空间<linux/list.h>及kmalloc需要修订
 *
 * History
 *  [Version]        [Author]                   [Date]            [Description]
 *     v1.0    sonic_rd@ruijie.com.cn         2020-02-17        Initial version
 *
 */

#include <linux/list.h>
#include <linux/slab.h>

#include "../include/dfd_cfg_listnode.h"

/**
 * 查找节点
 * @root: 根节点指针
 * @key: 节点索引值
 *
 * @return : 节点数据指针，NULL失败
 */
void *lnode_find_node(lnode_root_t *root, int key)
{
    lnode_node_t *lnode;

    if (root == NULL){
        return NULL;
    }

    /* 遍历查询 */
    list_for_each_entry(lnode, &(root->root), lst) {
        if (lnode->key == key) {
            return lnode->data;
        }
    }

    return NULL;
}

/**
 * 插入节点
 * @root: 根节点指针
 * @key: 节点索引值
 * @data: 数据
 *
 * @return : 0--成功，其他失败
 */
int lnode_insert_node(lnode_root_t *root, int key, void *data)
{
    lnode_node_t *lnode;
    void *data_tmp;

    if ((root == NULL) || (data == NULL)) {
        return LNODE_RV_INPUT_ERR;
    }

    /* 判断节点是否已存在 */
    data_tmp = lnode_find_node(root, key);
    if (data_tmp != NULL) {
        return LNODE_RV_NODE_EXIST;
    }

    /* 节点内存申请 */
    lnode = kmalloc(sizeof(lnode_node_t), GFP_KERNEL);
    if (lnode == NULL) {
        return LNODE_RV_NOMEM;
    }

    /* 加入链表 */
    lnode->key = key;
    lnode->data = data;
    list_add_tail(&(lnode->lst), &(root->root));

    return LNODE_RV_OK;
}

/**
 * 初始化根节点
 * @root: 根节点指针
 *
 * @return : 0 成功，其他失败
 */
int lnode_init_root(lnode_root_t *root)
{
    if (root == NULL) {
        return LNODE_RV_INPUT_ERR;
    }

    INIT_LIST_HEAD(&(root->root));

    return LNODE_RV_OK;
}

/**
 * 释放链表
 * @root: 根节点指针
 *
 * @return : void
 */
void lnode_free_list(lnode_root_t *root)
{
    lnode_node_t *lnode, *lnode_next;

    if (root == NULL){
        return ;
    }

    /* 遍历删除链表 */
    list_for_each_entry_safe(lnode, lnode_next, &(root->root), lst) {
        if ( lnode->data ) {
            kfree(lnode->data);
            lnode->data = NULL;
            lnode->key = 0;
        }
        list_del(&lnode->lst);
        kfree(lnode);
        lnode = NULL;
    }

    return ;

}
