currentdir = $(shell pwd)
CUSTOMS_DIRS = $(currentdir)/common_custom/common_factest

MODULE_DIRS := b6510-32cq
MODULE_DIRS += b6920-32qc-e

export CUSTOMS_DIRS MODULE_DIRS
