from test.testcase import TestCase
from test.resources.data.package_data import test_package1

testcase_add_package = TestCase(
    name = 'Package-001',
    desc = 'Add a package with basic inputs.',
    judgements = '''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template = '_add_package',
    data = {
           'package': test_package1
       },
)

