from dwf.ormmodels import datetime
import random
import uuid


class ModelTestInstance:
    def __init__(self, id, subid, creator, owner, current_process, last_modifier, create_time, update_ime, name,
                 description, input_data_patterns, output_data_patterns, model_path, model_resource, usage):
        self.id = id
        self.subid = subid
        self.creator = creator
        self.owner = owner
        self.current_process = current_process
        self.last_modifier = last_modifier
        self.create_time = create_time
        self.update_ime = update_ime
        random_postfix = random.randint(1000, 9999)
        self.name = '%s_%s' % (name, random_postfix)
        self.description = description
        self.input_data_patterns = input_data_patterns
        self.output_data_patterns = output_data_patterns
        self.model_path = model_path
        self.model_resource = model_resource
        self.usage = usage


test_model1 = ModelTestInstance(
    id=str(uuid.uuid1()).replace('-', ''),
    subid='001',
    creator='admin',
    owner='admin',
    current_process='process1',
    last_modifier='admin',
    create_time=datetime.now(),
    update_ime=datetime.now(),
    name='test_model',
    description='test model description',
    input_data_patterns='[test_pattern1,test_pattern2]',
    output_data_patterns='[test_pattern3,test_pattern4]',
    model_path='test model path',
    model_resource='test model resource',
    usage='test model usage'
)
