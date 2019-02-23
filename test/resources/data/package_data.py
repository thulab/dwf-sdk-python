from dwf.ormmodels import datetime
from dwf.util.id import generate_primary_key
import random


class PackageTestInstance:
    def __init__(self,id, name,create_time, package_source, package_path, description):
        self.id = id
        self.create_time = create_time
        random_postfix = random.randint(1000, 9999)
        self.name = '%s_%s' % (name, random_postfix)
        self.package_source = package_source
        self.package_path = package_path
        self.description = description

_setup_test_package1 = PackageTestInstance(
    id=generate_primary_key('PACK'),
    name = 'test_package1_name',
    create_time=datetime.now(),
    package_source = 'test_package_source',
    package_path = 'test_package_path',
    description = 'test_description')

test_package1 = PackageTestInstance(
    id=generate_primary_key('PACK'),
    name = 'test_package1_name',
    create_time=datetime.now(),
    package_source = 'test_package_source',
    package_path = 'test_package_path',
    description = 'test_description')

test_package2 = PackageTestInstance(
    id=generate_primary_key('PACK'),
    name = 'test_package2_name',
    create_time=datetime.now(),
    package_source = 'test_package_source2',
    package_path = 'test_package_path2',
    description = 'test_description2')

test_package3 = PackageTestInstance(
    id=generate_primary_key('PACK'),
    name = 'test_package3_name',
    create_time=datetime.now(),
    package_source = 'test_package_source3',
    package_path = 'test_package_path3',
    description = 'test_description3')

test_package4 = PackageTestInstance(
    id=generate_primary_key('PACK'),
    name = 'test_package4_name',
    create_time=datetime.now(),
    package_source = 'test_package_source4',
    package_path = 'test_package_path4',
    description = 'test_description4')

test_package5 = PackageTestInstance(
    id=generate_primary_key('PACK'),
    name = 'test_package5_name',
    create_time=datetime.now(),
    package_source = 'test_package_source5',
    package_path = 'test_package_path5',
    description = 'test_description5')