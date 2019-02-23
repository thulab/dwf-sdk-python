from dwf.ormmodels import Datasource
from dwf.util.id import generate_primary_key
import random


class DataSourceTestInstance:
    def __init__(self, id, name, hostname, port, username, passwd, datasource_type):
        self.id = id
        random_postfix = random.randint(1000, 9999)
        self.name = '%s_%s' % (name, random_postfix)
        self.hostname = hostname
        self.port = port
        self.username = username
        self.passwd = passwd
        self.datasource_type = datasource_type

_setup_test_datasource_hdfs = DataSourceTestInstance(
    id=generate_primary_key('DSOU'),
    name='HDSFServer',
    hostname='192.168.5.5',
    port='9900',
    username='user',
    passwd='password',
    datasource_type=Datasource.HDFS_TYPE)


test_datasource_hdfs = DataSourceTestInstance(
    id=generate_primary_key('DSOU'),
    name='HDSFServer',
    hostname='192.168.5.5',
    port='9900',
    username='user',
    passwd='password',
    datasource_type=Datasource.HDFS_TYPE)

