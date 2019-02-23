# -*- coding:utf-8 -*-
#
# generate primary id
# Author: jinying(sherryying003@gmail.com)
# Initial Date: 2018.12.03
# Version 0.1
#
import uuid


def generate_primary_key(prefix):
    return prefix + str(uuid.uuid1()).replace('-', '')[0:28]


def generate_primary_key_without_prefix():
    return str(uuid.uuid1()).replace('-', '')
