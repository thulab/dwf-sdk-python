from test.testcase import TestCase
from test.resources.data.datasource_data import test_datasource_hdfs

testcase_add_datasource_hdfs = TestCase(
    name = 'Datasource-001',
    desc = 'Add an HDFS datasource with basic inputs.',
    judgements = '''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template = '_add_datasource',
    data = {
           'datasource': test_datasource_hdfs
       },
)

testcase_get_datasource_hdfs = TestCase(
    name = 'Datasource-002',
    desc = 'Get an HDFS datasource with id.',
    judgements = '''
    1. check whether name is right
    2. check whether desc is right
    3. check whether type is right
    ''',
    template = '_get_datasource',
    data = {
           'datasource': test_datasource_hdfs
       },
)

testcase_delete_datasource_hdfs = TestCase(
    name = 'Datasource-003',
    desc = 'Delete an HDFS datasource with id.',
    judgements = '''
    1. check whether datasource is deleted
    ''',
    template = '_delete_datasource',
    data = {
           'datasource': test_datasource_hdfs
       },
)

