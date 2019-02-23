# -*- coding:utf-8 -*-
#
# DataWay SDK
# Initial Date: 2018.10.30
#
# Title: methods for metadata of data pattern
#
# Version 1.0
#

from dwf.ormmodels import Package, datetime
from dwf.common.log import logger
from dwf.common.exception import *
from dwf.util.id import generate_primary_key


class PackageCRUD:
    def __init__(self, db_session):
        self.db_session = db_session

    def add_package(self, name, package_source, package_path, description=None):
        #    NO.A317
        #        Add one new package, create a new conda or find an existed conda according to requirement_list.
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

        id = generate_primary_key('PACK')
        create_time = datetime.now()
        package = Package(id=id, create_time=create_time, name=name, package_source=package_source,
                          package_path=package_path, description=description)
        self.db_session.add(package)
        self.db_session.commit()
        return id

    def delete_package(self, package_id):
        #    NO.A320
        #        Delete one package.
        #    Args：
        #        package_id: The id of package to be deleted.
        #    Returns：
        #        None.
        #    Exceptions:
        #        NON_EXISTING_PACKAGE - The given package_id does not exist.
        #        DELETE_FAILURE - The package cannot be deleted.
        self.db_session.query(Package).filter(Package.id == package_id).delete()
        self.db_session.commit()

    def update_package(self, package_id, name=None, package_source=None, package_path=None, description=None):
        #    NO.A321
        #        Update one package.
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
        pending = self.db_session.query(Package).get(package_id)
        if package_id is None:
            logger.error('package_id is needed')
            raise PARAM_LACK

        if name is not None:
            pending.plt_name = name
        if package_source is not None:
            pending.package_source = package_source
        if package_path is not None:
            pending.package_path = package_path
        if description is not None:
            pending.update_time = description

        pending.create_time = datetime.now()
        self.db_session.commit()
        return pending

    def query_package(self, package_id):
        #    NO.A322
        #        Query package configs.
        #    Args：
        #        package_id: The id of package.
        #    Returns：
        #        {
        #            package_name:"***",
        #            deployment_path:"***",
        #            upload_source:"***",
        #            requirement_list:"***"
        #        }
        package = self.db_session.query(Package).get(package_id)
        return package
