# -*- coding:utf-8 -*-
#
# auto update
# Author: kouzhi(lanxiaozhidoge@gmail.com)
# Initial Date: 2019.02.27
# Version 0.1
#
from dwf.common.log import logger
from dwf.common.exception import *


def auto_update(instance, args_dict, check_list):
    for attribute, value in args_dict.items():
        if attribute in check_list:
            if value is None:
                logger.error('{} is needed'.format(attribute))
                raise PARAM_LACK
        if value is not None:
            setattr(instance, attribute, value)
    return True
