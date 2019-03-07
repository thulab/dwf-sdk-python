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
        model_id = self.cruder.add_model(subid=model_instance.subid, creator=model_instance.creator,
                                         owner=model_instance.owner, current_process=model_instance.current_process,
                                         last_modifier=model_instance.last_modifier, name=model_instance.name,
                                         algorithm_id=model_instance.algorithm_id,
                                         description=model_instance.description,
                                         input_data_patterns=model_instance.input_data_patterns,
                                         output_data_patterns=model_instance.output_data_patterns,
                                         model_path=model_instance.model_path,
                                         model_resource=model_instance.model_resource, usage=model_instance.usage)
        model_db_instance = self.test_db_session.query(Model).get(model_id)

        self.assertEqual(model_db_instance.subid, model_instance.subid)
        self.assertEqual(model_db_instance.creator, model_instance.creator)
        self.assertEqual(model_db_instance.owner, model_instance.owner)
        self.assertEqual(model_db_instance.current_process, model_instance.current_process)
        self.assertEqual(model_db_instance.last_modifier, model_instance.last_modifier)
        self.assertEqual(model_db_instance.name, model_instance.name)
        self.assertEqual(model_db_instance.description, model_instance.description)
        self.assertEqual(model_db_instance.input_data_patterns, model_instance.input_data_patterns)
        self.assertEqual(model_db_instance.output_data_patterns, model_instance.output_data_patterns)
        self.assertEqual(model_db_instance.model_path, model_instance.model_path)
        self.assertEqual(model_db_instance.model_resource, model_instance.model_resource)
        self.assertEqual(model_db_instance.usage, model_instance.usage)

        # self.test_db_session.delete(model_db_instance)
        self.test_db_session.commit()


if __name__ == '__main__':
    unittest.main()
