# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.06.17
#
# Title: Tests for CRUD of algorithm metadata
#
# Version 1.0
#

import unittest

from dwf.algorithm.metadata.algorithm_crud import AlgorithmCRUD
from dwf.model.metadata.model_crud import *
from dwf.ormmodels import build_test_session, DataPattern, Package, \
    Algorithm, AlgorithmInputDataPatterns, AlgorithmOutputDataPatterns, \
    ModelInputDataPatterns, ModelOutputDataPatterns
from dwf.common.config import test_config

from test.dwf.algorithm.metadata import cases
from test.runner import check_and_do_cases
from test.resources.data.algorithm_data import _setup_test_algorithm1, _setup_test_algorithm2
from test.resources.data.package_data import _setup_test_package1
from test.resources.data.datapattern_data import _setup_test_datapattern1, \
    _setup_test_datapattern2, _setup_test_datapattern3, _setup_test_datapattern4


class TestCRUD(unittest.TestCase):

    def prepare_data(self):
        self.to_be_deleted = []

        self._package_instance = Package(id=_setup_test_package1.id,
                                         name=_setup_test_package1.name,
                                         create_time=_setup_test_package1.create_time,
                                         package_source=_setup_test_package1.package_source,
                                         package_path=_setup_test_package1.package_path,
                                         description=_setup_test_package1.description)
        self.test_db_session.add(self._package_instance)
        self.test_db_session.commit()
        self.to_be_deleted.append(self._package_instance)

        self._datapattern_instance1 = DataPattern(id=_setup_test_datapattern1.id, name=_setup_test_datapattern1.name,
                                                  semantic=_setup_test_datapattern1.semantic)
        self._datapattern_instance2 = DataPattern(id=_setup_test_datapattern2.id, name=_setup_test_datapattern2.name,
                                                  semantic=_setup_test_datapattern2.semantic)
        self._datapattern_instance3 = DataPattern(id=_setup_test_datapattern3.id, name=_setup_test_datapattern3.name,
                                                  semantic=_setup_test_datapattern3.semantic)
        self._datapattern_instance4 = DataPattern(id=_setup_test_datapattern4.id, name=_setup_test_datapattern4.name,
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

        self._algorithm_instance1 = Algorithm(id=_setup_test_algorithm1.id,
                                              create_time=datetime.now(),
                                              name=_setup_test_algorithm1.name,
                                              main_file_name=_setup_test_algorithm1.main_file_name,
                                              hyperparameter_config=_setup_test_algorithm1.hyperparameter_config,
                                              learning=_setup_test_algorithm1.learning,
                                              available=1,
                                              package_id=_setup_test_algorithm1.package_id)
        self._algorithm_instance2 = Algorithm(id=_setup_test_algorithm2.id,
                                              create_time=datetime.now(),
                                              name=_setup_test_algorithm2.name,
                                              main_file_name=_setup_test_algorithm2.main_file_name,
                                              hyperparameter_config=_setup_test_algorithm2.hyperparameter_config,
                                              learning=_setup_test_algorithm2.learning,
                                              available=1,
                                              package_id=_setup_test_algorithm2.package_id)
        self.algorithm_instance_list = [_setup_test_algorithm1, _setup_test_algorithm2]
        self.test_db_session.add(self._algorithm_instance1)
        self.test_db_session.add(self._algorithm_instance2)
        self.test_db_session.commit()
        self.to_be_deleted.append(self._algorithm_instance1)
        self.to_be_deleted.append(self._algorithm_instance2)

    def test_all_cases(self):
        self.test_db_session = build_test_session(test_config)
        self.cruder = AlgorithmCRUD(db_session=self.test_db_session)
        check_and_do_cases(self, cases)

    def _add_algorithm(self, case_data):
        algorithm_instance = case_data['algorithm']

        algorithm_id = self.cruder.add_algorithm(
            name=algorithm_instance.name,
            main_file_name=algorithm_instance.main_file_name,
            hyperparameter_config=algorithm_instance.hyperparameter_config,
            train_input_pattern=algorithm_instance.train_input_pattern,
            train_output_pattern=algorithm_instance.train_output_pattern,
            model_input_pattern=algorithm_instance.model_input_pattern,
            model_output_pattern=algorithm_instance.model_output_pattern,
            learning=algorithm_instance.learning,
            package_id=algorithm_instance.package_id)

        model_name = algorithm_instance.name + ' example model'
        example_model = self.test_db_session.query(Model).filter(Model.name == model_name).first()
        self.to_be_deleted.append(example_model)
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)
        self.to_be_deleted.append(algorithm_db_instance)

        input_data_pattern_db_instances = self.test_db_session.query(AlgorithmInputDataPatterns). \
            filter(AlgorithmInputDataPatterns.algorithm_id == algorithm_id).all()
        output_data_pattern_db_instances = self.test_db_session.query(AlgorithmOutputDataPatterns). \
            filter(AlgorithmOutputDataPatterns.algorithm_id == algorithm_id).all()
        for input_data_pattern_db_instance in input_data_pattern_db_instances:
            self.to_be_deleted.append(input_data_pattern_db_instance)
        for output_data_pattern_db_instance in output_data_pattern_db_instances:
            self.to_be_deleted.append(output_data_pattern_db_instance)
        model_input_data_pattern_db_instances = self.test_db_session.query(ModelInputDataPatterns). \
            filter(ModelInputDataPatterns.model_id == example_model.id).all()
        model_output_data_pattern_db_instances = self.test_db_session.query(ModelOutputDataPatterns). \
            filter(ModelOutputDataPatterns.model_id == example_model.id).all()
        for model_input_data_pattern_db_instance in model_input_data_pattern_db_instances:
            self.to_be_deleted.append(model_input_data_pattern_db_instance)
        for model_output_data_pattern_db_instance in model_output_data_pattern_db_instances:
            self.to_be_deleted.append(model_output_data_pattern_db_instance)

        self.assertEqual(algorithm_db_instance.name, algorithm_instance.name)
        self.assertEqual(algorithm_db_instance.main_file_name, algorithm_instance.main_file_name)
        self.assertEqual(algorithm_db_instance.hyperparameter_config, algorithm_instance.hyperparameter_config)
        self.assertEqual(algorithm_db_instance.learning, algorithm_instance.learning)
        self.assertEqual(algorithm_db_instance.package_id, algorithm_instance.package_id)
        self.assertIsNotNone(algorithm_db_instance.example_model_id)
        for input_data_pattern_db_instance in input_data_pattern_db_instances:
            self.assertIn(input_data_pattern_db_instance.pattern_id, algorithm_instance.train_input_pattern)
        for output_data_pattern_db_instance in output_data_pattern_db_instances:
            self.assertIn(output_data_pattern_db_instance.pattern_id, algorithm_instance.train_output_pattern)
        for model_input_data_pattern_db_instance in model_input_data_pattern_db_instances:
            self.assertIn(model_input_data_pattern_db_instance, example_model.input_data_patterns)
        for model_output_data_pattern_db_instance in model_output_data_pattern_db_instances:
            self.assertIn(model_output_data_pattern_db_instance, example_model.output_data_patterns)

    def _add_algorithm_not_learning(self, case_data):
        algorithm_instance = case_data['algorithm2']

        algorithm_id = self.cruder.add_algorithm(name=algorithm_instance.name,
                                                 main_file_name=algorithm_instance.main_file_name,
                                                 hyperparameter_config=algorithm_instance.hyperparameter_config,
                                                 train_input_pattern=algorithm_instance.train_input_pattern,
                                                 train_output_pattern=algorithm_instance.train_output_pattern,
                                                 model_input_pattern=algorithm_instance.model_input_pattern,
                                                 model_output_pattern=algorithm_instance.model_output_pattern,
                                                 learning=algorithm_instance.learning,
                                                 package_id=algorithm_instance.package_id)

        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)
        self.to_be_deleted.append(algorithm_db_instance)
        input_data_pattern_db_instances = self.test_db_session.query(AlgorithmInputDataPatterns). \
            filter(AlgorithmInputDataPatterns.algorithm_id == algorithm_id).all()
        output_data_pattern_db_instances = self.test_db_session.query(AlgorithmOutputDataPatterns). \
            filter(AlgorithmOutputDataPatterns.algorithm_id == algorithm_id).all()
        for input_data_pattern_db_instance in input_data_pattern_db_instances:
            self.to_be_deleted.append(input_data_pattern_db_instance)
        for output_data_pattern_db_instance in output_data_pattern_db_instances:
            self.to_be_deleted.append(output_data_pattern_db_instance)

        model_name = algorithm_instance.name + ' example model'
        example_model = self.test_db_session.query(Model).filter(Model.name == model_name)
        self.assertIsNone(example_model)
        self.assertEqual(algorithm_db_instance.name, algorithm_instance.name)
        self.assertEqual(algorithm_db_instance.main_file_name, algorithm_instance.main_file_name)
        self.assertEqual(algorithm_db_instance.hyperparameter_config, algorithm_instance.hyperparameter_config)
        self.assertEqual(algorithm_db_instance.learning, algorithm_instance.learning)
        self.assertEqual(algorithm_db_instance.package_id, algorithm_instance.package_id)
        self.assertIsNone(algorithm_db_instance.example_model_id)
        for input_data_pattern_db_instance in input_data_pattern_db_instances:
            self.assertIn(input_data_pattern_db_instance.pattern_id, algorithm_instance.train_input_pattern)
        for output_data_pattern_db_instance in output_data_pattern_db_instances:
            self.assertIn(output_data_pattern_db_instance.pattern_id, algorithm_instance.train_output_pattern)

    def _query_algorithm(self, case_data):
        algorithm_db_instance = self.cruder.query_algorithm(self._algorithm_instance1.id)
        self.assertEqual(algorithm_db_instance.name, self._algorithm_instance1.name)
        self.assertEqual(algorithm_db_instance.main_file_name, self._algorithm_instance1.main_file_name)
        self.assertEqual(algorithm_db_instance.hyperparameter_config, self._algorithm_instance1.hyperparameter_config)
        self.assertEqual(algorithm_db_instance.learning, self._algorithm_instance1.learning)
        self.assertEqual(algorithm_db_instance.available, self._algorithm_instance1.available)
        self.assertEqual(algorithm_db_instance.package_id, self._algorithm_instance1.package_id)

    def _query_algorithms(self, case_data):

        algorithm_db_instances = self.cruder.query_algorithms()
        print(algorithm_db_instances[0].name)
        print(algorithm_db_instances[1].name)
        print(self.algorithm_instance_list[0].name)
        print(self.algorithm_instance_list[1].name)
        for existing_algorithm_instance in self.algorithm_instance_list:
            found = False
            for algorithm_db_instance in algorithm_db_instances:
                if algorithm_db_instance.name == existing_algorithm_instance.name:
                    found = True
                    self.assertEqual(algorithm_db_instance.name, existing_algorithm_instance.name)
                    self.assertEqual(algorithm_db_instance.main_file_name, existing_algorithm_instance.main_file_name)
                    self.assertEqual(algorithm_db_instance.hyperparameter_config,
                                     existing_algorithm_instance.hyperparameter_config)
                    self.assertEqual(algorithm_db_instance.learning, existing_algorithm_instance.learning)
                    self.assertEqual(algorithm_db_instance.available, 1)
                    self.assertEqual(algorithm_db_instance.package_id, existing_algorithm_instance.package_id)
            if not found:
                self.assertTrue(False, 'Algorithm %s not found in DB!' % existing_algorithm_instance.name)

    def _delete_algorithm(self, case_data):
        self.cruder.delete_algorithm(self._algorithm_instance1)
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(self._algorithm_instance1)
        self.assertEqual(algorithm_db_instance.deleted, 1)

    def _recover_algorithm(self, case_data):
        self.cruder.delete_algorithm(self._algorithm_instance1)
        self.cruder.recover_algorithm(self._algorithm_instance1)
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(self._algorithm_instance1)
        self.assertEqual(algorithm_db_instance.deleted, 0)

    def _clean_algorithm(self, case_data):
        self.cruder.clean_algorithm(self._algorithm_instance1)
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(self._algorithm_instance1)
        self.assertIsNone(algorithm_db_instance.deleted)

    def _update_algorithm(self, case_data):

        self.cruder.update_algorithm(algorithm_id=self._algorithm_instance1.id, name=self._algorithm_instance1.name,
                                     main_file_name=self._algorithm_instance1.main_file_name,
                                     hyperparameter_config=self._algorithm_instance1.hyperparameter_config,
                                     train_input_pattern=self._algorithm_instance1.train_input_pattern,
                                     train_output_pattern=self._algorithm_instance1.train_output_pattern,
                                     model_input_pattern=self._algorithm_instance1.model_input_pattern,
                                     model_output_pattern=self._algorithm_instance1.model_output_pattern,
                                     learning=0, package_id=self._algorithm_instance1.package_id)

        algorithm_db_instance = self.test_db_session.query(Algorithm).get(self._algorithm_instance1.id)

        self.assertEqual(algorithm_db_instance.name, self._algorithm_instance1.name)
        self.assertEqual(algorithm_db_instance.main_file_name, self._algorithm_instance1.main_file_name)
        self.assertEqual(algorithm_db_instance.hyperparameter_config, self._algorithm_instance1.hyperparameter_config)
        self.assertEqual(algorithm_db_instance.learning, self._algorithm_instance1.learning)
        self.assertEqual(algorithm_db_instance.package_id, self._algorithm_instance1.package_id)
        self.assertIsNone(algorithm_db_instance.example_model_id)

        input_data_pattern_db_instances = self.test_db_session.query(AlgorithmInputDataPatterns). \
            filter(AlgorithmInputDataPatterns.algorithm_id == self._algorithm_instance1.id).all()
        output_data_pattern_db_instances = self.test_db_session.query(AlgorithmOutputDataPatterns). \
            filter(AlgorithmOutputDataPatterns.algorithm_id == self._algorithm_instance1.id).all()

        for input_data_pattern_db_instance in input_data_pattern_db_instances:
            self.assertIn(input_data_pattern_db_instance.pattern_id, self._algorithm_instance1.train_input_pattern)

        for output_data_pattern_db_instance in output_data_pattern_db_instances:
            self.assertIn(output_data_pattern_db_instance.pattern_id, self._algorithm_instance1.train_output_pattern)

        self.test_db_session.query(AlgorithmInputDataPatterns).filter(
            AlgorithmInputDataPatterns.algorithm_id == self._algorithm_instance1.id).delete()
        self.test_db_session.query(AlgorithmOutputDataPatterns).filter(
            AlgorithmOutputDataPatterns.algorithm_id == self._algorithm_instance1.id).delete()


if __name__ == '__main__':
    unittest.main()
