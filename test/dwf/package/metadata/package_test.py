# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2018.10.30
#
# Title: Tests for CRUD of package metadata
#
# Version 1.0


import unittest
from dwf.package.metadata.package_crud import PackageCRUD
from test.dwf.package.metadata import cases
from dwf.common.config import test_config
from dwf.ormmodels import build_test_session, Package

from test.runner import check_and_do_cases


class TestCRUD(unittest.TestCase):

    def prepare_data(self):
        self.to_be_deleted = []

    def test_all_cases(self):
        self.test_db_session = build_test_session(test_config)
        self.cruder = PackageCRUD(db_session=self.test_db_session)
        check_and_do_cases(self, cases)

    def _add_package(self, case_data):
        package_instance = case_data['package']
        package_id = self.cruder.add_package(name=package_instance.name, package_source=package_instance.package_source,
                                             package_path=package_instance.package_path,
                                             description=package_instance.description)
        package_db_instance = self.test_db_session.query(Package).get(package_id)

        self.assertEqual(package_db_instance.name, package_instance.name)
        self.assertEqual(package_db_instance.package_source, package_instance.package_source)
        self.assertEqual(package_db_instance.package_path, package_instance.package_path)
        self.assertEqual(package_db_instance.description, package_instance.description)

        self.test_db_session.delete(package_db_instance)
        self.test_db_session.commit()


if __name__ == '__main__':
    unittest.main()
