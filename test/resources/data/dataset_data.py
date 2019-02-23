from test.resources.data.datapattern_data import _setup_test_datapattern1, _setup_test_datapattern2
from test.resources.data.datasource_data import _setup_test_datasource_hdfs
from dwf.util.id import generate_primary_key
import random

class DatasetTestInstance:
    def __init__(self, id, name, pattern_id, datasource_id, filter, description=None):
        self.id = id
        random_postfix = random.randint(1000, 9999)
        self.name = '%s_%s' % (name, random_postfix)
        self.pattern_id = pattern_id
        self.datasource_id = datasource_id
        self.filter = filter
        self.description = description

_setup_test_dataset1 = DatasetTestInstance(
    id=generate_primary_key('DSET'),
    name='test_dataset1',
    pattern_id=_setup_test_datapattern1.id,
    datasource_id=_setup_test_datasource_hdfs.id,
    filter='')

test_dataset1 = DatasetTestInstance(
    id=generate_primary_key('DSET'),
    name='test_dataset1',
    pattern_id=_setup_test_datapattern1.id,
    datasource_id=_setup_test_datasource_hdfs.id,
    filter='')

test_dataset2 = DatasetTestInstance(
    id=generate_primary_key('DSET'),
    name='test_dataset2',
    pattern_id=_setup_test_datapattern2.id,
    datasource_id=_setup_test_datasource_hdfs.id,
    filter='')
