# -*- coding:utf-8 -*-
#
# DataWay ORM Models
#
# Title: the define of sqlalchemy
#

from datetime import datetime
from sqlalchemy import Column, String, create_engine, Integer, DateTime, Boolean, ForeignKey, Table, Interval
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from dwf.common.config import *

Base = declarative_base()


class Datasource(Base):
    __tablename__ = 'plt_cus_datasource'

    id = Column(String, primary_key=True, name='plt_oid')
    subid = Column(String, name='plt_id')
    creator = Column(String, name='plt_creator')
    owner = Column(String, name='plt_owner')
    current_process = Column(String, name='plt_currentProcess')
    last_modifier = Column(String, name='plt_lastModifier')
    create_time = Column(DateTime, nullable=False, name='plt_createTime')
    update_time = Column(DateTime, name='plt_lastModifyTime')

    name = Column(String, unique=True, nullable=False, name='plt_dataSourceName')
    database_name = Column(String, name='plt_databaseName')
    data_file_format = Column(String, name='plt_dataFileFormat')
    datasource_type = Column(String, name='plt_dataSourceType')
    description = Column(String, name='plt_description')
    folder_depth = Column(String, name='plt_folderDepth')
    param1 = Column(String, name='plt_param1')
    password = Column(String, name='plt_password')
    server_ip = Column(String, name='plt_serverIp')
    server_port = Column(String, name='plt_serverPort')
    username = Column(String, name='plt_userName')
    workbench_url = Column(String, name='plt_workbenchUrl')

    def __repr__(self):
        return '<Datasource %r %r>' % (self.id, self.name)


class Dataset(Base):
    __tablename__ = 'plt_cus_dataset'

    id = Column(String, primary_key=True, name='plt_oid')
    subid = Column(String, name='plt_id')
    creator = Column(String, name='plt_creator')
    owner = Column(String, name='plt_owner')
    current_process = Column(String, name='plt_currentProcess')
    last_modifier = Column(String, name='plt_lastModifier')
    create_time = Column(DateTime, nullable=False, name='plt_createTime')
    update_time = Column(DateTime, name='plt_lastModifyTime')

    name = Column(String, unique=True, nullable=False, name='plt_dataSetName')
    data_file_format = Column(String, name='plt_dataFileFormat')
    datasource_id = Column(String, nullable=False, name='plt_dataSourceId')
    default_filter_string = Column(String, name='plt_defaultFilterString')
    description = Column(String, name='plt_description')
    filter = Column(String, name='plt_filterString')
    patterns = Column(String, name='plt_dataPattern4Learning')
    target_entity_class = Column(String, name='plt_targetEntityClass')

    def __repr__(self):
        return '<Dataset %r %r>' % (self.id, self.name)


class Algorithm(Base):
    __tablename__ = 'plt_cus_algorithm'

    id = Column(String, primary_key=True, name='pl_oid')
    subid = Column(String, name='plt_id')
    creator = Column(String, name='plt_creator')
    owner = Column(String, name='plt_owner')
    current_process = Column(String, name='plt_currentProcess')
    last_modifier = Column(String, name='plt_lastModifier')
    create_time = Column(DateTime, nullable=False, name='plt_createTime')
    update_ime = Column(DateTime, name='plt_lastModifyTime')
    name = Column(String, unique=True, nullable=False, name='plt_algorithmName')
    display_name = Column(String, name='plt_algorithmDisplayName')
    algorithm_type = Column(String, name='plt_algorithmType')
    description = Column(String, name='plt_description')
    alg_input_patterns = Column(String, name='plt_algInputPatterns')
    alg_output_patterns = Column(String, name='plt_algOutputPatterns')
    parameters = Column(String, name='plt_algParameters')
    entry_name = Column(String, name='plt_entryName')
    available = Column(Integer, nullable=False, name='plt_available')
    isbuiltin = Column(Integer, name='plt_isbuiltin')
    isdeleted = Column(Integer, name='plt_isdeleted')
    islearning = Column(Integer, name='plt_islearning')
    model_input_patterns = Column(String, name='plt_modelInputPatterns')
    model_output_patterns = Column(String, name='plt_modelOutputPatterns')
    package_id = Column(String, name='plt_packageID')
    prog_language = Column(String, name='plt_progLanguage')
    reference_count = Column(Integer, name='plt_referenceCount')
    runtime = Column(String, name='plt_runtime')
    tag = Column(String, name='plt_tag')

    def __repr__(self):
        return '<Algorithm %r %r>' % (self.id, self.name)


