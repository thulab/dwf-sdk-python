# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.16
#
# Title: Logger
#
# Version 0.1
#

import logging as logger
from dwf.common.config import deploy_config

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = deploy_config.get('LOG', 'LOG_FILE')

if deploy_config.get('LOG', 'LOG_LEVEL') == 'debug':
    logger.basicConfig(filename=LOG_FILE, level=logger.DEBUG, format=LOG_FORMAT)
else:
    logger.basicConfig(filename=LOG_FILE, level=logger.INFO, format=LOG_FORMAT)
