from test.testcase import TestCase
from test.resources.data.model_data import *

testcase_add_datasource_hdfs = TestCase(
    name = 'Model-001',
    desc = 'Add an model with basic inputs.',
    judgements = '''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template = '_add_model',
    data = {
           'model': test_model1
       },
)

