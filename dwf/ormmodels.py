# -*- coding:utf-8 -*-
#
# DataWay ORM Models
# Initial Date: 2018.06.17
#
# Title: the define of sqlalchemy
#
# Version 0.1
from datetime import datetime
from sqlalchemy import Column, String, create_engine, Integer, DateTime, Boolean, ForeignKey, Table, Interval
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from dwf.common.config import *

Base = declarative_base()


class Datasource(Base):
    __tablename__ = 'plt_cus_datasource'

    id = Column(String, primary_key=True, name='plt_cus_oid')
    create_time = Column(DateTime, nullable=False, name='plt_cus_createTime')
    update_time = Column(DateTime, name='plt_cus_updateTime')
    name = Column(String, unique=True, nullable=False, name='plt_cus_dataSourceName')
    username = Column(String, name='plt_cus_userName')
    password = Column(String, name='plt_cus_password')
    datasource_type = Column(String, nullable=False, name='plt_cus_dataSourceType')
    view_metadata_port = Column(String, name='plt_cus_viewMetadataPort')
    description = Column(String, name='plt_cus_description')
    LOCAL_TYPE = 'LOCAL'
    HDFS_TYPE = 'HDFS'

    database_name = Column(String, name='plt_cus_databaseName')
    data_file_format = Column(String, name='plt_cus_dataFileFormat')
    folder_depth = Column(String, name='plt_cus_folderDepth')
    param1 = Column(String, name='plt_cus_param1')
    server_ip = Column(String, nullable=False, name='plt_cus_serverIp')
    server_port = Column(String, nullable=False, name='plt_cus_serverPort')
    workbench_url = Column(String, name='plt_cus_workbenchUrl')

    def __repr__(self):
        return '<Datasource %r %r>' % (self.id, self.name)


class Dataset(Base):
    __tablename__ = 'plt_cus_dataset'

    id = Column(String, primary_key=True, name='plt_cus_oid')
    name = Column(String, unique=True, nullable=False, name='plt_cus_dataSetName')
    create_time = Column(DateTime, nullable=False, name='plt_cus_createTime')
    update_ime = Column(DateTime, name='plt_cus_updateTime')
    patterns = Column(String, nullable=False, name='plt_cus_dataPattern4Learning')
    datasource_id = Column(String, nullable=False, name='plt_cus_dataSourceId')
    filter = Column(String, nullable=False, name='plt_cus_filterString')
    description = Column(String, name='plt_cus_description')

    data_file_format = Column(String, name='plt_cus_dataFileFormat')
    default_filter_string = Column(String, name='plt_cus_defaultFilterString')
    target_entity_class = Column(String, name='plt_cus_targetEntityClass')


    def __repr__(self):
        return '<Dataset %r %r>' % (self.id, self.name)


class DataPattern(Base):
    __tablename__ = 'datapattern'

    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    data_type = Column(String)
    organization = Column(String)
    organization_parameter = Column(String)
    semantic = Column(String)

    def __repr__(self):
        return '<DataPattern %r %r>' % (self.id, self.name)


class Algorithm(Base):
    __tablename__ = 'plt_cus_algorithm'

    id = Column(String, primary_key=True, name='plt_cus_oid')
    algInputPatterns = Column(String, name='plt_cus_algInputPatterns')
    displayName = Column(String, name='plt_cus_algorithmDisplayName')
    name = Column(String, unique=True, nullable=False, name='plt_cus_algorithmName')
    type = Column(String, name='plt_cus_algorithmType')
    algOutputPatterns = Column(String, name='plt_cus_algOutputPatterns')
    parameters = Column(String, name='plt_cus_algParameters')
    available = Column(Integer, nullable=False, name='plt_cus_available')
    description = Column(String, name='plt_cus_description')
    entryName = Column(String, name='plt_cus_entryName')
    isbuiltin = Column(Boolean, name='plt_cus_isbuiltin')
    isdeleted = Column(Integer, name='plt_cus_isdeleted')
    islearning = Column(String, name='plt_cus_islearning')
    modelInputPatterns = Column(String, name='plt_cus_modelInputPatterns')
    modelOutputPatterns = Column(String, name='plt_cus_modelOutputPatterns')
    package_id = Column(String, name='plt_cus_packageID')
    progLanguage = Column(String, name='plt_cus_progLanguage')
    referenceCount = Column(Integer, name='plt_cus_referenceCount')
    runtime = Column(String, name='plt_cus_runtime')
    tag = Column(String, name='plt_cus_tag')

    def __repr__(self):
        return '<Algorithm %r %r>' % (self.id, self.name)


class Package(Base):
    __tablename__ = 'plt_cus_package'

    id = Column(String, primary_key=True, name='plt_cus_oid')
    name = Column(String, unique=True, nullable=False, name='plt_cus_packageName')
    description = Column(String, name='plt_cus_packageDescription')
    package_source = Column(String, nullable=False, name='plt_cus_packageSource')
    package_path = Column(String, nullable=False, name='plt_cus_packagePath')

    def __repr__(self):
        return '<Package %r %r>' % (self.id, self.name)

class Model(Base):
    __tablename__ = 'model'

    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    parallelism = Column(Integer)
    description = Column(String)
    help = Column(String)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    model_path = Column(String, nullable=False)
    log_path = Column(String)
    input_data_patterns = relationship("ModelInputDataPatterns", back_populates='model', lazy='dynamic')
    output_data_patterns = relationship("ModelOutputDataPatterns", back_populates='model', lazy='dynamic')

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
