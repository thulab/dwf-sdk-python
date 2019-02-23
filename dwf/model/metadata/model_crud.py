# -*- coding:utf-8 -*-
#
# DataWay model SDK
# Initial Date: 2018.06.14
#
# Title: metadata APIs for Model
#
# Version 0.1
#

from dwf.ormmodels import Model, datetime
from dwf.common.log import logger
from dwf.common.exception import *
from dwf.util.id import generate_primary_key


class ModelCRUD:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_model(self, model_id):
        # query a model
        pending = self.db_session.query(Model).get(model_id)
        return pending

    def get_all_model(self):
        # query all models
        models = self.db_session.query(Model).all()
        return models

    def add_model(self, name, model_path, parallelism=None, description=None, help=None, log_path=None):
        # add a model
        id = generate_primary_key('SERV')
        create_time = datetime.now()

        model = Model(id=id, name=name, parallelism=parallelism, description=description, help=help,
                      create_time=create_time,
                      model_path=model_path, log_path=log_path)
        self.db_session.add(model)
        self.db_session.commit()
        return id

    def delete_model(self, model_id):
        # delete a model
        pending = self.db_session.query(Model).get(model_id)
        self.db_session.delete(pending)
        self.db_session.commit()
        return

    def modify_model(self, model_id, name=None, parallelism=None, description=None, help=None, model_path=None,
                     log_path=None):
        # modify a model with
        pending = self.db_session.query(Model).get(model_id)
        if model_id is None:
            logger.error('model_id is needed')
            raise PARAM_LACK

        if name is not None:
            pending.name = name
        if description is not None:
            pending.description = description
        if parallelism is not None:
            pending.parallelism = parallelism
        if help is not None:
            pending.help = help
        if model_path is not None:
            pending.model_path = model_path
        if log_path is not None:
            pending.log_path = log_path

        pending.update_time = datetime.now()
        self.db_session.commit()
        return pending
