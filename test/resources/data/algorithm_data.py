from dwf.util.id import generate_primary_key
from test.resources.data.datapattern_data import _setup_test_datapattern1,\
    _setup_test_datapattern2, _setup_test_datapattern3, _setup_test_datapattern4
from test.resources.data.package_data import _setup_test_package1
import random


class AlgorithmTestInstance:
    def __init__(self, id, name, main_file_name, hyperparameter_config, train_input_pattern, train_output_pattern,
                  model_input_pattern, model_output_pattern, learning, package_id):
        self.id = id
        random_postfix = random.randint(1000,9999)
        self.name = '%s_%s' % (name, random_postfix)
        self.main_file_name = main_file_name
        self.hyperparameter_config = hyperparameter_config
        self.train_input_pattern = train_input_pattern
        self.train_output_pattern = train_output_pattern
        self.model_input_pattern = model_input_pattern
        self.model_output_pattern = model_output_pattern
        self.learning = learning
        self.package_id = package_id


_setup_test_algorithm1 = AlgorithmTestInstance(
    id=generate_primary_key('ALGO'),
    name='setup_test_algorithm_0',
    main_file_name='test.py',
    hyperparameter_config='{learning_rate:0.01}',
    train_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    train_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    model_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    model_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    learning=1,
    package_id=_setup_test_package1.id)

_setup_test_algorithm2 = AlgorithmTestInstance(
    id=generate_primary_key('ALGO'),
    name='setup_algorithm_not_learning',
    main_file_name='test.py',
    hyperparameter_config='{learning_rate:0.01}',
    train_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    train_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    model_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    model_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    learning=0,
    package_id=_setup_test_package1.id)

_setup_test_algorithm3 = AlgorithmTestInstance(
    id=generate_primary_key('ALGO'),
    name='setup_test_algorithm3',
    main_file_name='test.py',
    hyperparameter_config='{learning_rate:0.01}',
    train_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    train_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    model_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    model_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    learning=1,
    package_id=_setup_test_package1.id)

_setup_test_algorithm4 = AlgorithmTestInstance(
    id=generate_primary_key('ALGO'),
    name='setup_test_algorithm4',
    main_file_name='test.py',
    hyperparameter_config='{learning_rate:0.01}',
    train_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    train_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    model_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    model_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    learning=1,
    package_id=_setup_test_package1.id)

_setup_test_algorithm5 = AlgorithmTestInstance(
    id=generate_primary_key('ALGO'),
    name='setup_test_algorithm5',
    main_file_name='test.py',
    hyperparameter_config='{learning_rate:0.01}',
    train_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    train_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    model_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    model_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    learning=1,
    package_id=_setup_test_package1.id)

test_algorithm1 = AlgorithmTestInstance(
    id=generate_primary_key('ALGO'),
    name='test_algorithm_1',
    main_file_name='test.py',
    hyperparameter_config='{learning_rate:0.01}',
    train_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    train_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    model_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    model_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    learning=1,
    package_id=_setup_test_package1.id)

test_algorithm2 = AlgorithmTestInstance(
    id=generate_primary_key('ALGO'),
    name='test_algorithm_2',
    main_file_name='test.py',
    hyperparameter_config='{learning_rate:0.01}',
    train_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    train_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    model_input_pattern=[_setup_test_datapattern1.id, _setup_test_datapattern2.id],
    model_output_pattern=[_setup_test_datapattern3.id, _setup_test_datapattern4.id],
    learning=1,
    package_id=_setup_test_package1.id)
