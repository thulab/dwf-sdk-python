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

    def add_model(self, name, algorithm_id, input_data_patterns, output_data_patterns, subid=None, creator=None,
                  owner=None,
                  current_process=None, last_modifier=None, description=None, model_path=None, model_resource=None,
                  usage=None):
        # add a model
        id = generate_primary_key('MODE')
        create_time = datetime.now()

        model = Model(id=id, subid=subid, creator=creator, owner=owner, current_process=current_process,
                      last_modifier=last_modifier, create_time=create_time, name=name, algorithm_id=algorithm_id,
                      description=description, input_data_patterns=input_data_patterns,
                      output_data_patterns=output_data_patterns, model_path=model_path, model_resource=model_resource,
                      usage=usage)

        self.db_session.add(model)
        self.db_session.commit()
        return id

    def delete_model(self, model_id):
        # delete a model
        pending = self.db_session.query(Model).get(model_id)
        self.db_session.delete(pending)
        self.db_session.commit()
        return

    def update_model(self, model_id, subid=None, creator=None, owner=None, current_process=None, last_modifier=None,
                     name=None, algorithm_id=None, description=None, input_data_patterns=None,
                     output_data_patterns=None, model_path=None, model_resource=None, usage=None):
        # update a model with param
        pending = self.db_session.query(Model).get(model_id)
        if model_id is None:
            logger.error('model_id is needed')
            raise PARAM_LACK

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
        if algorithm_id is not None:
            pending.algorithm_id = algorithm_id
        if description is not None:
            pending.description = description
        if input_data_patterns is not None:
            pending.input_data_patterns = input_data_patterns
        if output_data_patterns is not None:
            pending.output_data_patterns = output_data_patterns
        if model_path is not None:
            pending.model_path = model_path
        if model_resource is not None:
            pending.model_resource = model_resource
        if usage is not None:
            pending.usage = usage

        pending.update_time = datetime.now()
        self.db_session.commit()
        return pending
