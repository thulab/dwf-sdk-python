from dwf.ormmodels import datetime
from dwf.util.id import generate_primary_key
import random

class ModelTestInstance:
    def __init__(self,id,name,description,help,create_time,update_time, model_path,log_path):
        self.id = id
        random_postfix = random.randint(1000, 9999)
        self.name = '%s_%s' % (name, random_postfix)
        self.description = description
        self.help = help
        self.create_time = create_time
        self.update_time = update_time
        self.model_path = model_path
        self.log_path = log_path


test_model1 = ModelTestInstance(
    id=generate_primary_key('MODE'),
    name='test_model',
    description='test model description',
    help='test model help',
    create_time=datetime.now(),
    update_time=datetime.now(),
    model_path='test model path',
    log_path='test model log path')

_setup_test_model1 = ModelTestInstance(
    id=generate_primary_key('MODE'),
    name='setup_test_model',
    description='setup_test model description',
    help='setup_test model help',
    create_time=datetime.now(),
    update_time=datetime.now(),
    model_path='setup_test model path',
    log_path='setup_test model log path')
