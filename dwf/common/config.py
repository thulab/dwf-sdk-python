# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.06.15
#
# Title: Global Configuration
#
# Version 0.1
#

import configparser
import os

# don't add logger here to avoid cycled dependencies.

deploy_config = configparser.ConfigParser()
file_name = "dwf.conf"
if not os.path.exists(file_name):
    file_name = "../dwf.conf"
if not os.path.exists(file_name):
    file_name = "/etc/dwf/dwf.conf"
deploy_config.read(file_name)

test_config = configparser.ConfigParser()
file_name = "dwf.conf"
if not os.path.exists(file_name):
    file_name = "../dwf.conf"
if not os.path.exists(file_name):
    file_name = "/etc/dwf/dwf.conf"
test_config.read(file_name)
