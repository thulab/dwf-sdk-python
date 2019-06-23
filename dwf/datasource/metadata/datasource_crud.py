# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.06.14
#
# Title: methods for metadata of datasource
#
# Version 0.1
#

from dwf.common.exception import *
from dwf.common.log import logger
from dwf.ormmodels import Datasource, datetime
from dwf.util.id import generate_primary_key


class DataSourceCRUD:

    def __init__(self, db_session):
        self.db_session = db_session

    def add_datasource(self, name, subid=None, creator=None, owner=None, current_process=None, last_modifier=None,
                       data_file_format=None, database_name=None, datasource_type='LOCAL_FS', description=None,
                       folder_depth=None, paramone=None, password=None, server_ip=None, server_port=None, username=None,
                       workbench_url=None):
        """
        创建数据源元信息

        :param name: 数据源名称
        :param subid:
        :param creator:
        :param owner:
        :param current_process:
        :param last_modifier:
        :param data_file_format:
        :param database_name:
        :param datasource_type:
        :param description:
        :param folder_depth:
        :param paramone:
        :param password:
        :param server_ip:
        :param server_port:
        :param username:
        :param workbench_url:
        :return: 数据源ID
        """

        id = generate_primary_key('DSOU')
        create_time = datetime.now()

        if creator is None:
            creator = 'admin'
        if owner is None:
            owner = 'admin'
        if last_modifier is None:
            last_modifier = 'admin'
        if database_name is None:
            database_name = '/'
        if folder_depth is None:
            folder_depth = -1

        new_datasource = Datasource(id=id, subid=subid, creator=creator, owner=owner, current_process=current_process,
                                    last_modifier=last_modifier, create_time=create_time, name=name,
                                    database_name=database_name, data_file_format=data_file_format,
                                    datasource_type=datasource_type, description=description, folder_depth=folder_depth,
                                    paramone=paramone, password=password, server_ip=server_ip, server_port=server_port,
                                    username=username, workbench_url=workbench_url)
        self.db_session.add(new_datasource)
        self.db_session.commit()

        return id

    def get_datasource(self, datasource_id):
        """
        根据ID获取数据源元信息

        :param datasource_id: 数据源ID
        :return: 数据源元信息
        """

        datasource = self.db_session.query(Datasource).get(datasource_id)

        return datasource

    def get_all_datasource(self):
        """
        获取全部的数据源元信息

        :return: 数据源元信息列表
        """

        datasource_list = self.db_session.query(Datasource).all()

        return datasource_list

    def delete_datasource(self, datasource_id):
        """
        删除数据源元信息

        :param datasource_id: 数据源ID
        :return: 无
        """

        pending = self.db_session.query(Datasource).get(datasource_id)
        self.db_session.delete(pending)
        self.db_session.commit()

    def update_datasource(self, datasource_id, name=None, subid=None, creator=None, owner=None, current_process=None,
                          last_modifier=None, data_file_format=None, database_name=None, datasource_type=None,
                          description=None, folder_depth=None, paramone=None, password=None, server_ip=None,
                          server_port=None, username=None, workbench_url=None):
        """
        更新数据源元信息

        :param datasource_id: 数据源ID
        :param name: 数据源名称
        :param subid:
        :param creator:
        :param owner:
        :param current_process:
        :param last_modifier:
        :param data_file_format:
        :param database_name:
        :param datasource_type:
        :param description:
        :param folder_depth:
        :param paramone:
        :param password:
        :param server_ip:
        :param server_port:
        :param username:
        :param workbench_url:
        :return: 无
        """

        if datasource_id is None:
            logger.error('缺少数据源ID')
            raise PARAM_LACK

        pending = self.db_session.query(Datasource).get(datasource_id)

        if subid is not None:
            pending.subid = subid
        if creator is not None:
            pending.creator = creator
        if owner is not None:
            pending.owner = owner
        if current_process is not None:
            pending.current_process = current_process
        if last_modifier is not None:
            pending.last_modifier = last_modifier
        if name is not None:
            pending.name = name
        if database_name is not None:
            pending.database_name = database_name
        if server_ip is not None:
            pending.server_ip = server_ip
        if server_port is not None:
            pending.server_port = server_port
        if workbench_url is not None:
            pending.workbench_url = workbench_url
        if data_file_format is not None:
            pending.data_file_format = data_file_format
        if datasource_type is not None:
            pending.datasource_type = datasource_type
        if folder_depth is not None:
            pending.folder_depth = folder_depth
        if paramone is not None:
            pending.paramone = paramone
        if password is not None:
            pending.password = password
        if username is not None:
            pending.username = username
        if description is not None:
            pending.description = description

        pending.update_time = datetime.now()
        self.db_session.commit()
