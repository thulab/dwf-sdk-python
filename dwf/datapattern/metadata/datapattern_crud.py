# -*- coding:utf-8 -*-
#
# DataWay Algorithm SDK
# Initial Date: 2018.10.27
#
# Title: methods for metadata of pattern
#
# Version 1.0
#

from dwf.ormmodels import *
from dwf.common.log import logger
from dwf.common.exception import *
from dwf.util.id import generate_primary_key


class DataPatternCRUD:

    def __init__(self, db_session):
        self.db_session = db_session

    def add_datapattern(self, name, semantic=None):
        #    NO.A317
        #        Wait for jinying
        #    Args：
        #        package_name - The name of package.
        #        deployment_path - The path to deploy algorithm.
        #        upload_source - The upload source of package.
        #        requirement_list - Dependencies of algorithms in this package.
        #    Returns：
        #        package_id
        #        hyperparameter_config
        #    Exceptions:
        #        ADD_FAILURE
        id = generate_primary_key('DPAT')
        pattern = DataPattern(id=id, name=name, semantic=semantic)
        self.db_session.add(pattern)
        self.db_session.commit()
        return id

    def delete_datapattern(self, delete_pattern_id):
        #    NO.A320
        #        Wait for jinying
        #    Args：
        #        package_id: The id of package to be deleted.
        #    Returns：
        #        None.
        #    Exceptions:
        #        NON_EXISTING_PACKAGE - The given package_id does not exist.
        #        DELETE_FAILURE - The package cannot be deleted.
        pending = self.db_session.query(DataPattern).get(delete_pattern_id)
        self.db_session.delete(pending)
        self.db_session.commit()
        return

    def update_datapattern(self, delete_pattern_id, name=None, semantic=None):
        #    NO.A321
        #        Wait for jinying
        #    Args：
        #        package_name - The name of package.
        #        deployment_path - The path to deploy algorithm.
        #        upload_source - The upload source of package.
        #        requirement_list - Dependencies of algorithms in this package.
        #    Returns：
        #        package_id - The id of package.
        #        conda_id - The id of conda.
        #    Exceptions:
        #        UPDATE_FAILURE - Fail to add this package.
        pending = self.db_session.query(DataPattern).get(delete_pattern_id)
        if delete_pattern_id is None:
            logger.error('delete_pattern_id is needed')
            raise PARAM_LACK

        if name is not None:
            pending.plt_name = name
        if semantic is not None:
            pending.semantic = semantic
        self.db_session.commit()
        return pending

    def query_datapattern(self, delete_pattern_id):
        #    NO.A322
        #        Wait for jinying
        #    Args：
        #        package_id: The id of package.
        #    Returns：
        #        {
        #            package_name:"***",
        #            deployment_path:"***",
        #            upload_source:"***",
        #            requirement_list:"***"
        #        }
        pending = self.db_session.query(DataPattern).get(delete_pattern_id)
        if pending is None:
            logger.error('data pattern is not found')
            raise NON_EXISTING_DATA_PATTERN
        return pending
