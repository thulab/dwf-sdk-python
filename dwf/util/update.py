# -*- coding:utf-8 -*-
#
# auto update
# Author: kouzhi(lanxiaozhidoge@gmail.com)
# Initial Date: 2019.02.27
# Version 0.1
#


def auto_update(instance, args_dict):
    for attribute, value in args_dict:
        if value is not None:
            setattr(instance, attribute, value)
    return True
