from test.testcase import TestCase
from test.resources.data.dataset_data import test_dataset1, test_dataset2

testcase_add_dataset = TestCase(
    name='Dataset-001',
    desc='Add a dataset with basic inputs.',
    judgements='''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template='_add_dataset',
    data={
        'dataset': test_dataset1,
    },
)

testcase_get_dataset = TestCase(
    name='Dataset-002',
    desc='Get a dataset in database with id.',
    judgements='''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template='_get_dataset',
    data={
        'dataset': test_dataset1,
    },
)

testcase_get_dataset_all = TestCase(
    name='Dataset-003',
    desc='Get all datasets in database.',
    judgements='''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template='_get_dataset_all',
    data={
        'dataset': test_dataset1,
        'dataset2': test_dataset2,
    },
)

testcase_delete_dataset_all = TestCase(
    name='Dataset-004',
    desc='Delete a dataset in database with id.',
    judgements='''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template='_delete_dataset',
    data={
        'dataset': test_dataset1,
    },
)
