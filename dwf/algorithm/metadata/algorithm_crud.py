# -*- coding:utf-8 -*-
#
# DataWay Algorithm SDK
# Initial Date: 2018.06.19
#
# Title: methods for metadata of algorithm
#
# Version 1.0
#

from dwf.ormmodels import *
from dwf.common.log import logger
from dwf.common.exception import *
from dwf.util.id import generate_primary_key, generate_primary_key_without_prefix


class AlgorithmCRUD:

    def __init__(self, db_session):
        self.db_session = db_session

    def add_algorithm(self, name, display_name, description, entry_name, algorithm_type, hyperparameter_config,
                      train_input_pattern, train_output_pattern,
                      model_input_pattern, model_output_pattern, runtime, learning=1, package_id=None):
        #    NO.A301
        #	     Add an algorithm into the metadata DB.
        #    Args:
        #        name - name of algorithm
        #        display_name - display name of algorithm
        #        discription - discription of algorithm
        #        entry_name - name of entry in the package
        #        hyperparameter_config - hyperparameter config
        #        train_input_pattern - [train_input_pattern_id1, train_input_pattern_id2 ...]
        #        train_output_pattern - [train_output_pattern_id1, train_output_pattern_id2 ...]
        #        model_input_pattern - [model_input_pattern_id1, model_input_pattern_id2 ...]
        #        model_output_pattern - [model_output_pattern_id1, model_output_pattern_id2 ...]
        #        runtime - running environment eg. xlearn.pytorch/ xlearn.tensorflow
        #        learning - whether it is a learning algorithm, 0/1
        #        package_id - id of package
        #    Returns:
        #	     Algorithm id
        #    Exceptions:
        #
        id = generate_primary_key('ALGO')
        create_time = datetime.now()

        algorithm = Algorithm(id=id,
                              subid=id,
                              creator='admin',
                              owner='admin',
                              last_modifier='admin',
                              create_time=create_time,
                              name=name,
                              display_name=display_name,
                              algorithm_type=algorithm_type,
                              description=description,
                              alg_input_patterns=train_input_pattern,
                              alg_output_patterns=train_output_pattern,
                              parameters=hyperparameter_config,
                              entry_name=entry_name,
                              available=1,
                              isbuiltin=0,
                              isdeleted=0,
                              islearning=learning,
                              model_input_patterns=model_input_pattern,
                              model_output_patterns=model_output_pattern,
                              package_id=package_id,
                              prog_language='python',
                              reference_count=0,
                              runtime=runtime
                              )
        self.db_session.add(algorithm)
        self.db_session.commit()
        return id

    def update_algorithm(self, algorithm_id, name=None, display_name=None, description=None, entry_name=None,
                         hyperparameter_config=None, train_input_pattern=None, train_output_pattern=None,
                         model_input_pattern=None, model_output_pattern=None, runtime=None, learning=None,
                         package_id=None):
        #    NO.A302
        #        Update a deep-learning algorithm into the metadata DB.
        #        Attention: It is DANGEROUS that the last last hyperparameter_config will be covered.
        #    Args:
        #        name - name of algorithm
        #        main_file_name - name of main file in the package
        #        hyperparameter_config - hyperparameter config
        #        train_input_pattern - [train_input_pattern_id1, train_input_pattern_id2 ...]
        #        train_output_pattern - [train_output_pattern_id1, train_output_pattern_id2 ...]
        #        model_input_pattern - [model_input_pattern_id1, model_input_pattern_id2 ...]
        #        model_output_pattern - [model_output_pattern_id1, model_output_pattern_id2 ...]
        #        example_model_id - id of example model
        #        learning - whether it is a learning algorithm
        #        package_id - id of package
        #    Returns:
        #        Algorithm id.
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.

        pending = self.db_session.query(Algorithm).get(algorithm_id)

        if pending is None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM

        if name is not None:
            pending.name = name

        if display_name is not None:
            pending.display_name = display_name

        if description is not None:
            pending.description = description

        if entry_name is not None:
            pending.entry_name = entry_name

        if hyperparameter_config is not None:
            pending.parameters = hyperparameter_config

        if train_input_pattern is not None:
            pending.alg_input_patterns = train_input_pattern

        if train_output_pattern is not None:
            pending.alg_output_patterns = train_output_pattern

        if model_input_pattern is not None:
            pending.model_input_patterns = model_input_pattern

        if model_output_pattern is not None:
            pending.model_output_patterns = model_output_pattern

        if runtime is not None:
            pending.runtime = runtime

        if learning is not None:
            pending.islearning = learning

        if package_id is not None:
            pending.package_id = package_id

        self.db_session.commit()
        return algorithm_id

    def query_algorithm(self, algorithm_id):
        #    NO.A312
        #	     Query algorithm information.
        #    Args：
        #	     algorithm_id - The ID of algorithm.
        #    Returns：
        #  	     algorithm_object
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm is None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM
        return algorithm

    def query_algorithms(self):
        #    NO.A313
        #        Add a deep-learning algorithm into the metadata DB.
        #    Args：
        #        algorithm_id - The ID of algorithm.
        #    Returns：
        #        algorithm_info
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        algorithms = self.db_session.query(Algorithm).all()
        return algorithms

    def delete_algorithm(self, algorithm_id):
        #    NO.A314
        #	     Set "deleted" of algorithm to False in the metadata DB. The algorithm cannot be used after deleted,
        #        It's still saved in DB. Thus when needed, deleted algorithms can be recovered.
        #        If an algorithm is running, it cannot be deleted.
        #    Args:
        #	     algorithm_id - The ID of algorithm.
        #    Returns:
        #	     None.
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        #        DELETE_FAILURE - The algorithm cannot be deleted.
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm is None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM
        algorithm.isdeleted = 1
        self.db_session.commit()

    def recover_algorithm(self, algorithm_id):
        #    NO.A315
        #        Recover deleted algorithm.
        #    Args：
        #        algorithm_id - The ID of algorithm.
        #    Returns：
        #        None.
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        #        NOT_DELETED - The algorithm is not deleted.
        #        RECOVER_FAILURE - The algorithm cannot be recovered.
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm is None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM
        algorithm.isdeleted = 0
        self.db_session.commit()

    def make_algorithm_unavailable(self, algorithm_id):
        #    NO.A316
        #        Make one algorithm unavailable --- cannot be used in tasks.
        #    Args：
        #        algorithm_id - The ID of algorithm.
        #    Returns：
        #        None.
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm is None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM
        algorithm.available = 0
        self.db_session.commit()

    def clean_algorithm(self, algorithm_id):
        #    NO.A317
        #	     Set "deleted" of algorithm to False in the metadata DB. The algorithm cannot be used after deleted,
        #        It's still saved in DB. Thus when needed, deleted algorithms can be recovered.
        #        If an algorithm is using, it cannot be deleted.
        #    Args:
        #	     algorithm_id - The ID of algorithm.
        #    Returns:
        #	     None.
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        #        DELETE_FAILURE - The algorithm cannot be deleted.
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm is None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM
        self.db_session.delete(algorithm)
        self.db_session.commit()

    def resolve_hyperparameter(self, package_id, main_file_name):
        #    NO.A323
        #        Resolve Hyperparameter.
        #    Args:
        #        package_id - The id of package.
        #        main_file_name - The name of main file.
        #    Returns:
        #        hyperparameter - Json file.
        #    Exceptions:
        #	 NO_EXISTING_PACKAGE - The package doesn't exist.
        #	 NO_EXISTING_MAIN_FILE - The main file doesn't exist.
        #	 RESOLVE_FAILURE - Fail to resolve hyperparamter from main file.
        return
