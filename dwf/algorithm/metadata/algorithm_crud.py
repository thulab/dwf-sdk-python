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

    def add_algorithm(self, name, main_file_name, hyperparameter_config, train_input_pattern, train_output_pattern,
                      model_input_pattern, model_output_pattern, learning=1, package_id=None):
        #    NO.A301
        #	     Add an algorithm into the metadata DB.
        #    Args:
        #        name - name of algorithm
        #        main_file_name - name of main file in the package
        #        hyperparameter_config - hyperparameter config
        #        train_input_pattern - [train_input_pattern_id1, train_input_pattern_id2 ...]
        #        train_output_pattern - [train_output_pattern_id1, train_output_pattern_id2 ...]
        #        model_input_pattern - [model_input_pattern_id1, model_input_pattern_id2 ...]
        #        model_output_pattern - [model_output_pattern_id1, model_output_pattern_id2 ...]
        #        example_model_id - id of example model
        #        learning - whether it is a learning algorithm, 0/1
        #        package_id - id of package
        #    Returns:
        #	     Algorithm id
        #    Exceptions:
        #
        id = generate_primary_key('ALGO')
        create_time = datetime.now()

        # 如果是学习类算法，增加model对象，获取example_model_id
        # example_model的名字采用“***算法示例模型”
        # example_model_id = ....
        if learning == 1:
            example_model_id = generate_primary_key('MODE')
            example_model = Model(id=example_model_id,
                                  name=str(name) + ' example model',
                                  description=str(name) + ' example model',
                                  create_time=datetime.now(),
                                  model_path='xlearn/models')
            self.db_session.add(example_model)

            model_input_pattern_id_index = 1
            for input_pattern_id in model_input_pattern:
                model_input_id = generate_primary_key_without_prefix()
                model_input_data_pattern = ModelInputDataPatterns(id=model_input_id,
                                                                  model_id=example_model_id,
                                                                  pattern_id=input_pattern_id,
                                                                  index=model_input_pattern_id_index)
                self.db_session.add(model_input_data_pattern)
                model_input_pattern_id_index = model_input_pattern_id_index + 1

            model_output_pattern_id_index = 1
            for output_pattern_id in model_output_pattern:
                model_output_id = generate_primary_key_without_prefix()
                model_output_data_pattern = ModelOutputDataPatterns(id=model_output_id,
                                                                    model_id=example_model_id,
                                                                    pattern_id=output_pattern_id,
                                                                    index=model_output_pattern_id_index)
                self.db_session.add(model_output_data_pattern)
                model_output_pattern_id_index = model_output_pattern_id_index + 1
        else:
            example_model_id = None

        algorithm = Algorithm(id=id, create_time=create_time, name=name, main_file_name=main_file_name,
                              hyperparameter_config=hyperparameter_config, example_model_id=example_model_id,
                              learning=learning, available=1, package_id=package_id)
        self.db_session.add(algorithm)

        input_pattern_id_index = 1
        for input_pattern_id in train_input_pattern:
            algo_input_id = generate_primary_key_without_prefix()
            algorithm_input_data_pattern = AlgorithmInputDataPatterns(id=algo_input_id, algorithm_id=id,
                                                                      pattern_id=input_pattern_id,
                                                                      index=input_pattern_id_index)
            self.db_session.add(algorithm_input_data_pattern)
            input_pattern_id_index = input_pattern_id_index + 1

        output_pattern_id_index = 1
        for output_pattern_id in train_output_pattern:
            algo_output_id = generate_primary_key_without_prefix()
            algorithm_output_data_pattern = AlgorithmOutputDataPatterns(id=algo_output_id, algorithm_id=id,
                                                                        pattern_id=output_pattern_id,
                                                                        index=output_pattern_id_index)
            self.db_session.add(algorithm_output_data_pattern)
            output_pattern_id_index = output_pattern_id_index + 1

        self.db_session.commit()
        return id

    def update_algorithm(self, algorithm_id, name=None, main_file_name=None, hyperparameter_config=None,
                         train_input_pattern=None,
                         train_output_pattern=None, model_input_pattern=None, model_output_pattern=None,
                         example_model_id=None, learning=None, package_id=None):
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
        #        ADD_FAILURE - Fail to add this algorithm.
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)

        if name is not None:
            algorithm.name = name

        if main_file_name is not None:
            algorithm.main_file_name = main_file_name

        if hyperparameter_config is not None:
            algorithm.hyperparameter_config = hyperparameter_config

        if train_input_pattern is not None:
            self.db_session.query(AlgorithmInputDataPatterns).filter(
                AlgorithmInputDataPatterns.algorithm_id == algorithm_id).delete()
            input_pattern_id_index = 1
            for input_pattern_id in train_input_pattern:
                algo_input_id = generate_primary_key_without_prefix()
                algorithm_input_data_pattern = AlgorithmInputDataPatterns(id=algo_input_id, algorithm_id=algorithm_id,
                                                                          pattern_id=input_pattern_id,
                                                                          index=input_pattern_id_index)
                self.db_session.add(algorithm_input_data_pattern)
                input_pattern_id_index = input_pattern_id_index + 1

        if train_output_pattern is not None:
            self.db_session.query(AlgorithmOutputDataPatterns).filter(
                AlgorithmOutputDataPatterns.algorithm_id == algorithm_id).delete()
            output_pattern_id_index = 1
            for output_pattern_id in train_output_pattern:
                algo_output_id = generate_primary_key_without_prefix()
                algorithm_output_data_pattern = AlgorithmOutputDataPatterns(id=algo_output_id,
                                                                            algorithm_id=algorithm_id,
                                                                            pattern_id=output_pattern_id,
                                                                            index=output_pattern_id_index)
                self.db_session.add(algorithm_output_data_pattern)
                output_pattern_id_index = output_pattern_id_index + 1

        if example_model_id is not None:
            algorithm.example_model_id = example_model_id

        if learning is not None:
            if learning == 1 and (algorithm.example_model_id is None) and (example_model_id is None):
                # 修改非学习算法为算法时，未传入示例模型，则新建示例模型
                example_model_id = generate_primary_key('MODE')
                example_model = Model(id=example_model_id,
                                      name=str(name) + ' example model',
                                      description=str(name) + ' example model',
                                      create_time=datetime.now(),
                                      model_path='xlearn/models')
                self.db_session.add(example_model)
                model_input_pattern_id_index = 1
                for input_pattern_id in model_input_pattern:
                    model_input_id = generate_primary_key_without_prefix()
                    model_input_data_pattern = ModelInputDataPatterns(id=model_input_id,
                                                                      model_id=example_model_id,
                                                                      pattern_id=input_pattern_id,
                                                                      index=model_input_pattern_id_index)
                    self.db_session.add(model_input_data_pattern)
                    model_input_pattern_id_index = model_input_pattern_id_index + 1

                model_output_pattern_id_index = 1
                for output_pattern_id in model_output_pattern:
                    model_output_id = generate_primary_key_without_prefix()
                    model_output_data_pattern = ModelOutputDataPatterns(id=model_output_id,
                                                                        model_id=example_model_id,
                                                                        pattern_id=output_pattern_id,
                                                                        index=model_output_pattern_id_index)
                    self.db_session.add(model_output_data_pattern)
                    model_output_pattern_id_index = model_output_pattern_id_index + 1
                algorithm.example_model_id = example_model_id
            elif learning == 0 and algorithm.example_model_id is not None:
                self. db_session.query(Model).filter(Model.id == algorithm.example_model_id).delete()
                algorithm.example_model_id = None

            algorithm.learning = learning

        if package_id is not None:
            algorithm.package_id = package_id

        self.db_session.commit()
        return id

    def query_algorithm(self, algorithm_id):
        #    NO.A312
        #	     Query algorithm information.
        #    Args：
        #	     algorithm_id - The ID of algorithm.
        #    Returns：
        #  	     algorithm_object
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        # TODO check 是否存在
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm == None:
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
        #  TODO check 是否存在
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm == None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM
        algorithm.deleted = 1
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
        #  TODO check 是否存在
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm is None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM
        algorithm.deleted = 0
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
        return

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
        #  TODO check 是否存在
        algorithm = self.db_session.query(Algorithm).get(algorithm_id)
        if algorithm is None:
            logger.error('Algorithm is not found')
            raise NON_EXISTING_ALGORITHM
        self.db_session.delete(algorithm)
        self.db_session.commit()

    def query_algorithms_tree(self, root_id, depth):
        #    NO.A300
        #        Query a complete or partial tree of algorithms representing the function hierarchy of algorithms.
        #    Args:
        #        root_id - The id of the root node of the tree being queried. Default value is None meaning the complete tree.
        #        depth	- The depth of children that would be returned. Default value is None meaning the whole subtree.
        #    Returns:
        #        algorithms_tree - Queried tree of algorithms which contains nodes representing category, problem and algorithms.
        #        Format:
        #        {
        #	  	     root_id:"***",
        #            nodes :
        #            {
        #	  	         node_id1:{
        #	  				id:"***",
        #                    			type:"***",
        #	  				name:"***",
        #	  				description:"***",
        #	  				son_id:["***","***"...]
        #	  		     },
        #		         node_id2:{
        #	  				id:"***",
        #                    			type:"***",
        #	  				name:"***",
        #	  				description:"***",
        #	  				son_id:["***","***"...]
        #	  		     }
        #	  		     ...
        #            }
        #        }
        #    Exceptions:
        #	     NON_EXISTING_NODE - The given root_id does not exist.
        return

    def query_criterions(self):
        #    NO.A301
        #        Query all criterions.
        #    Args：
        #        None.
        #    Returns：
        #        {
        #            criterion_id1:{
        #                id:"***",
        #                name:"***",
        #                description:"***"
        #            },
        #            criterion_id2:{
        #                id:"***",
        #                name:"***",
        #                description:"***"
        #            }
        #            ...
        #        }
        return

    def query_criterion(self, criterion_id):
        #    NO.A302
        #        Query one criterion.
        #    Args：
        #        criterion_id - The id of criterion.
        #    Returns：
        #    {
        #        id:"***",
        #        name:"***",
        #        description:"***"
        #    }
        return

    def query_patterns(self):
        #    NO.A303
        #        Query all kinds of patterns.
        #    Args:
        #        None.
        #    Returns:
        #        {
        #            pattern_id1:{
        #                id:"***",
        #                name:"***",
        #                format:"***",
        #                description:"***"
        #            },
        #            pattern_id2:{
        #                id:"***",
        #                name:"***",
        #                format:"***",
        #                description:"***"
        #            }
        #            ...
        #        }
        return

    def attach_datasets_to_problem(self, problem_id, dataset_list):
        #    NO.A304
        #        Attach one reference to the problem.
        #    Args:
        #        dataset_list - The id of dataset group.
        #        problem_id - The id of problem.
        #    Returns：
        #        None.
        #    Exceptions:
        #        ATTACH_FAILURE - Fail to attach reference.
        return

    def query_algorithm_config(self, algorithm_id):
        #    NO.A307
        #	     Query algorithm config, including data types and formats of inputs and outputs, together with the hyperparameters of the algorithm.
        #    Args:
        #        algorithm_id - The id of the queried algorithm.
        #    Returns:
        #        algorithm_config - The id of input_pattern, id of output_pattern and hyperparameter of algorithm.
        #    Format:
        #        {
        #     	      "input_pattern_id": [train_input_pattern_id1, train_input_pattern_id2 ...], [test_input_pattern_id1, test_input_pattern_id2 ...],
        #     	      "output_pattern_id": [train_output_pattern_id1, train_output_pattern_id2 ...], [test_output_pattern_id1, test_output_pattern_id2 ...],
        #     	      "hyperparameters":[
        #                  {
        #                       name:"***",
        #                       default:"***",
        #                       suggest:"***", # 1: suggest to tune, 0: not recommend to tune
        #                       scope:"***", # range: <1,10> , choice: [3,4,5]
        #                       type:"***", # eg. str, int, float
        #                       description:"***",
        #                       index:"***"
        #                   },
        #                   {
        #                       name:"***",
        #                       default:"***",
        #                       suggest:"***",
        #                       scope:"***",
        #                       type:"***",
        #                       description:"***",
        #                       index:"***"
        #                   }
        #                   ...
        #            ]
        #    }
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        return

    def query_algorithm_knowledge(self, algorithm_id):
        #    NO.A308
        #        Query algorithm knowledge, including instructions and evaluations of queried algorithm.
        #    Args:
        #        algorithm_id - The id of the queried algorithm.
        #    Returns:
        #        algorithm_knowledge - Documentations, problems this algorithm can solve and evaluations of algorithm.
        #    Format:
        #        {
        #      	      "documentation":"***",
        #             "problems":[problem_id1, problem_id2 ...],
        #      	      "evaluations": [
        #                 {
        #      				  "evaluation_criterion":"***",
        #      				  "dataset_name":"***",
        #      				  "criterion_value":"***",
        #      				  "hyperparameter_setting":"***"
        #      			  },
        #      			  {
        #      				  "evaluation_criterion":"***",
        #      			      "dataset_name":"***",
        #      			      "criterion_value":"***",
        #      			      "hyperparameter_setting":"***"
        #      			  }
        #      			  ...
        #      	     ]
        #        }
        #    Exceptions:
        #        NON_EXISTING_ALGORITHM - The given algorithm_id does not exist.
        return

    def query_problem_knowledge(self, problem_id):
        #    NO.A309
        #        Query knowledge of problems, including description of that problem and the list of algorithms that solve the problem. The list should contain the comparison of the algorithms.
        #    Args:
        #        problem_id - The id of the queried problem.
        #    Returns:
        #        problem_knowledge - Description of the problem and algorithms attached to this problem.
        #    Format:
        #        {
        #      	     "description": "***",
        #      	     "algorithms": {
        #                 algorithm_id1:{
        #                     id:"***",
        #                     name:"***"
        #                 }
        #                 algorithm_id2:{
        #                     id:"***",
        #                     name:"***"
        #                 }
        #                 ...
        #             },
        #             "evaluations":{
        #                 dataset_id1:{
        #                     algorithm_id:[algorithm_id1, algorithm_id2 ...],
        #                     criterion_id:[criterion_id1, criterion_id2 ...],
        #                     crterion_value:[
        #                         [algorithm1_criterion1, algorithm1_criterion2 ...]
        #                         [algorithm2_criterion1, algorithm2_criterion2 ...]
        #                         ...
        #                     ],
        #                     hyperparameter_setting:[algorithm1_hyperparameter_setting, algorithm2_hyperparameter_setting ...]
        #                 }
        #                 dataset_id2:{
        #                     algorithm_id:[algorithm_id1, algorithm_id2 ...],
        #                     criterion_id:[criterion_id1, criterion_id2 ...],
        #                     crterion_value:[
        #                         [algorithm1_criterion1, algorithm1_criterion2 ...]
        #                         [algorithm2_criterion1, algorithm2_criterion2 ...]
        #                         ...
        #                     ],
        #                     hyperparameter_setting:[algorithm1_hyperparameter_setting, algorithm2_hyperparameter_setting ...]
        #                 }
        #                 ...
        #            }
        #        }
        #    Exceptions:
        #        NON_EXISTING_problem - The given problem_id does not exist.
        return

    def update_hyperparameter_config(self, algorithm_id, hyperparameter_config):
        #    NO.A318
        #        Add one new package, create a new conda or find an existed conda according to requirement_list.
        #    Args：
        #        algorithm_id - The id of algorithm.
        #        hyperparameter_config - Hyperparameter config of this algorithm.
        #    Returns：
        #	     None.
        #    Exceptions:
        #        UPDATE_FAILURE
        return

    def resolve_hyperparameter_config(self, package_id, main_file):
        #    NO.A319
        #        Add one new package, create a new conda or find an existed conda according to requirement_list.
        #    Args：
        #        package_id - The id of package.
        #	     main_file - The main file of algorithm whose hyperparameter is to be resolved in the package.
        #    Returns：
        #	     None.
        #    Exceptions:
        #        RESOLVE_FAILURE

        return

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
