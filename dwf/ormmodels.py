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

    id = Column(String, primary_key=True)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    name = Column(String, unique=True, nullable=False)
    hostname = Column(String, nullable=False)
    port = Column(String, nullable=False)
    username = Column(String)
    password = Column(String)
    datasource_type = Column(String, nullable=False)
    view_metadata_port = Column(String)
    description = Column(String)

    def __repr__(self):
        return '<Datasource %r %r>' % (self.id, self.name)


class Dataset(Base):
    __tablename__ = 'plt_cus_dataset'

    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    pattern_id = Column(String, ForeignKey('plt_cus_datapattern.id'), nullable=False)
    pattern = relationship("DataPattern")
    datasource_id = Column(String, ForeignKey('plt_cus_datasource.id'), nullable=False)
    filter = Column(String, nullable=False)
    description = Column(String)

    def __repr__(self):
        return '<Dataset %r %r>' % (self.id, self.name)


class DataPattern(Base):
    __tablename__ = 'plt_cus_datapattern'

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

    id = Column(String, primary_key=True, name='plt_oid')
    subid = Column(String, name='plt_id')
    creator = Column(String, name='plt_creator')
    owner = Column(String, name='plt_owner')
    current_process = Column(String, name='plt_currentprocess')
    last_modifier = Column(String, name='plt_lastmodifier')
    create_time = Column(DateTime, nullable=False, name='plt_createtime')
    update_ime = Column(DateTime, name='plt_lastmodifytime')
    name = Column(String, unique=True, nullable=False, name='plt_algorithmname')
    display_name = Column(String, name='plt_algorithmdisplayname')
    algorithm_type = Column(String, name='plt_algorithmtype')
    description = Column(String, name='plt_description')
    alg_input_patterns = Column(String, name='plt_alginputpatterns')
    alg_output_patterns = Column(String, name='plt_algoutputpatterns')
    parameters = Column(String, name='plt_algparameters')
    entry_name = Column(String, name='plt_entryname')
    available = Column(Integer, nullable=False, name='plt_available')
    isbuiltin = Column(Integer, name='plt_isbuiltin')
    isdeleted = Column(Integer, name='plt_isdeleted')
    islearning = Column(Integer, name='plt_islearning')
    model_input_patterns = Column(String, name='plt_modelinputpatterns')
    model_output_patterns = Column(String, name='plt_modeloutputpatterns')
    package_id = Column(String, name='plt_packageid')
    prog_language = Column(String, name='plt_proglanguage')
    reference_count = Column(Integer, name='plt_referencecount')
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
    current_process = Column(String, name='plt_currentprocess')
    last_modifier = Column(String, name='plt_lastmodifier')
    create_time = Column(DateTime, nullable=False, name='plt_createtime')
    update_ime = Column(DateTime, name='plt_lastmodifytime')
    name = Column(String, unique=True, nullable=False, name='plt_packagename')
    description = Column(String, name='plt_packagedescription')
    package_source = Column(String, nullable=False, name='plt_packagesource')
    package_path = Column(String, nullable=False, name='plt_packagepath')

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
