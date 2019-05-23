
import unittest
import ddt
from test.util.handle_yaml import HandleYaml
from test.util import util

from dwf.common.config import test_config
from dwf.ormmodels import build_test_session, Dataset
from dwf.dataset.metadata.dataset_crud import DatasetCRUD

# 从yaml文件中取出该接口的参数
params = HandleYaml("dataset_data.yaml").get_data()


@ddt.ddt
class TestDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_session = build_test_session(test_config)
        cls.cruder = DatasetCRUD(db_session=cls.test_db_session)

    @classmethod
    def tearDownClass(cls):
        cls.test_db_session.close_all()

    @ddt.data(params)
    def test_add_dataset(self, params):
        dataset = params["add"]
        test_name = util.get_name(dataset["name"])
        dataset_id = self.cruder.add_dataset(test_name, datasource_id=dataset["datasource_id"], subid=dataset["subid"],
                                             creator=dataset["creator"], owner=dataset["owner"],
                                             current_process=dataset["current_process"],
                                             last_modifier=dataset["last_modifier"],
                                             data_file_format=dataset["data_file_format"],
                                             default_filter_string=dataset["default_filter_string"],
                                             description=dataset["description"],
                                             filter=dataset["filter"], patterns=dataset["patterns"],
                                             target_entity_class=dataset["target_entity_class"])
        # 断言
        dataset_db_instance = self.test_db_session.query(Dataset).get(dataset_id)

        self.assertEqual(dataset_db_instance.name, test_name)
        self.assertEqual(dataset_db_instance.datasource_id, dataset["datasource_id"])
        self.assertEqual(dataset_db_instance.subid, dataset["subid"])
        self.assertEqual(dataset_db_instance.creator, dataset["creator"])
        self.assertEqual(dataset_db_instance.owner, dataset["owner"])
        self.assertEqual(dataset_db_instance.current_process, dataset["current_process"])
        self.assertEqual(dataset_db_instance.last_modifier, dataset["last_modifier"])
        self.assertEqual(dataset_db_instance.data_file_format, dataset["data_file_format"])
        self.assertEqual(dataset_db_instance.default_filter_string, dataset["default_filter_string"])
        self.assertEqual(dataset_db_instance.description, dataset["description"])
        self.assertEqual(dataset_db_instance.filter, dataset["filter"])
        self.assertEqual(dataset_db_instance.patterns, dataset["patterns"])
        self.assertEqual(dataset_db_instance.target_entity_class, dataset["target_entity_class"])

        self.test_db_session.delete(dataset_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_update_dataset(self, params):
        update_dataset = params["update"]
        dataset = params["add"]
        test_name = util.get_name(dataset["name"])
        dataset_id = self.cruder.add_dataset(test_name, datasource_id=dataset["datasource_id"], subid=dataset["subid"],
                                             creator=dataset["creator"], owner=dataset["owner"],
                                             current_process=dataset["current_process"],
                                             last_modifier=dataset["last_modifier"],
                                             data_file_format=dataset["data_file_format"],
                                             default_filter_string=dataset["default_filter_string"],
                                             description=dataset["description"],
                                             filter=dataset["filter"], patterns=dataset["patterns"],
                                             target_entity_class=dataset["target_entity_class"])

        self.cruder.update_dataset(dataset_id=dataset_id, description=update_dataset["description"])

        dataset_db_instance = self.test_db_session.query(Dataset).get(dataset_id)

        # 断言
        self.assertEqual(dataset_db_instance.description, update_dataset["description"])
        # 删除新增的测试数据
        self.test_db_session.delete(dataset_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_dataset(self, params):
        dataset = params["add"]
        test_name = util.get_name(dataset["name"])
        dataset_id = self.cruder.add_dataset(test_name, datasource_id=dataset["datasource_id"], subid=dataset["subid"],
                                             creator=dataset["creator"], owner=dataset["owner"],
                                             current_process=dataset["current_process"],
                                             last_modifier=dataset["last_modifier"],
                                             data_file_format=dataset["data_file_format"],
                                             default_filter_string=dataset["default_filter_string"],
                                             description=dataset["description"],
                                             filter=dataset["filter"], patterns=dataset["patterns"],
                                             target_entity_class=dataset["target_entity_class"])

        dataset_crud = self.cruder.get_dataset(dataset_id)

        # 断言
        self.assertEqual(dataset_crud.name, test_name)
        self.assertEqual(dataset_crud.datasource_id, dataset["datasource_id"])
        self.assertEqual(dataset_crud.subid, dataset["subid"])
        self.assertEqual(dataset_crud.creator, dataset["creator"])
        self.assertEqual(dataset_crud.owner, dataset["owner"])
        self.assertEqual(dataset_crud.current_process, dataset["current_process"])
        self.assertEqual(dataset_crud.last_modifier, dataset["last_modifier"])
        self.assertEqual(dataset_crud.data_file_format, dataset["data_file_format"])
        self.assertEqual(dataset_crud.default_filter_string, dataset["default_filter_string"])
        self.assertEqual(dataset_crud.description, dataset["description"])
        self.assertEqual(dataset_crud.filter, dataset["filter"])
        self.assertEqual(dataset_crud.patterns, dataset["patterns"])
        self.assertEqual(dataset_crud.target_entity_class, dataset["target_entity_class"])
        # 删除新增的测试数据
        self.test_db_session.delete(dataset_crud)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_all_dataset(self, params):
        dataset = params["add"]
        test_name = util.get_name(dataset["name"])
        dataset_id = self.cruder.add_dataset(test_name, datasource_id=dataset["datasource_id"], subid=dataset["subid"],
                                             creator=dataset["creator"], owner=dataset["owner"],
                                             current_process=dataset["current_process"],
                                             last_modifier=dataset["last_modifier"],
                                             data_file_format=dataset["data_file_format"],
                                             default_filter_string=dataset["default_filter_string"],
                                             description=dataset["description"],
                                             filter=dataset["filter"], patterns=dataset["patterns"],
                                             target_entity_class=dataset["target_entity_class"])

        dataset_cruds = self.cruder.get_all_dataset()
        dataset_db_all = self.test_db_session.query(Dataset).all()
        # # 断言
        self.assertEqual(len(dataset_cruds), len(dataset_db_all))
        # # 删除新增的测试数据
        dataset_db_instance = self.test_db_session.query(Dataset).get(dataset_id)
        self.test_db_session.delete(dataset_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_delete_dataset(self, params):
        dataset = params["add"]
        test_name = util.get_name(dataset["name"])
        dataset_id = self.cruder.add_dataset(test_name, datasource_id=dataset["datasource_id"], subid=dataset["subid"],
                                             creator=dataset["creator"], owner=dataset["owner"],
                                             current_process=dataset["current_process"],
                                             last_modifier=dataset["last_modifier"],
                                             data_file_format=dataset["data_file_format"],
                                             default_filter_string=dataset["default_filter_string"],
                                             description=dataset["description"],
                                             filter=dataset["filter"], patterns=dataset["patterns"],
                                             target_entity_class=dataset["target_entity_class"])

        self.cruder.delete_dataset(dataset_id)

        # 断言
        # 根据id查询
        dataset_db_instance = self.test_db_session.query(Dataset).get(dataset_id)
        self.assertEqual(dataset_db_instance, None)



if __name__ == '__main__':
    unittest.main()
