# -*- coding:utf-8 -*-
from dwf.ormmodels import *
from dwf.common.exception import *
from dwf.common.log import logger
from dwf.util.id import generate_primary_key


class DataSourceCRUD:
    def __init__(self, db_session):
        self.db_session = db_session

    def add_datasource(self, name, hostname, port, datasource_type, username=None, password=None,
                       view_metadata_port=None, description=None):
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
        id = generate_primary_key('DSOU'),
        create_time = datetime.now()

        new_datasource = Datasource(id=id, create_time=create_time, name=name, hostname=hostname, port=port,
                                    username=username, password=password, datasource_type=datasource_type,
                                    view_metadata_port=view_metadata_port, description=description)
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
