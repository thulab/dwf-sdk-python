# -*- coding:utf-8 -*-
from dwf.ormmodels import Datasource, datetime
from dwf.util.id import generate_primary_key


class DataSourceCRUD:
    def __init__(self, db_session):
        self.db_session = db_session

    def add_datasource(self, name, subid=None, creator=None, owner=None, current_process=None, last_modifier=None,
                       data_file_format=None, database_name=None, datasource_type='LOCAL_FS', description=None,
                       folder_depth=None, paramone=None, password=None, server_ip=None, server_port=None, username=None,
                       workbench_url=None):
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
        id = generate_primary_key('DSOU')
        create_time = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')

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

    def get_all_datasource(self):
        '''
            Get all datasources from the metadata DB of DWF.
            Args:

            Returns:
                The list of datasources.
        '''
        datasource_list = self.db_session.query(Datasource).all()
        return datasource_list

    def delete_datasource(self, datasource_id):
        '''
            Delete a datasource by ID from the metadata DB of DWF.
            Args:
                datasource_id - The ID of datasource.
        '''
        self.db_session.query(Datasource).filter(Datasource.id == datasource_id).delete()
        self.db_session.commit()
        return True

    def update_datasource(self, datasource_id, name=None, subid=None, creator=None, owner=None, current_process=None,
                          last_modifier=None, data_file_format=None, database_name=None, datasource_type=None,
                          description=None, folder_depth=None, paramone=None, password=None, server_ip=None,
                          server_port=None, username=None, workbench_url=None):
        """

        :param datasource_id:
        :param name:
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
        :return:
        """
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
            folder_depth = folder_depth
        if paramone is not None:
            pending.paramone = paramone
        if password is not None:
            pending.password = password
        if username is not None:
            pending.username = username
        if description is not None:
            pending.description = description

        pending.update_time = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        self.db_session.commit()
        return pending
