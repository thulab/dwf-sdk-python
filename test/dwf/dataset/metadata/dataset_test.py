# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.06.17
#
# Title: Tests for CRUD of dataset metadata
#
# Version 0.1
#

import unittest
from dwf.dataset.metadata.dataset_crud import DatasetCRUD
from dwf.common.config import test_config
from dwf.ormmodels import build_test_session, DataPattern, Datasource, Dataset, datetime
from test.runner import check_and_do_cases
from test.dwf.dataset.metadata import cases
from test.resources.data.dataset_data import _setup_test_dataset1
from test.resources.data.datasource_data import _setup_test_datasource_hdfs
from test.resources.data.datapattern_data import _setup_test_datapattern1, \
    _setup_test_datapattern2, _setup_test_datapattern3, _setup_test_datapattern4


class TestCRUD(unittest.TestCase):

    def prepare_data(self):
        self.to_be_deleted = []

        self._datapattern_instance1 = DataPattern(id=_setup_test_datapattern1.id,
                                                  name=_setup_test_datapattern1.name,
                                                  semantic=_setup_test_datapattern1.semantic)
        self._datapattern_instance2 = DataPattern(id=_setup_test_datapattern2.id,
                                                  name=_setup_test_datapattern2.name,
                                                  semantic=_setup_test_datapattern2.semantic)
        self._datapattern_instance3 = DataPattern(id=_setup_test_datapattern3.id,
                                                  name=_setup_test_datapattern3.name,
                                                  semantic=_setup_test_datapattern3.semantic)
        self._datapattern_instance4 = DataPattern(id=_setup_test_datapattern4.id,
                                                  name=_setup_test_datapattern4.name,
                                                  semantic=_setup_test_datapattern4.semantic)
        self.test_db_session.add(self._datapattern_instance1)
        self.test_db_session.add(self._datapattern_instance2)
        self.test_db_session.add(self._datapattern_instance3)
        self.test_db_session.add(self._datapattern_instance4)
        self.test_db_session.commit()
        self.to_be_deleted.append(self._datapattern_instance1)
        self.to_be_deleted.append(self._datapattern_instance2)
        self.to_be_deleted.append(self._datapattern_instance3)
        self.to_be_deleted.append(self._datapattern_instance4)

        self._datasource_instance = Datasource(id=_setup_test_datasource_hdfs.id,
                                               create_time=datetime.now(),
                                               name=_setup_test_datasource_hdfs.name,
                                               hostname=_setup_test_datasource_hdfs.hostname,
                                               port=_setup_test_datasource_hdfs.port,
                                               datasource_type=_setup_test_datasource_hdfs.datasource_type,
                                               username=_setup_test_datasource_hdfs.username,
                                               password=_setup_test_datasource_hdfs.passwd)
        self.test_db_session.add(self._datasource_instance)
        self.test_db_session.commit()
        self.to_be_deleted.append(self._datasource_instance)

        self._dataset_instance = Dataset(id=_setup_test_dataset1.id,
                                         name=_setup_test_dataset1.name,
                                         create_time=datetime.now(),
                                         pattern_id=_setup_test_datapattern1.id,
                                         datasource_id=_setup_test_datasource_hdfs.id,
                                         filter=_setup_test_dataset1.filter,
                                         description=_setup_test_dataset1.description)

        self.test_db_session.add(self._dataset_instance)
        self.test_db_session.commit()
        self.to_be_deleted.append(self._dataset_instance)

    def test_all_cases(self):
        self.test_db_session = build_test_session(test_config)
        self.cruder = DatasetCRUD(db_session=self.test_db_session)
        check_and_do_cases(self, cases)

    def _add_dataset(self, case_data):
        dataset_instance = case_data['dataset']

        dataset_id = self.cruder.add_dataset(dataset_instance.name, dataset_instance.pattern_id,
                                             dataset_instance.datasource_id,
                                             dataset_instance.filter, dataset_instance.description)

        dataset_db_instance = self.test_db_session.query(Dataset).get(dataset_id)
        self.to_be_deleted.append(dataset_db_instance)

        self.assertEqual(dataset_db_instance.name, dataset_instance.name)
        self.assertEqual(dataset_db_instance.pattern_id, dataset_instance.pattern_id)
        self.assertEqual(dataset_db_instance.datasource_id, dataset_instance.datasource_id)
        self.assertEqual(dataset_db_instance.filter, dataset_instance.filter)
        self.assertEqual(dataset_db_instance.description, dataset_instance.description)

    def _get_dataset(self, case_data):
        dataset_db_instance = self.cruder.get_dataset(self._dataset_instance.id)
        self.assertEqual(dataset_db_instance.name, self._dataset_instance.name)
        self.assertEqual(dataset_db_instance.pattern_id, self._dataset_instance.pattern_id)
        self.assertEqual(dataset_db_instance.datasource_id, self._dataset_instance.datasource_id)
        self.assertEqual(dataset_db_instance.filter, self._dataset_instance.filter)
        self.assertEqual(dataset_db_instance.description, self._dataset_instance.description)

    def _get_dataset_all(self, case_data):
        # TODO 参考算法的get_all测试
        dataset_db_instance_list = self.cruder.get_dataset_all()

    def _delete_dataset(self, case_data):
        self.cruder.delete_dataset(self._dataset_instance.id)
        self.test_db_session.commit()
        dataset_db_instance = self.test_db_session.query(Dataset).get(self._dataset_instance.id)
        self.assertIsNone(dataset_db_instance)


if __name__ == '__main__':
    unittest.main()
