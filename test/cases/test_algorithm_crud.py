
import unittest
import ddt
from test.util.handle_yaml import HandleYaml
from test.util import util

from dwf.common.config import test_config
from dwf.ormmodels import build_test_session, Algorithm
from dwf.algorithm.metadata.algorithm_crud import AlgorithmCRUD

# 从yaml文件中取出该接口的参数
params = HandleYaml("algorithm_data.yaml").get_data()


@ddt.ddt
class TestDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_session = build_test_session(test_config)
        cls.cruder = AlgorithmCRUD(db_session=cls.test_db_session)

    @classmethod
    def tearDownClass(cls):
        cls.test_db_session.close_all()

    @ddt.data(params)
    def test_add_algorithm(self, params):
        algorithm = params["add"]
        test_name = util.get_name(algorithm["name"])
        algorithm_id = self.cruder.add_algorithm(name=test_name, display_name=algorithm["display_name"],
                                                 description=algorithm["description"],
                                                 entry_name=algorithm["entry_name"],
                                                 algorithm_type=algorithm["algorithm_type"],
                                                 hyperparameter_config=algorithm["hyperparameter_config"],
                                                 available=algorithm["available"],
                                                 train_input_pattern=algorithm["train_input_pattern"],
                                                 train_output_pattern=algorithm["train_output_pattern"],
                                                 model_input_pattern=algorithm["model_input_pattern"],
                                                 model_output_pattern=algorithm["model_output_pattern"],
                                                 runtime=algorithm["runtime"], learning=algorithm["learning"],
                                                 package_id=algorithm["package_id"])

        # 断言
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)

        self.assertEqual(algorithm_db_instance.name, test_name)
        self.assertEqual(algorithm_db_instance.display_name, algorithm["display_name"])
        self.assertEqual(algorithm_db_instance.description, algorithm["description"])
        self.assertEqual(algorithm_db_instance.entry_name, algorithm["entry_name"])
        self.assertEqual(algorithm_db_instance.algorithm_type, algorithm["algorithm_type"])
        self.assertEqual(algorithm_db_instance.parameters, algorithm["hyperparameter_config"])
        self.assertEqual(algorithm_db_instance.available, algorithm["available"])
        self.assertEqual(algorithm_db_instance.alg_input_patterns, algorithm["train_input_pattern"])
        self.assertEqual(algorithm_db_instance.alg_output_patterns, algorithm["train_output_pattern"])
        self.assertEqual(algorithm_db_instance.model_input_patterns, algorithm["model_input_pattern"])
        self.assertEqual(algorithm_db_instance.model_output_patterns, algorithm["model_output_pattern"])
        self.assertEqual(algorithm_db_instance.runtime, algorithm["runtime"])
        self.assertEqual(algorithm_db_instance.package_id, algorithm["package_id"])

        self.test_db_session.delete(algorithm_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_update_algorithm(self, params):
        update_algorithm = params["update"]
        algorithm = params["add"]
        test_name = util.get_name(algorithm["name"])
        algorithm_id = self.cruder.add_algorithm(name=test_name, display_name=algorithm["display_name"],
                                                 description=algorithm["description"],
                                                 entry_name=algorithm["entry_name"],
                                                 algorithm_type=algorithm["algorithm_type"],
                                                 hyperparameter_config=algorithm["hyperparameter_config"],
                                                 available=algorithm["available"],
                                                 train_input_pattern=algorithm["train_input_pattern"],
                                                 train_output_pattern=algorithm["train_output_pattern"],
                                                 model_input_pattern=algorithm["model_input_pattern"],
                                                 model_output_pattern=algorithm["model_output_pattern"],
                                                 runtime=algorithm["runtime"], learning=algorithm["learning"],
                                                 package_id=algorithm["package_id"])

        self.cruder.update_algorithm(algorithm_id=algorithm_id, description=update_algorithm["description"])

        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)

        # 断言
        self.assertEqual(algorithm_db_instance.description, update_algorithm["description"])
        # 删除新增的测试数据
        self.test_db_session.delete(algorithm_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_algorithm(self, params):
        algorithm = params["add"]
        test_name = util.get_name(algorithm["name"])
        algorithm_id = self.cruder.add_algorithm(name=test_name, display_name=algorithm["display_name"],
                                                 description=algorithm["description"],
                                                 entry_name=algorithm["entry_name"],
                                                 algorithm_type=algorithm["algorithm_type"],
                                                 hyperparameter_config=algorithm["hyperparameter_config"],
                                                 available=algorithm["available"],
                                                 train_input_pattern=algorithm["train_input_pattern"],
                                                 train_output_pattern=algorithm["train_output_pattern"],
                                                 model_input_pattern=algorithm["model_input_pattern"],
                                                 model_output_pattern=algorithm["model_output_pattern"],
                                                 runtime=algorithm["runtime"], learning=algorithm["learning"],
                                                 package_id=algorithm["package_id"])

        algorithm_crud = self.cruder.get_algorithm(algorithm_id)

        # 断言
        self.assertEqual(algorithm_crud.name, test_name)
        self.assertEqual(algorithm_crud.display_name, algorithm["display_name"])
        self.assertEqual(algorithm_crud.description, algorithm["description"])
        self.assertEqual(algorithm_crud.entry_name, algorithm["entry_name"])
        self.assertEqual(algorithm_crud.algorithm_type, algorithm["algorithm_type"])
        self.assertEqual(algorithm_crud.parameters, algorithm["hyperparameter_config"])
        self.assertEqual(algorithm_crud.available, algorithm["available"])
        self.assertEqual(algorithm_crud.alg_input_patterns, algorithm["train_input_pattern"])
        self.assertEqual(algorithm_crud.alg_output_patterns, algorithm["train_output_pattern"])
        self.assertEqual(algorithm_crud.model_input_patterns, algorithm["model_input_pattern"])
        self.assertEqual(algorithm_crud.model_output_patterns, algorithm["model_output_pattern"])
        self.assertEqual(algorithm_crud.runtime, algorithm["runtime"])
        self.assertEqual(algorithm_crud.package_id, algorithm["package_id"])

        # 删除新增的测试数据
        self.test_db_session.delete(algorithm_crud)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_all_algorithm(self, params):
        algorithm = params["add"]
        test_name = util.get_name(algorithm["name"])
        algorithm_id = self.cruder.add_algorithm(name=test_name, display_name=algorithm["display_name"],
                                                 description=algorithm["description"],
                                                 entry_name=algorithm["entry_name"],
                                                 algorithm_type=algorithm["algorithm_type"],
                                                 hyperparameter_config=algorithm["hyperparameter_config"],
                                                 available=algorithm["available"],
                                                 train_input_pattern=algorithm["train_input_pattern"],
                                                 train_output_pattern=algorithm["train_output_pattern"],
                                                 model_input_pattern=algorithm["model_input_pattern"],
                                                 model_output_pattern=algorithm["model_output_pattern"],
                                                 runtime=algorithm["runtime"], learning=algorithm["learning"],
                                                 package_id=algorithm["package_id"])

        algorithm_cruds = self.cruder.get_all_algorithms()
        algorithm_db_all = self.test_db_session.query(Algorithm).all()
        # # 断言
        self.assertEqual(len(algorithm_cruds), len(algorithm_db_all))
        # # 删除新增的测试数据
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)
        self.test_db_session.delete(algorithm_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_delete_algorithm(self, params):
        algorithm = params["add"]
        test_name = util.get_name(algorithm["name"])
        algorithm_id = self.cruder.add_algorithm(name=test_name, display_name=algorithm["display_name"],
                                                 description=algorithm["description"],
                                                 entry_name=algorithm["entry_name"],
                                                 algorithm_type=algorithm["algorithm_type"],
                                                 hyperparameter_config=algorithm["hyperparameter_config"],
                                                 available=algorithm["available"],
                                                 train_input_pattern=algorithm["train_input_pattern"],
                                                 train_output_pattern=algorithm["train_output_pattern"],
                                                 model_input_pattern=algorithm["model_input_pattern"],
                                                 model_output_pattern=algorithm["model_output_pattern"],
                                                 runtime=algorithm["runtime"], learning=algorithm["learning"],
                                                 package_id=algorithm["package_id"])

        self.cruder.delete_algorithm(algorithm_id)

        # 断言
        # 根据id查询
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)
        self.assertEqual(algorithm_db_instance.isdeleted, "1")
        # # 删除新增的测试数据
        self.test_db_session.delete(algorithm_db_instance)
        self.test_db_session.commit()


    @ddt.data(params)
    def test_recover_algorithm(self, params):
        algorithm = params["add"]
        test_name = util.get_name(algorithm["name"])
        algorithm_id = self.cruder.add_algorithm(name=test_name, display_name=algorithm["display_name"],
                                                 description=algorithm["description"],
                                                 entry_name=algorithm["entry_name"],
                                                 algorithm_type=algorithm["algorithm_type"],
                                                 hyperparameter_config=algorithm["hyperparameter_config"],
                                                 available=algorithm["available"],
                                                 train_input_pattern=algorithm["train_input_pattern"],
                                                 train_output_pattern=algorithm["train_output_pattern"],
                                                 model_input_pattern=algorithm["model_input_pattern"],
                                                 model_output_pattern=algorithm["model_output_pattern"],
                                                 runtime=algorithm["runtime"], learning=algorithm["learning"],
                                                 package_id=algorithm["package_id"])

        self.cruder.recover_algorithm(algorithm_id)

        # 断言
        # 根据id查询
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)
        self.assertEqual(algorithm_db_instance.isdeleted, "0")
        # # 删除新增的测试数据
        self.test_db_session.delete(algorithm_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_algorithm_unavailable(self, params):
        algorithm = params["add"]
        test_name = util.get_name(algorithm["name"])
        algorithm_id = self.cruder.add_algorithm(name=test_name, display_name=algorithm["display_name"],
                                                 description=algorithm["description"],
                                                 entry_name=algorithm["entry_name"],
                                                 algorithm_type=algorithm["algorithm_type"],
                                                 hyperparameter_config=algorithm["hyperparameter_config"],
                                                 available=algorithm["available"],
                                                 train_input_pattern=algorithm["train_input_pattern"],
                                                 train_output_pattern=algorithm["train_output_pattern"],
                                                 model_input_pattern=algorithm["model_input_pattern"],
                                                 model_output_pattern=algorithm["model_output_pattern"],
                                                 runtime=algorithm["runtime"], learning=algorithm["learning"],
                                                 package_id=algorithm["package_id"])

        self.cruder.make_algorithm_unavailable(algorithm_id)

        # 断言
        # 根据id查询
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)
        self.assertEqual(algorithm_db_instance.available, "0")
        # # 删除新增的测试数据
        self.test_db_session.delete(algorithm_db_instance)
        self.test_db_session.commit()


    @ddt.data(params)
    def test_clean_algorithm(self, params):
        algorithm = params["add"]
        test_name = util.get_name(algorithm["name"])
        algorithm_id = self.cruder.add_algorithm(name=test_name, display_name=algorithm["display_name"],
                                                 description=algorithm["description"],
                                                 entry_name=algorithm["entry_name"],
                                                 algorithm_type=algorithm["algorithm_type"],
                                                 hyperparameter_config=algorithm["hyperparameter_config"],
                                                 available=algorithm["available"],
                                                 train_input_pattern=algorithm["train_input_pattern"],
                                                 train_output_pattern=algorithm["train_output_pattern"],
                                                 model_input_pattern=algorithm["model_input_pattern"],
                                                 model_output_pattern=algorithm["model_output_pattern"],
                                                 runtime=algorithm["runtime"], learning=algorithm["learning"],
                                                 package_id=algorithm["package_id"])

        self.cruder.clean_algorithm(algorithm_id)

        # 断言
        # 根据id查询
        algorithm_db_instance = self.test_db_session.query(Algorithm).get(algorithm_id)
        self.assertEqual(algorithm_db_instance, None)


if __name__ == '__main__':
    unittest.main()
