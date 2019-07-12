# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.06.14
#
# Title: methods for metadata of dataset
#
# Version 0.1
#

from dwf.common.exception import *
from dwf.common.log import logger
from dwf.ormmodels import Dataset, datetime
from dwf.util.id import generate_primary_key


class DatasetCRUD:

    def __init__(self, db_session):
        self.db_session = db_session

    def add_dataset(self, name, datasource_id, subid=None, creator=None, owner=None, current_process=None,
                    last_modifier=None, data_file_format=None, default_filter_string=None, description=None,
                    filter=None, patterns=None, target_entity_class=None):
        """
        创建数据集元信息

        :param name: 数据集名称
        :param datasource_id: 数据源ID
        :param subid:
        :param creator:
        :param owner:
        :param current_process:
        :param last_modifier:
        :param data_file_format:
        :param default_filter_string:
        :param description:
        :param filter:
        :param patterns:
        :param target_entity_class:
        :return: 数据集ID
        """

        id = generate_primary_key('DSET')
        create_time = datetime.now()

        if creator is None:
            creator = 'admin'
        if owner is None:
            owner = 'admin'
        if last_modifier is None:
            last_modifier = 'admin'

        dataset = Dataset(id=id, subid=subid, creator=creator, owner=owner, current_process=current_process,
                          last_modifier=last_modifier, create_time=create_time, name=name,
                          data_file_format=data_file_format, datasource_id=datasource_id,
                          default_filter_string=default_filter_string, description=description, filter=filter,
                          patterns=patterns, target_entity_class=target_entity_class)
        self.db_session.add(dataset)
        self.db_session.commit()

        return id

    def get_dataset(self, dataset_id):
        """
        通过ID获取数据集元信息

        :param dataset_id: 数据集ID
        :return: 数据集元信息
        """

        dataset = self.db_session.query(Dataset).get(dataset_id)

        return dataset

    def get_all_dataset(self):
        """
        获取全部的数据集元信息

        :return: 数据集元信息列表
        """

        datasets = self.db_session.query(Dataset).all()

        return datasets

    def delete_dataset(self, dataset_id):
        """
        删除数据集元信息

        :param dataset_id: 数据集ID
        :return: 无
        """

        pending = self.db_session.query(Dataset).get(dataset_id)
        self.db_session.delete(pending)
        self.db_session.commit()

    def update_dataset(self, dataset_id, subid=None, creator=None, owner=None, current_process=None, last_modifier=None,
                       name=None, datasource_id=None, data_file_format=None, default_filter_string=None,
                       description=None, filter=None, patterns=None, target_entity_class=None):
        """
        更新数据集元信息

        :param dataset_id: 数据集ID
        :param subid:
        :param creator:
        :param owner:
        :param current_process:
        :param last_modifier:
        :param name: 数据集名称
        :param datasource_id: 数据源ID
        :param data_file_format:
        :param default_filter_string:
        :param description:
        :param filter:
        :param patterns:
        :param target_entity_class:
        :return: 无
        """

        if dataset_id is None:
            logger.error('缺少数据集ID')
            raise PARAM_LACK

        pending = self.db_session.query(Dataset).get(dataset_id)

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
        if datasource_id is not None:
            pending.datasource_id = datasource_id
        if data_file_format is not None:
            pending.data_file_format = data_file_format
        if default_filter_string is not None:
            pending.default_filter_string = default_filter_string
        if description is not None:
            pending.description = description
        if filter is not None:
            pending.filter = filter
        if patterns is not None:
            pending.patterns = patterns
        if target_entity_class is not None:
            pending.target_entity_class = target_entity_class

        pending.update_time = datetime.now()
        self.db_session.commit()