class Package(Base):
    __tablename__ = 'plt_cus_algorithmPackage'

    id = Column(String, primary_key=True, name='plt_oid')
    subid = Column(String, name='plt_id')
    creator = Column(String, name='plt_creator')
    owner = Column(String, name='plt_owner')
    current_process = Column(String, name='plt_currentProcess')
    last_modifier = Column(String, name='plt_lastModifier')
    create_time = Column(DateTime, nullable=False, name='plt_createTime')
    update_ime = Column(DateTime, name='plt_lastModifyTime')
    name = Column(String, unique=True, nullable=False, name='plt_packageName')
    description = Column(String, name='plt_packageDescription')
    package_source = Column(String, nullable=False, name='plt_packageSource')
    package_path = Column(String, nullable=False, name='plt_packagePath')

    def __repr__(self):
        return '<Package %r %r>' % (self.id, self.name)


class Model(Base):
    __tablename__ = 'plt_cus_model'

    id = Column(String, primary_key=True, name='plt_oid')
    subid = Column(String, name='plt_id')
    creator = Column(String, name='plt_creator')
    owner = Column(String, name='plt_owner')
    current_process = Column(String, name='plt_currentprocess')
    last_modifier = Column(String, name='plt_lastmodifier')
    create_time = Column(DateTime, nullable=False, name='plt_createtime')
    update_time = Column(DateTime, name='plt_lastmodifytime')
    algorithm_id = Column(String, name='plt_algorithmid')
    name = Column(String, unique=True, nullable=False, name='plt_modelname')
    description = Column(String, name='plt_modeldescription')
    input_data_patterns = Column(String, nullable=False, name='plt_modelinputpatterns')
    output_data_patterns = Column(String, nullable=False, name='plt_modeloutputpatterns')
    model_path = Column(String, nullable=False, name='plt_modelpath')
    model_resource = Column(String, name='plt_modelresource')
    usage = Column(String, name='plt_modelusage')

    def __repr__(self):
        return '<Model %r %r>' % (self.id, self.name)


def build_session(deploy_config):
    # the parameter configuration of connecting the PostgreSql database
    db_username = deploy_config.get('DB', 'DB_USER')
    db_password = deploy_config.get('DB', 'DB_PASSWORD')
    db_hostname = deploy_config.get('DB', 'DB_HOST')
    db_database = deploy_config.get('DB', 'DB_NAME')

    conn_url = 'postgresql://%s:%s@%s/%s' % (db_username, db_password, db_hostname, db_database)
    engine = create_engine(conn_url, echo=False, poolclass=NullPool, isolation_level="AUTOCOMMIT")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    return db_session


def build_test_session(test_config):
    # the parameter configuration of connecting the PostgreSql database
    db_username = test_config.get('TEST_DB', 'DB_USER')
    db_password = test_config.get('TEST_DB', 'DB_PASSWORD')
    db_hostname = test_config.get('TEST_DB', 'DB_HOST')
    db_database = test_config.get('TEST_DB', 'DB_NAME')

    test_conn_url = 'postgresql://%s:%s@%s/%s' % (db_username, db_password, db_hostname, db_database)
    test_engine = create_engine(test_conn_url, echo=False, poolclass=NullPool, isolation_level="AUTOCOMMIT")
    Base.metadata.create_all(test_engine)
    TEST_Session = sessionmaker(bind=test_engine)
    test_db_session = TEST_Session()
    return test_db_session


if __name__ == '__main__':
    build_session(deploy_config)
