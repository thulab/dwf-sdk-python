
import unittest
import ddt
from test.util.handle_yaml import HandleYaml
from test.util import util

from dwf.common.config import test_config
from dwf.ormmodels import build_test_session,Datasource
from dwf.datasource.metadata.datasource_crud import DataSourceCRUD


# 从yaml文件中取出该接口的参数
params = HandleYaml("datasource_data.yaml").get_data()


@ddt.ddt
class TestDatasource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_session = build_test_session(test_config)
        cls.cruder = DataSourceCRUD(db_session=cls.test_db_session)

    @classmethod
    def tearDownClass(cls):
        cls.test_db_session.close_all()

    @ddt.data(params)
    def test_add_datasource(self,params):
        datasource = params["add"]
        test_name = util.get_name(datasource["name"])
        datasource_id = self.cruder.add_datasource(name=test_name, subid=datasource["subid"],
                                              creator=datasource["creator"], owner=datasource["owner"],
                                              current_process=datasource["current_process"],
                                              last_modifier=datasource["last_modifier"],
                                              database_name=datasource["database_name"],
                                              description=datasource['description'],
                                              folder_depth=datasource["folder_depth"], paramone=datasource["paramone"],
                                              password=datasource["password"], server_ip=datasource["server_ip"],
                                              server_port=datasource["server_port"], username=datasource["username"],
                                              workbench_url=datasource["workbench_url"])
        # 断言
        datasource_db_instance = self.test_db_session.query(Datasource).get(datasource_id)

        self.assertEqual(datasource_db_instance.subid, datasource["subid"])
        self.assertEqual(datasource_db_instance.name,test_name)
        self.assertEqual(datasource_db_instance.creator, datasource["creator"])
        self.assertEqual(datasource_db_instance.owner, datasource["owner"])
        self.assertEqual(datasource_db_instance.current_process, datasource["current_process"])
        self.assertEqual(datasource_db_instance.last_modifier, datasource["last_modifier"])
        self.assertEqual(datasource_db_instance.database_name, datasource["database_name"])
        self.assertEqual(datasource_db_instance.description, datasource["description"])
        self.assertEqual(datasource_db_instance.folder_depth, datasource["folder_depth"])
        self.assertEqual(datasource_db_instance.paramone, datasource["paramone"])
        self.assertEqual(datasource_db_instance.password, datasource["password"])
        self.assertEqual(datasource_db_instance.server_ip, datasource["server_ip"])
        self.assertEqual(datasource_db_instance.server_port, datasource["server_port"])
        self.assertEqual(datasource_db_instance.username, datasource["username"])
        self.assertEqual(datasource_db_instance.workbench_url, datasource["workbench_url"])

        self.test_db_session.delete(datasource_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_update_datasource(self,params):
        update_datasource = params["update"]
        datasource = params["add"]
        test_name = util.get_name(datasource["name"])
        datasource_id = self.cruder.add_datasource(name=test_name, subid=datasource["subid"],
                                                   creator=datasource["creator"], owner=datasource["owner"],
                                                   current_process=datasource["current_process"],
                                                   last_modifier=datasource["last_modifier"],
                                                   database_name=datasource["database_name"],
                                                   description=datasource['description'],
                                                   folder_depth=datasource["folder_depth"],
                                                   paramone=datasource["paramone"],
                                                   password=datasource["password"], server_ip=datasource["server_ip"],
                                                   server_port=datasource["server_port"],
                                                   username=datasource["username"],
                                                   workbench_url=datasource["workbench_url"])

        self.cruder.update_datasource(datasource_id=datasource_id, server_port=update_datasource["server_port"])

        datasource_db_instance = self.test_db_session.query(Datasource).get(datasource_id)

        # 断言
        self.assertEqual(datasource_db_instance.server_port, update_datasource["server_port"])
        # 删除新增的测试数据
        self.test_db_session.delete(datasource_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_datasource(self, params):
        datasource = params["add"]
        test_name = util.get_name(datasource["name"])
        datasource_id = self.cruder.add_datasource(name=test_name, subid=datasource["subid"],
                                                   creator=datasource["creator"], owner=datasource["owner"],
                                                   current_process=datasource["current_process"],
                                                   last_modifier=datasource["last_modifier"],
                                                   database_name=datasource["database_name"],
                                                   description=datasource['description'],
                                                   folder_depth=datasource["folder_depth"],
                                                   paramone=datasource["paramone"],
                                                   password=datasource["password"], server_ip=datasource["server_ip"],
                                                   server_port=datasource["server_port"],
                                                   username=datasource["username"],
                                                   workbench_url=datasource["workbench_url"])

        datasource_crud = self.cruder.get_datasource(datasource_id)

        # 断言
        self.assertEqual(datasource_crud.subid, datasource["subid"])
        self.assertEqual(datasource_crud.name, test_name)
        self.assertEqual(datasource_crud.creator, datasource["creator"])
        self.assertEqual(datasource_crud.owner, datasource["owner"])
        self.assertEqual(datasource_crud.current_process, datasource["current_process"])
        self.assertEqual(datasource_crud.last_modifier, datasource["last_modifier"])
        self.assertEqual(datasource_crud.database_name, datasource["database_name"])
        self.assertEqual(datasource_crud.description, datasource["description"])
        self.assertEqual(datasource_crud.folder_depth, datasource["folder_depth"])
        self.assertEqual(datasource_crud.paramone, datasource["paramone"])
        self.assertEqual(datasource_crud.password, datasource["password"])
        self.assertEqual(datasource_crud.server_ip, datasource["server_ip"])
        self.assertEqual(datasource_crud.server_port, datasource["server_port"])
        self.assertEqual(datasource_crud.username, datasource["username"])
        self.assertEqual(datasource_crud.workbench_url, datasource["workbench_url"])
        # 删除新增的测试数据
        self.test_db_session.delete(datasource_crud)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_all_datasource(self, params):
        datasource = params["add"]
        test_name = util.get_name(datasource["name"])
        datasource_id = self.cruder.add_datasource(name=test_name, subid=datasource["subid"],
                                                   creator=datasource["creator"], owner=datasource["owner"],
                                                   current_process=datasource["current_process"],
                                                   last_modifier=datasource["last_modifier"],
                                                   database_name=datasource["database_name"],
                                                   description=datasource['description'],
                                                   folder_depth=datasource["folder_depth"],
                                                   paramone=datasource["paramone"],
                                                   password=datasource["password"], server_ip=datasource["server_ip"],
                                                   server_port=datasource["server_port"],
                                                   username=datasource["username"],
                                                   workbench_url=datasource["workbench_url"])

        datasource_cruds = self.cruder.get_all_datasource()
        datasource_db_all = self.test_db_session.query(Datasource).all()
        # # 断言
        self.assertEqual(len(datasource_cruds), len(datasource_db_all))
        # # 删除新增的测试数据
        datasource_db_instance = self.test_db_session.query(Datasource).get(datasource_id)
        self.test_db_session.delete(datasource_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_delete_datasource(self, params):
        datasource = params["add"]
        test_name = util.get_name(datasource["name"])
        datasource_id = self.cruder.add_datasource(name=test_name, subid=datasource["subid"],
                                                   creator=datasource["creator"], owner=datasource["owner"],
                                                   current_process=datasource["current_process"],
                                                   last_modifier=datasource["last_modifier"],
                                                   database_name=datasource["database_name"],
                                                   description=datasource['description'],
                                                   folder_depth=datasource["folder_depth"],
                                                   paramone=datasource["paramone"],
                                                   password=datasource["password"], server_ip=datasource["server_ip"],
                                                   server_port=datasource["server_port"],
                                                   username=datasource["username"],
                                                   workbench_url=datasource["workbench_url"])

        self.cruder.delete_datasource(datasource_id)

        # 断言
        # 根据id查询
        datasource_db_instance = self.test_db_session.query(Datasource).get(datasource_id)
        self.assertEqual(datasource_db_instance, None)


if __name__ == '__main__':
    unittest.main()