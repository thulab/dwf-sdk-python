# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.06.17
#
# Title: Tests for CRUD of datasource metadata
#
# Version 1.0

import unittest
from dwf.datasource.metadata.datasource_crud import DataSourceCRUD
from dwf.common.config import test_config
from dwf.ormmodels import build_test_session, Datasource, datetime

from test.dwf.datasource.metadata import cases
from test.runner import check_and_do_cases

class TestCRUD(unittest.TestCase):

    def prepare_data(self):
        self.to_be_deleted = []

    def test_all_cases(self):
        self.test_db_session = build_test_session(test_config)
        self.cruder = DataSourceCRUD(db_session=self.test_db_session)
        check_and_do_cases(self, cases)

    def _add_datasource(self, case_data):
        datasource_instance = case_data['datasource']
        self._datasource_instance = self.test_db_session.query(Datasource).filter_by(name=datasource_instance.name).first()
        if self._datasource_instance is not None:
            self.test_db_session.delete(self._datasource_instance)
            self.test_db_session.commit()
        datasource_id = self.cruder.add_datasource(datasource_instance.name, datasource_instance.hostname,
                                       datasource_instance.port, datasource_instance.datasource_type,
                                       datasource_instance.username, datasource_instance.passwd, )
        datasource_db_instance = self.test_db_session.query(Datasource).get(datasource_id)

        self.assertEqual(datasource_db_instance.name, datasource_instance.name)
        self.assertEqual(datasource_db_instance.hostname, datasource_instance.hostname)
        self.assertEqual(datasource_db_instance.port, datasource_instance.port)
        self.assertEqual(datasource_db_instance.password, datasource_instance.passwd)

        self.test_db_session.delete(datasource_db_instance)
        self.test_db_session.commit()

    def _get_datasource(self, case_data):
        datasource_instance = case_data['datasource']
        _datasource_instance = Datasource(id=datasource_instance.id, create_time=datetime.now(),
                                          name=datasource_instance.name, hostname=datasource_instance.hostname,
                                          port=datasource_instance.port,
                                          datasource_type=datasource_instance.datasource_type,
                                          username=datasource_instance.username, password=datasource_instance.passwd)
        self.test_db_session.add(_datasource_instance)
        self.test_db_session.commit()

        datasource_db_instance = self.cruder.get_datasource(datasource_instance.id)

        self.assertEqual(datasource_db_instance.name, datasource_instance.name)
        self.assertEqual(datasource_db_instance.hostname, datasource_instance.hostname)
        self.assertEqual(datasource_db_instance.port, datasource_instance.port)
        self.assertEqual(datasource_db_instance.password, datasource_instance.passwd)

        self.test_db_session.delete(datasource_db_instance)
        self.test_db_session.commit()

    def _delete_datasource(self, case_data):
        datasource_instance = case_data['datasource']
        _datasource_instance = Datasource(id=datasource_instance.id, create_time=datetime.now(),
                                          name=datasource_instance.name, hostname=datasource_instance.hostname,
                                          port=datasource_instance.port,
                                          datasource_type=datasource_instance.datasource_type,
                                          username=datasource_instance.username, password=datasource_instance.passwd)
        self.test_db_session.add(_datasource_instance)
        self.test_db_session.commit()

        self.cruder.delete_datasource(datasource_instance.id)
        datasource_db_instance = self.test_db_session.query(Datasource).get(datasource_instance.id)
        self.assertIsNone(datasource_db_instance)


if __name__ == '__main__':
    unittest.main()
