# -*- coding:utf-8 -*-
from dwf.ormmodels import *
from dwf.common.exception import *
from dwf.common.log import logger
from dwf.common.config import test_config
from dwf.util.id import generate_primary_key
from dwf.util.update import auto_update


class DataSourceCRUD:
    def __init__(self, db_session):
        self.db_session = db_session

    def add_datasource(self, name, database_name, server_ip=None, server_port=None, workbench_url=None, subid=None,
                       creator=None, owner=None, current_process=None, last_modifier=None, data_file_format=None,
                       datasource_type='LOCAL_FS', param1=None, password=None, username=None, description=None):
        '''
            Register a datasource in the metadata DB of DWF.
            Args:
                id -
                create_time -
                update_time -
                name - Name of DB.
                hostname - The hostname or IP of DB.
                port - The Port of DB.
                username - The username used for login.
                password - The password of DB.
                datasource_type -  The type of datasource, like HDFS.
                view_metadata_port -
                description - The description of datasource
            Returns:
                The ID of datasource.

        '''
        datasources = self.db_session.query(Datasource).filter(Datasource.name == name)
        if datasources.count() > 0:
            logger.error("The name of datasource already exists." % name)
            raise ILLEGAL_REPEATED_FILED

        id = generate_primary_key('DSOU')
        create_time = datetime.now()

        new_datasource = Datasource(id=id, subid=subid, creator=creator, owner=owner, current_process=current_process,
                                    last_modifier=last_modifier, create_time=create_time, name=name,
                                    database_name=database_name, data_file_format=data_file_format,
                                    datasource_type=datasource_type, description=description, param1=param1,
                                    password=password, server_ip=server_ip, server_port=server_port, username=username,
                                    workbench_url=workbench_url)
        self.db_session.add(new_datasource)
        self.db_session.commit()
        return new_datasource.id

    def get_datasource(self, datasource_id):
        '''
            Get a datasource by ID from the metadata DB of DWF.
            Args:
                datasource_id - The ID of datasource.
            Returns:
                The object of datasource.
        '''
        datasource = self.db_session.query(Datasource).get(datasource_id)
        return datasource

    def delete_datasource(self, datasource_id):
        '''
            Delete a datasource by ID from the metadata DB of DWF.
            Args:
                datasource_id - The ID of datasource.
        '''
        self.db_session.query(Datasource).filter(Datasource.id == datasource_id).delete()
        self.db_session.commit()

    def update_datasource(self, datasource_id, name=None, database_name=None, server_ip=None, server_port=None,
                          workbench_url=None, subid=None,
                          creator=None, owner=None, current_process=None, last_modifier=None, data_file_format=None,
                          datasource_type=None, param1=None, password=None, username=None, description=None):
        """

        :param datasource_id:
        :param name:
        :param database_name:
        :param server_ip:
        :param server_port:
        :param workbench_url:
        :param subid:
        :param creator:
        :param owner:
        :param current_process:
        :param last_modifier:
        :param data_file_format:
        :param datasource_type:
        :param param1:
        :param password:
        :param username:
        :param description:
        :return:
        """
        pending = self.db_session.query(Datasource).get(datasource_id)
        if datasource_id is None:
            logger.error('datasource_id is needed')
            raise PARAM_LACK

        args_dict = locals().pop('datasource_id')
        auto_update(pending, args_dict)
        """
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
        if param1 is not None:
            pending.param1 = param1
        if password is not None:
            pending.password = password
        if username is not None:
            pending.username = username
        if description is not None:
            pending.description = description
        """

        pending.update_time = datetime.now()
        self.db_session.commit()
        return pending


def test():
    cruder = DataSourceCRUD(build_test_session(test_config))
    cruder.add_datasource(name="test_datasource", database_name='/')


test()
