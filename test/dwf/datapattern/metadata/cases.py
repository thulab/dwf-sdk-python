from test.testcase import TestCase
from test.resources.data.datapattern_data import _setup_test_datapattern1

testcase_add_datapattern = TestCase(
    name='Datapattern-001',
    desc='Add a datapattern with basic inputs.',
    judgements='''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template='_add_datapattern',
    data={
        'datapattern': _setup_test_datapattern1
    },
)
