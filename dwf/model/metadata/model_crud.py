# -*- coding:utf-8 -*-
#
# DataWay model SDK
# Initial Date: 2018.06.14
#
# Title: metadata APIs for Model
#
# Version 0.1
#

import traceback

from dwf.common.exception import *
from dwf.common.log import logger
from dwf.ormmodels import Model, datetime
from dwf.util.id import generate_primary_key


class ModelCRUD:

    def __init__(self, db_session):
        self.db_session = db_session

    def add_model(self, name, algorithm_id, input_data_patterns, output_data_patterns, subid=None, creator=None,
                  owner=None, current_process=None, last_modifier=None, description=None, model_path=None,
                  model_resource=None, usage=None):
        """
        创建模型元信息

        :param name: 模型名称
        :param algorithm_id: 算法ID
        :param input_data_patterns:
        :param output_data_patterns:
        :param subid:
        :param creator:
        :param owner:
        :param current_process:
        :param last_modifier:
        :param description:
        :param model_path:
        :param model_resource:
        :param usage:
        :return: 模型ID
        """

        check_name = self.db_session.query(Model).filter(Model.name == name)
        if check_name is not None:
            raise DUPLICATE_NAME

        id = generate_primary_key('MODE')
        create_time = datetime.now()

        if creator is None:
            creator = 'admin'
        if owner is None:
            owner = 'admin'
        if last_modifier is None:
            last_modifier = 'admin'

        try:
            model = Model(id=id, subid=subid, creator=creator, owner=owner, current_process=current_process,
                          last_modifier=last_modifier, create_time=create_time, name=name, algorithm_id=algorithm_id,
                          description=description, input_data_patterns=input_data_patterns,
                          output_data_patterns=output_data_patterns, model_path=model_path,
                          model_resource=model_resource,
                          usage=usage)

            self.db_session.add(model)
            self.db_session.commit()
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            self.db_session.rollback()
            raise ADD_FAILED

        return id

    def get_model(self, model_id):
        """
        根据ID查询模型元信息

        :param model_id: 模型ID
        :return: 模型元信息
        """

        try:
            pending = self.db_session.query(Model).get(model_id)
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            raise QUERY_FAILED

        return pending

    def get_all_model(self):
        """
        查询全部模型元信息

        :return: 模型元信息列表
        """

        try:
            model_list = self.db_session.query(Model).all()
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            raise QUERY_FAILED

        return model_list

    def delete_model(self, model_id):
        """
        删除模型元信息

        :param model_id: 模型ID
        :return: 无
        """

        try:
            pending = self.db_session.query(Model).get(model_id)
            self.db_session.delete(pending)
            self.db_session.commit()
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            raise DELETE_FAILED

    def update_model(self, model_id, subid=None, creator=None, owner=None, current_process=None, last_modifier=None,
                     name=None, algorithm_id=None, description=None, input_data_patterns=None,
                     output_data_patterns=None, model_path=None, model_resource=None, usage=None):
        """
        更新模型元信息

        :param model_id: 模型ID
        :param subid:
        :param creator:
        :param owner:
        :param current_process:
        :param last_modifier:
        :param name:
        :param algorithm_id:
        :param description:
        :param input_data_patterns:
        :param output_data_patterns:
        :param model_path:
        :param model_resource:
        :param usage:
        :return: 无
        """

        if model_id is None:
            logger.error('缺少模型ID')
            raise PARAM_LACK

        check_name = self.db_session.query(Model).filter(Model.name == name)
        if check_name is not None:
            raise DUPLICATE_NAME

        pending = self.db_session.query(Model).get(model_id)

        try:
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
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            self.db_session.rollback()
            raise UPDATE_FAILED
