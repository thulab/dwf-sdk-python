
import unittest
import ddt
from test.util.handle_yaml import HandleYaml

from dwf.common.config import test_config
from dwf.model.metadata.model_crud import ModelCRUD
from dwf.ormmodels import build_test_session, Model


# 从yaml文件中取出该接口的参数
params = HandleYaml().get_data()


@ddt.ddt
class TestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_session = build_test_session(test_config)
        cls.cruder = ModelCRUD(db_session=cls.test_db_session)

    @classmethod
    def tearDownClass(cls):
        cls.test_db_session.close_all()

    @ddt.data(params)
    def test_add_model(self,params):
        model = params["add"]

        model_id = self.cruder.add_model(subid=model["subid"], creator=model["creator"],
                                         owner=model["owner"], current_process=model["current_process"],
                                         last_modifier=model["last_modifier"], name=model["name"],
                                         algorithm_id=model["algorithm_id"],
                                         description=model["description"],
                                         input_data_patterns=model["input_data_patterns"],
                                         output_data_patterns=model["output_data_patterns"],
                                         model_path=model["model_path"],
                                         model_resource=model["model_resource"], usage=model["usage"])
        model_db_instance = self.test_db_session.query(Model).get(model_id)

        self.assertEqual(model_db_instance.subid, model["subid"])
        self.assertEqual(model_db_instance.creator, model["creator"])
        self.assertEqual(model_db_instance.owner, model["owner"])
        self.assertEqual(model_db_instance.current_process, model["current_process"])
        self.assertEqual(model_db_instance.last_modifier, model["last_modifier"])
        self.assertEqual(model_db_instance.name, model["name"])
        self.assertEqual(model_db_instance.description, model["description"])
        self.assertEqual(model_db_instance.input_data_patterns, model["input_data_patterns"])
        self.assertEqual(model_db_instance.output_data_patterns, model["output_data_patterns"])
        self.assertEqual(model_db_instance.model_path,model["model_path"])
        self.assertEqual(model_db_instance.model_resource, model["model_resource"])
        self.assertEqual(model_db_instance.usage, model["usage"])

        self.test_db_session.delete(model_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_update_model(self,params):
        update_model = params["update"]
        model = params["add"]
        model_id = self.cruder.add_model(subid=model["subid"], creator=model["creator"],
                                         owner=model["owner"], current_process=model["current_process"],
                                         last_modifier=model["last_modifier"], name=model["name"],
                                         algorithm_id=model["algorithm_id"],
                                         description=model["description"],
                                         input_data_patterns=model["input_data_patterns"],
                                         output_data_patterns=model["output_data_patterns"],
                                         model_path=model["model_path"],
                                         model_resource=model["model_resource"], usage=model["usage"])

        self.cruder.update_model(model_id, usage=update_model["usage"])

        # 根据model_id查询
        model_db_instance = self.test_db_session.query(Model).get(model_id)

        # 断言
        self.assertEqual(model_db_instance.usage, update_model["usage"])
        # 删除新增的测试数据
        self.test_db_session.delete(model_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_model(self, params):
        model = params["add"]
        model_id = self.cruder.add_model(subid=model["subid"], creator=model["creator"],
                                         owner=model["owner"], current_process=model["current_process"],
                                         last_modifier=model["last_modifier"], name=model["name"],
                                         algorithm_id=model["algorithm_id"],
                                         description=model["description"],
                                         input_data_patterns=model["input_data_patterns"],
                                         output_data_patterns=model["output_data_patterns"],
                                         model_path=model["model_path"],
                                         model_resource=model["model_resource"], usage=model["usage"])

        model_crud = self.cruder.get_model(model_id)

        # 断言
        self.assertEqual(model_crud.subid, model["subid"])
        self.assertEqual(model_crud.creator, model["creator"])
        self.assertEqual(model_crud.owner, model["owner"])
        self.assertEqual(model_crud.current_process, model["current_process"])
        self.assertEqual(model_crud.last_modifier, model["last_modifier"])
        self.assertEqual(model_crud.name, model["name"])
        self.assertEqual(model_crud.description, model["description"])
        self.assertEqual(model_crud.input_data_patterns, model["input_data_patterns"])
        self.assertEqual(model_crud.output_data_patterns, model["output_data_patterns"])
        self.assertEqual(model_crud.model_path, model["model_path"])
        self.assertEqual(model_crud.model_resource, model["model_resource"])
        self.assertEqual(model_crud.usage, model["usage"])
        # 删除新增的测试数据
        self.test_db_session.delete(model_crud)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_all_model(self, params):
        model = params["add"]
        model_id = self.cruder.add_model(subid=model["subid"], creator=model["creator"],
                                         owner=model["owner"], current_process=model["current_process"],
                                         last_modifier=model["last_modifier"], name=model["name"],
                                         algorithm_id=model["algorithm_id"],
                                         description=model["description"],
                                         input_data_patterns=model["input_data_patterns"],
                                         output_data_patterns=model["output_data_patterns"],
                                         model_path=model["model_path"],
                                         model_resource=model["model_resource"], usage=model["usage"])
        model_cruds = self.cruder.get_all_model()
        model_db_all = self.test_db_session.query(Model).all()
        # # 断言
        self.assertEqual(len(model_cruds), len(model_db_all))
        # # 删除新增的测试数据
        model_db_instance = self.test_db_session.query(Model).get(model_id)
        self.test_db_session.delete(model_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_delete_model(self, params):
        model = params["add"]
        model_id = self.cruder.add_model(subid=model["subid"], creator=model["creator"],
                                         owner=model["owner"], current_process=model["current_process"],
                                         last_modifier=model["last_modifier"], name=model["name"],
                                         algorithm_id=model["algorithm_id"],
                                         description=model["description"],
                                         input_data_patterns=model["input_data_patterns"],
                                         output_data_patterns=model["output_data_patterns"],
                                         model_path=model["model_path"],
                                         model_resource=model["model_resource"], usage=model["usage"])

        self.cruder.delete_model(model_id)

        # 断言
        # 根据id查询
        model_db_instance = self.test_db_session.query(Model).get(model_id)
        self.assertEqual(model_db_instance, None)



if __name__ == '__main__':
    unittest.main()