#ifndef __DFD_CFG_LISTNODE_H__
#define __DFD_CFG_LISTNODE_H__

#include <linux/list.h>

/* 返回值 */
#define LNODE_RV_OK             (0)
#define LNODE_RV_INPUT_ERR      (-1)    /* 入参错误 */
#define LNODE_RV_NODE_EXIST     (-2)    /* 节点已存在 */
#define LNODE_RV_NOMEM          (-3)    /* 节点已存在 */

/* 根节点公共结构 */
typedef struct lnode_root_s {
    struct list_head root;
} lnode_root_t;

/* 节点结构 */
typedef struct lnode_node_s {
    struct list_head lst;

    int key;                    /* 节点搜索索引值 */
    void *data;                 /* 实际的数据指针 */
} lnode_node_t;

/**
 * 查找节点
 * @root: 根节点指针
 * @key: 节点索引值
 *
 * @return : 节点数据指针，NULL失败
 */
void *lnode_find_node(lnode_root_t *root, int key);

/**
 * 插入节点
 * @root: 根节点指针
 * @key: 节点索引值
 * @data: 数据
 *
 * @return : 0--成功，其他失败
 */
int lnode_insert_node(lnode_root_t *root, int key, void *data);

/**
 * 初始化根节点
 * @root: 根节点指针
 *
 * @return : 0 成功，其他失败
 */
int lnode_init_root(lnode_root_t *root);

/**
 * 释放链表
 * @root: 根节点指针
 *
 * @return : void
 */
void lnode_free_list(lnode_root_t *root);

#endif /* __DFD_CFG_LISTNODE_H__ */
