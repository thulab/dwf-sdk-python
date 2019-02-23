# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.10.30
#
# Title: Tests for model
#
# Version 1.0
#


import unittest
from dwf.model.metadata.model_crud import ModelCRUD
from test.dwf.model.metadata import cases
from dwf.common.config import test_config
from dwf.ormmodels import build_test_session, Model

from test.runner import check_and_do_cases


class TestCRUD(unittest.TestCase):

    def prepare_data(self):
        self.to_be_deleted = []

    def test_all_cases(self):
        self.test_db_session = build_test_session(test_config)
        self.cruder = ModelCRUD(db_session=self.test_db_session)
        check_and_do_cases(self, cases)

    def _add_model(self, case_data):
        model_instance = case_data['model']
        self._model_instance = self.test_db_session.query(Model).filter_by(
            name=model_instance.name).first()
        if self._model_instance is not None:
            self.test_db_session.delete(self._model_instance)
            self.test_db_session.commit()
        model_id = self.cruder.add_model(name=model_instance.name,model_path=model_instance.model_path,
                             description=model_instance.description,help = model_instance.help,
                             log_path=model_instance.log_path)
        model_db_instance = self.test_db_session.query(Model).get(model_id)

        self.assertEqual(model_db_instance.name, model_instance.name)
        self.assertEqual(model_db_instance.model_path, model_instance.model_path)
        self.assertEqual(model_db_instance.description, model_instance.description)
        self.assertEqual(model_db_instance.help, model_instance.help)
        self.assertEqual(model_db_instance.log_path, model_instance.log_path)

        self.test_db_session.delete(model_db_instance)
        self.test_db_session.commit()


if __name__ == '__main__':
    unittest.main()
