# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.10.30
#
# Title: Tests for CRUD of datapattern metadata
#
# Version 1.0


import unittest

from dwf.common.config import test_config
from dwf.datapattern.metadata.datapattern_crud import DataPatternCRUD
from dwf.ormmodels import build_test_session, DataPattern

from test.dwf.datapattern.metadata import cases
from test.runner import check_and_do_cases


class TestCRUD(unittest.TestCase):

    def test_all_cases(self):
        self.test_db_session = build_test_session(test_config)
        self.cruder = DataPatternCRUD(db_session=self.test_db_session)
        check_and_do_cases(self, cases)

    def prepare_data(self):
        self.to_be_deleted = []

    def _add_datapattern(self, case_data):
        datapattern_instance = case_data['datapattern']
        datapattern_id = self.cruder.add_datapattern(name=datapattern_instance.name, semantic=datapattern_instance.semantic)
        datapattern_db_instance = self.test_db_session.query(DataPattern).get(datapattern_id)
        self.to_be_deleted.append(datapattern_db_instance)

        self.assertEqual(datapattern_db_instance.name, datapattern_instance.name)
        self.assertEqual(datapattern_db_instance.semantic, datapattern_instance.semantic)


if __name__ == '__main__':
    unittest.main()
