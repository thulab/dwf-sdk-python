import unittest
import ddt
from test.util.handle_yaml import HandleYaml
from test.util import util

from dwf.ormmodels import build_test_session, Package
from dwf.package.metadata.package_crud import PackageCRUD
from dwf.common.config import test_config

# 从yaml文件中取出该接口的参数
params = HandleYaml("package_data.yaml").get_data()


@ddt.ddt
class TestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_session = build_test_session(test_config)
        cls.cruder = PackageCRUD(db_session=cls.test_db_session)

    @classmethod
    def tearDownClass(cls):
        cls.test_db_session.close_all()

    @ddt.data(params)
    def test_add_package(self, params):
        package = params["add"]
        test_name = util.get_name(package["name"])
        package_id = self.cruder.add_package(name=test_name, package_source=package["package_source"],
                                             package_path=package["package_path"], description=package["description"])
        # 断言
        package_db_instance = self.test_db_session.query(Package).get(package_id)
        self.assertEqual(package_db_instance.name, test_name)
        self.assertEqual(package_db_instance.package_source, package["package_source"])
        self.assertEqual(package_db_instance.package_path, package["package_path"])
        self.assertEqual(package_db_instance.description, package["description"])
        # 数据清理
        self.test_db_session.delete(package_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_delete_package(self, params):
        package = params["add"]
        test_name = util.get_name(package["name"])
        package_id = self.cruder.add_package(name=test_name, package_source=package["package_source"],
                                             package_path=package["package_path"], description=package["description"])
        self.cruder.delete_package(package_id)

        # 断言
        package_db_instance = self.test_db_session.query(Package).get(package_id)
        self.assertEqual(package_db_instance, None)

    @ddt.data(params)
    def test_update_package(self, params):
        package = params["add"]
        update_package = params["update"]
        test_name = util.get_name(package["name"])
        package_id = self.cruder.add_package(name=test_name, package_source=package["package_source"],
                                             package_path=package["package_path"], description=package["description"])

        self.cruder.update_package(package_id=package_id, name=update_package["name"])
        # 断言
        package_db_instance = self.test_db_session.query(Package).get(package_id)
        self.assertEqual(package_db_instance.name, update_package["name"])
        # 数据清理
        self.test_db_session.delete(package_db_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_package(self, params):
        package = params["add"]
        test_name = util.get_name(package["name"])
        package_id = self.cruder.add_package(name=test_name, package_source=package["package_source"],
                                             package_path=package["package_path"], description=package["description"])
        package_instance = self.cruder.get_package(package_id)
        # 断言
        self.assertEqual(package_instance.name, test_name)
        self.assertEqual(package_instance.package_source, package["package_source"])
        self.assertEqual(package_instance.package_path, package["package_path"])
        self.assertEqual(package_instance.description, package["description"])

        # 数据清理
        self.test_db_session.delete(package_instance)
        self.test_db_session.commit()

    @ddt.data(params)
    def test_get_all_package(self, params):
        package = params["add"]
        test_name = util.get_name(package["name"])
        package_id = self.cruder.add_package(name=test_name, package_source=package["package_source"],
                                             package_path=package["package_path"], description=package["description"])
        package_all = self.cruder.get_all_packages()
        packages_db_all = self.test_db_session.query(Package).all()

        # 断言
        self.assertEqual(len(package_all), len(packages_db_all))
        # 数据清理
        package_db_instance = self.test_db_session.query(Package).get(package_id)
        self.test_db_session.delete(package_db_instance)
        self.test_db_session.commit()


