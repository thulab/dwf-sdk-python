from test.testcase import TestCase
from test.resources.data.algorithm_data import test_algorithm1, test_algorithm2


testcase_add_algorithm = TestCase(
    name = 'Algorithm-001',
    desc = 'Add an algorithm with basic inputs.',
    judgements = '''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template = '_add_algorithm',
    data = {
           'algorithm': test_algorithm1,
       },
)

testcase_query_algorithm = TestCase(
    name='Algorithm-003',
    desc='Query an algorithm in database with id.',
    judgements='''
    1. check whether name is right
    2. check whether main_file_name is right
    3. check whether hyperparameter_config is right
    4. check whether learning is right
    5. check whether available is right
    ''',
    template='_query_algorithm',
    data={
        'algorithm': test_algorithm2,
    },
)

testcase_query_algorithms = TestCase(
    name='Algorithm-004',
    desc='Query all algorithms in database.',
    judgements='''
    1. check whether name is right
    2. check whether main_file_name is right
    3. check whether hyperparameter_config is right
    4. check whether learning is right
    5. check whether available is right
    ''',
    template='_query_algorithms',
    data={
    },
)
