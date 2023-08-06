import teradataml as tdml
import re
from tdstone.code import create_code_repository
from tdstone.model import create_model_repository, create_code_model_view
from tdstone.trained_model import create_trained_model_repository, create_code_model_trained_model_view,create_error_trained_model_repository,create_code_model_error_trained_model_view
from tdstone.scoring_results import create_scoring_results

from tdstone.mapper.feature import create_mapper_feature, create_mapper_feature_description
from tdstone.mapper.training import create_mapper_training, create_mapper_training_description
from tdstone.mapper.scoring import create_mapper_scoring, create_mapper_scoring_description
from tdstone.utils import execute_querydictionary
from tdstone.feature_store import insert_new_process, feature_store,create_features_table

from tdstone.prepared_dataset import prepared_new_colums_sql,preparedataset_from_table
import os
import base64
import json


def reformat(df, arguments):
    import pandas as pd
    Params_STO = arguments['sto_parameters']
    # Cast the columns
    for c in Params_STO["float_columnames"]:
        if len(c) > 0:
            try:
                df[c] = pd.to_numeric(df[c])
            except Exception as e:
                STO_OUPTUT_DEFAULT_STATUS = f'{{"error": "failed", "info": "column {c} cannot be converted to float Python {e}"}}'
                print(STO_OUPTUT_DEFAULT_STATUS)
    for c in Params_STO["integer_columnames"]:
        if len(c) > 0:
            try:
                df[c] = df[c].astype('int')
            except Exception as e:
                STO_OUPTUT_DEFAULT_STATUS = f'{{"error": "failed", "info": "column {c} cannot be converted to int Python {e}"}}'
                print(STO_OUPTUT_DEFAULT_STATUS)
    for c in Params_STO["category_columns"]:
        if len(c) > 0:
            try:
                df[c] = df[c].astype('category')
            except Exception as e:
                STO_OUPTUT_DEFAULT_STATUS = f'{{"error": "failed", "info": "column {c} cannot be converted to category Python {e}"}}'
                print(STO_OUPTUT_DEFAULT_STATUS)

    return df

file_list = ['feature_engineering','feature_engineering_reducer','training','scoring','feature_engineering_jsonoutput']
this_dir, this_filename = os.path.split(__file__)



def mapper_get_dataset_(id_mapper, sto_mapper_description):
    # get the dataset related to a specific mapper
    #
    # id_mapper : int. id of the mapper
    # sto_mapper_description : str. the mapper table nam.

    query = f'''SEL 
        DATASET_OBJECT
    ,   COL_ID_ROW
    ,   COL_ID_PARTITION
    ,   COL_FOLD
    FROM {sto_mapper_description}
    WHERE ID = {id_mapper}'''

    #print(query)
    # get the dataset table
    try:
        res = tdml.get_context().execute(query).fetchall()[0]
    except Exception as e:
        print(f'the id_mapper = {id_mapper} may not exist in {sto_mapper_description}. Please check.')
        return
    return (res[0].replace('"',''),eval("['"+"','".join(res[1].split(','))+"']"),eval("['"+"','".join(res[2].split(','))+"']"),res[3])

def create_view_on_clause(on_clause_view_name, prepared_dataset_name, mapper_table, ID_MAPPER, model_code_view, **kwargs):


    # create the "on clause" view for the script table operator query
    #
    # on_clause : name of the "on clause" view to be created
    # prepared_dataset : name of the prepared dataset view or table. a prepared dataset is a view or table that contains
    # the columns STO_ROW_ID (VARCHAR), STO_PARTITION_ID (VARCHAR), STO_FOLD_ID (VARCHAR) at the end in this order.
    # mapper_table : the name of the mapper table that will be used with the script table operator query
    # ID_MAPPER : the id of the mapper to apply for this operation
    # model_code_view : the name of the view containing the code, the parameters and eventually the trained models
    # selected_fold : the fold to be selected, for example

    if 'STO_FOLD_ID' in tdml.DataFrame(tdml.in_schema(prepared_dataset_name.split('.')[0],prepared_dataset_name.split('.')[1])).columns:
        sql_query = f"""
            REPLACE VIEW {on_clause_view_name} AS
            WITH LEFT_MAPPED_TABLE AS (
                SEL 
                    A.*
                ,	ROW_NUMBER() OVER (PARTITION BY A.STO_PARTITION_ID, A.STO_FOLD_ID, MAPPER.ID_MODEL ORDER BY A.STO_ROW_ID) AS STO_FAKE_ROW
                ,	MAPPER.ID_MODEL AS STO_MODEL_ID
                FROM {prepared_dataset_name} A
                ,	(CURRENT VALIDTIME SEL * FROM {mapper_table}) MAPPER
                WHERE A.STO_PARTITION_ID = MAPPER.ID_PARTITION
                AND MAPPER.ID = {ID_MAPPER} AND MAPPER.STATUS = 'enabled'
            )
            SEL
                LEFT_MAPPED_TABLE.*
            ,	CASE WHEN LEFT_MAPPED_TABLE.STO_FAKE_ROW = 1 THEN CURRENT_MODELS.CODE_TYPE END AS STO_CODE_TYPE
            ,	CASE WHEN LEFT_MAPPED_TABLE.STO_FAKE_ROW = 1 THEN TRANSLATE(FROM_BYTES(CURRENT_MODELS.CODE, 'base64m') USING UNICODE_TO_LATIN) END AS STO_CODE
            ,	CASE WHEN LEFT_MAPPED_TABLE.STO_FAKE_ROW = 1 THEN REGEXP_REPLACE(REGEXP_REPLACE(CAST(CURRENT_MODELS.ARGUMENTS AS VARCHAR(32000)),'([\r|\t])', ''),'[\s+]', ' ') END AS ARGUMENTS
            FROM
                LEFT_MAPPED_TABLE
            LEFT JOIN (
                CURRENT VALIDTIME SEL
                  ID_MODEL as ID
                , CODE_TYPE
                , CODE
                , ARGUMENTS
                FROM
                {model_code_view}
                WHERE CODE_TYPE = 'python class MyModel'
            ) CURRENT_MODELS
            ON LEFT_MAPPED_TABLE.STO_MODEL_ID = CURRENT_MODELS.ID;    
        """
    else:
        sql_query = f"""
            REPLACE VIEW {on_clause_view_name} AS
            WITH LEFT_MAPPED_TABLE AS (
                SEL 
                    A.*
                ,	ROW_NUMBER() OVER (PARTITION BY A.STO_PARTITION_ID, MAPPER.ID_MODEL ORDER BY A.STO_ROW_ID) AS STO_FAKE_ROW
                ,	MAPPER.ID_MODEL AS STO_MODEL_ID
                FROM {prepared_dataset_name} A
                ,	(CURRENT VALIDTIME SEL * FROM {mapper_table}) MAPPER
                WHERE A.STO_PARTITION_ID = MAPPER.ID_PARTITION
                AND MAPPER.ID = {ID_MAPPER} AND MAPPER.STATUS = 'enabled'
            )
            SEL
                LEFT_MAPPED_TABLE.*
            ,	CASE WHEN LEFT_MAPPED_TABLE.STO_FAKE_ROW = 1 THEN CURRENT_MODELS.CODE_TYPE END AS STO_CODE_TYPE
            ,	CASE WHEN LEFT_MAPPED_TABLE.STO_FAKE_ROW = 1 THEN TRANSLATE(FROM_BYTES(CURRENT_MODELS.CODE, 'base64m') USING UNICODE_TO_LATIN) END AS STO_CODE
            ,	CASE WHEN LEFT_MAPPED_TABLE.STO_FAKE_ROW = 1 THEN REGEXP_REPLACE(REGEXP_REPLACE(CAST(CURRENT_MODELS.ARGUMENTS AS VARCHAR(32000)),'([\r|\t])', ''),'[\s+]', ' ') END AS ARGUMENTS
            FROM
                LEFT_MAPPED_TABLE
            LEFT JOIN (
                CURRENT VALIDTIME SEL
                  ID_MODEL as ID
                , CODE_TYPE
                , CODE
                , ARGUMENTS
                FROM
                {model_code_view}
                WHERE CODE_TYPE = 'python class MyModel'
            ) CURRENT_MODELS
            ON LEFT_MAPPED_TABLE.STO_MODEL_ID = CURRENT_MODELS.ID;    
        """

    con = tdml.get_connection()

    con.execute(sql_query)
    print(f'view {on_clause_view_name} successfully created')
    return sql_query

class sto_framework():

    def __init__(self,database,feature_store,
                 SEARCHUIFDBPATH=re.findall(string=str(tdml.get_context().url),pattern=r'DATABASE=(\w+)')[0],
                 rootname='STO'):
        self.database = database
        self.SEARCHUIFDBPATH = SEARCHUIFDBPATH
        self.code_repository = f'{database}.{rootname}_CODES'
        self.model_repository = f'{database}.{rootname}_MODELS'
        self.code_model_view = f'{database}.{rootname}_MODELS_WITH_CODE'


        self.trained_model_repository = f'{database}.{rootname}_TRAINED_MODELS'
        self.code_model_trained_model_view = f'{database}.{rootname}_TRAINED_MODELS_WITH_MODELS_WITH_CODE'
        self.error_trained_model_repository = f'{database}.{rootname}_ERROR_TRAINED_MODELS'
        self.error_feature_engineering      = f'{database}.{rootname}_ERROR_FEATURE_ENGINEERING'
        self.code_model_error_trained_model_view = f'{database}.{rootname}_ERROR_TRAINED_MODELS_WITH_MODELS_WITH_CODE'
        self.code_model_error_feature_engineering_view = f'{database}.{rootname}_ERROR_FEATURE_ENGINEERING_WITH_MODELS_WITH_CODE'

        self.mapper_feature = f'{database}.{rootname}_MAPPER_FEATURE'
        self.mapper_feature_description = f'{database}.{rootname}_MAPPER_FEATURE_DESCRIPTION'
        self.mapper_training = f'{database}.{rootname}_MAPPER_TRAINING'
        self.mapper_training_description = f'{database}.{rootname}_MAPPER_TRAINING_DESCRIPTION'
        self.mapper_scoring = f'{database}.{rootname}_MAPPER_SCORING'
        self.mapper_scoring_description = f'{database}.{rootname}_MAPPER_SCORING_DESCRIPTION'
        self.process_input_output = f'{database}.{feature_store.rootname}_MAPPER_SCORING_DESCRIPTION'
        self.feature_store = feature_store

    def setup(self):
        sql_queries = {}
        sql_queries['code_repository'] = create_code_repository(self.code_repository)
        sql_queries['model_repository'] = create_model_repository(self.model_repository)
        sql_queries['code_model_view'] = create_code_model_view(self.code_model_view,
                                                                self.code_repository,
                                                                self.model_repository)



        sql_queries['mapper_feature'] = create_mapper_feature(self.mapper_feature)
        sql_queries['mapper_feature_secondary_index'] = f'CREATE INDEX (ID_PARTITION) ON {self.mapper_feature};'
        sql_queries['mapper_feature_description'] = create_mapper_feature_description(self.mapper_feature_description)
        sql_queries['mapper_training'] = create_mapper_training(self.mapper_training)
        sql_queries['mapper_training_description'] = create_mapper_training_description(self.mapper_training_description)
        sql_queries['mapper_scoring'] = create_mapper_scoring(self.mapper_scoring)
        sql_queries['mapper_scoring_description'] = create_mapper_scoring_description(self.mapper_scoring_description)

        sql_queries['trained_model_repository'] = create_trained_model_repository(self.trained_model_repository)
        sql_queries['code_model_trained_model_view'] = create_code_model_trained_model_view(self.code_model_trained_model_view,
                                                                                            self.code_model_view,
                                                                                            self.trained_model_repository)

        sql_queries['error_trained_model_repository'] = create_error_trained_model_repository(self.error_trained_model_repository)
        sql_queries['code_model_error_trained_model_view'] = create_code_model_error_trained_model_view(self.code_model_error_trained_model_view,
                                                                                            self.code_model_view,
                                                                                            self.error_trained_model_repository)
        sql_queries['error_feature_engineering'] = create_error_trained_model_repository(self.error_feature_engineering)
        sql_queries['code_model_error_feature_engineering_view'] = create_code_model_error_trained_model_view(self.code_model_error_feature_engineering_view,
                                                                                            self.code_model_view,
                                                                                            self.error_feature_engineering)
        execute_querydictionary(sql_queries)
        self.create_view_process_input_output()
        return

    def clean(self):
        try:
            tdml.db_drop_view(self.code_model_trained_model_view.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_view(self.code_model_view.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.code_repository.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.model_repository.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.mapper_feature.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.mapper_feature_description.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.mapper_training.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.mapper_training_description.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.mapper_scoring.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.mapper_scoring_description.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])

        try:
            tdml.db_drop_table(self.trained_model_repository.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.error_trained_model_repository.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(self.error_feature_engineering.split('.')[1])
        except Exception as e:
            print(str(e).split('\n')[0])


        return

    def install_sto_files(self):

        for filename in file_list:
              tdml.install_file(file_identifier=filename,
                              file_path=os.path.join(this_dir, "data", filename+".py"),
                              file_on_client = True, is_binary = False)

        return

    def remove_sto_file(self):

        for filename in file_list:
            tdml.remove_file(file_identifier=filename,force_remove=True)

        return


    def PushFile(self):

        con = tdml.get_connection()

        import os
        # set the searchuifdbpath

        query_1 = 'SET SESSION SEARCHUIFDBPATH = "{}"'.format(self.SEARCHUIFDBPATH)
        query_2 = 'DATABASE {}'.format(self.SEARCHUIFDBPATH)
        con.execute(query_1)
        con.execute(query_2)

        # print(queries)
        for filename in file_list:
            try:
                query = "CALL SYSUIF.REMOVE_FILE('{}',1);".format(filename)
                # print(query)
                con.execute(query)
                print(f'File {filename}.py removed in Vantage')
                queries += '\n'
                queries += query
                # print(query)
            except:
                print("the file did not exist")

            if os.name == 'nt':
                # print('windows')
                query = "CALL SYSUIF.INSTALL_FILE('{}','{}','cz!{}')".format(filename,
                                                                             filename+'.py',
                                                                             os.path.join(this_dir, "data", filename+".py").replace("\\", "/").split(
                                                                                 ':')[1])

            else:
                # print('linux')
                query = "CALL SYSUIF.INSTALL_FILE('{}','{}','cz!{}')".format(filename,
                                                                             filename+'.py',
                                                                             os.path.join(this_dir, "data", filename+".py"))

            # print(query)
            con.execute(query)
            print(f'File {filename}.py installed in Vantage')

        return

    def remove_mapper_feature(id_mapper, **kwargs):
        # remove an existing mapper for feature enginieering

        sql_query = f"""
            DELETE {self.mapper_feature_description} 
            WHERE ID = {id_mapper};
            DELETE {self.mapper_feature} 
            WHERE ID = {id_mapper};    
            """

        con = tdml.get_connection()

        con.execute(sql_query, code)

        return

    def mapper_feature_get_dataset(self, id_mapper,  **kwargs):
        return mapper_get_dataset_(id_mapper, self.mapper_feature_description)






    def insert_code(self, code_id, filename, metadata, model_type='python class MyModel'):
        # insert the code in the sto_code_repository table
        #
        # code_id : int. the unique ID of the repo.
        # sto_code_repository : str. the name of the sto code repository table
        # filename : the filename of the python file containing the code
        # metadata : json format. e.g.'{"author": "Denis Molin"}'
        # model_type : str. default is 'python class MyModel'

        sql_query = f"""
        CURRENT VALIDTIME INSERT INTO {self.code_repository}
        (ID, CODE_TYPE, CODE, METADATA)
         VALUES
        ({code_id}, '{model_type}', ?, '{str(metadata).replace("'", '"')}');
        """

        with open(filename, 'r') as file:
            code = file.read()

        con = tdml.get_connection()

        con.execute(sql_query, code)

        return sql_query

    def remove_code(self,code_id, **kwargs):
        # remove a deployed code

        sql_query = f"""
        DELETE {self.code_repository} WHERE ID = {code_id};
        """

        con = tdml.get_connection()

        con.execute(sql_query)

        return sql_query

    def update_code(self,code_id,  filename, **kwargs):
        # update an existing code

        sql_query = f"""
        CURRENT VALIDTIME UPDATE {self.code_repository}
        SET CODE   = ?
        WHERE ID = {code_id};
        """

        with open(filename, 'r') as file:
            code = file.read()

        con = tdml.get_connection()

        con.execute(sql_query, code.encode())

        return sql_query

    def insert_model(self,model_id, code_id, arguments, metadata):
        # insert a new model
        #
        # model_id : int. id of the new model
        # code_id : id of an existing code
        # arguments : json. two fields: sto_parameters and model_parameters
        # metadata : json. e.g. {"author": "Denis Molin"}

        sql_insert_query = f"""
        CURRENT VALIDTIME INSERT INTO {self.model_repository}
        (ID, ID_CODE, ARGUMENTS, METADATA) VALUES
        ({model_id}, {code_id}, '{str(arguments).replace("'", '"')}', '{str(metadata).replace("'", '"')}');    
        """

        con = tdml.get_connection()

        con.execute(sql_insert_query)

        return sql_insert_query

    def remove_model(self,model_id,  **kwargs):
        # remove a model

        sql_query = f"""
        DELETE {self.model_repository} WHERE ID = {model_id};
        """

        con = tdml.get_connection()

        con.execute(sql_query)

        return sql_query

    def update_model_arguments(self,model_id, arguments,  **kwargs):
        # update the arguements of an existing model

        sql_query = f"""
        CURRENT VALIDTIME UPDATE {self.model_repository}
        SET ARGUMENTS = '{str(arguments).replace("'", '"')}'
        WHERE ID = {model_id};
        """

        con = tdml.get_connection()

        con.execute(sql_query)

        return sql_query

    def get_codes(self):
        return tdml.DataFrame(tdml.in_schema(self.code_repository.split('.')[0],
                                             self.code_repository.split('.')[1]))

    def get_models(self):
        return tdml.DataFrame(tdml.in_schema(self.code_model_view.split('.')[0],
                                             self.code_model_view.split('.')[1]))

    def get_current_codes(self):
        query = f"""
        CURRENT VALIDTIME
        SELECT * FROM {self.code_repository}
        """
        return tdml.DataFrame.from_query(query)

    def get_current_models(self):
        query = f"""
        CURRENT VALIDTIME
        SELECT * FROM {self.code_model_view}
        """
        return tdml.DataFrame.from_query(query)

    #################################### MAPPER FEATURE ENGINEERING ###################################
    def insert_mapper_feature(self, id_mapper, id_row, id_partition, id_fold, dataset_object, metadata, **kwargs):
        # insert a new mapper for training engineering
        #
        # id_mapper : int.
        # dataset_object : str. name of the dataset table or view the mapper applies for.
        # metadata : dict. e.g. '{"author": "Denis Molin", "description": "computation of the "}'

        sql_query = f"""
        INSERT INTO {self.mapper_feature_description}
        (ID, DATASET_OBJECT, COL_ID_ROW , COL_ID_PARTITION , COL_FOLD , METADATA) VALUES
        ({id_mapper}, '{dataset_object}', '{id_row}', '{id_partition}', '{id_fold}', '{str(metadata).replace("'", '"')}');
        """

        print(sql_query)
        con = tdml.get_connection()

        con.execute(sql_query)

        return

    def remove_mapper_feature(self,id_mapper, **kwargs):
        # remove an existing mapper for feature enginieering

        sql_query = f"""
        DELETE {self.mapper_feature_description} 
        WHERE ID = {id_mapper};
        DELETE {self.mapper_feature} 
        WHERE ID = {id_mapper};    
        """

        con = tdml.get_connection()

        con.execute(sql_query)

        return sql_query



    def mapper_feature_get_dataset(self,id_mapper, **kwargs):

        return mapper_get_dataset_(id_mapper, self.mapper_feature_description)

    def map_mapper_feature_insert_all(self, id_mapper, id_model, metadata):
        # attribute the same model corresponding the the id_model to all partitions of the dataset object.
        # Note that the dataset object is already linked to the mapper.
        #
        # id_mapper : int. id of the mapper
        # id_model : int. id of the model
        # sto_mapper_training : str. name of the mapper training table
        # metadata : dict. e.g. {"author" :  "Denis Molin"}
        # sto_mapper_training_description : str. name of the mapper training description table

        # get the prepared dataset table/view name
        dataset_object, id_row, id_columns, _ = self.mapper_feature_get_dataset(id_mapper)
        sub_query = prepared_new_colums_sql(dataset_object.split('.')[0], dataset_object.split('.')[1], id_row,
                                            id_columns)

        # insert query of partition that are not attributed yet to this model
        sql_insert_query = f"""
        -- ADD A NEW MAPPER ON ALL CURVES APPLY MODEL 
        CURRENT VALIDTIME INSERT INTO {self.mapper_feature}
        (ID, ID_MODEL, ID_PARTITION, STATUS, METADATA)
        SELECT
            {id_mapper} AS ID
        ,	{id_model} AS ID_MODEL
        ,	ID_PARTITION
        ,	'enabled' AS STATUS
        ,   '{str(metadata).replace("'", '"')}'
        FROM (SEL DISTINCT STO_PARTITION_ID AS ID_PARTITION FROM ({sub_query}) A_) A
        WHERE ID_PARTITION NOT IN (
            SEL DISTINCT ID_PARTITION FROM {self.mapper_feature}
            WHERE ID = {id_mapper}
            AND ID_MODEL = {id_model}
        )
        ;    
        """

        con = tdml.get_connection()

        con.execute(sql_insert_query)

        return

    def map_mapper_feature_insert_some(self,id_mapper, mapper_dictionary, metadata):
        # map the partitions to the models as described in the mapper dictrionary {sto_partition_id : model_id}
        # Note that the dataset object is already linked to the mapper.
        #
        # id_mapper : int. id of the mapper
        # mapper_dictionary : dict. {sto_partition_id : model_id}
        # sto_mapper_training : str. name of the mapper training table
        # metadata : dict. e.g. {"author" :  "Denis Molin"}
        # sto_mapper_training_description : str. name of the mapper training description table

        # get the prepared dataset table/view name
        dataset_object, id_row, id_columns, _ = self.mapper_feature_get_dataset(id_mapper)
        sub_query = prepared_new_colums_sql(dataset_object.split('.')[0], dataset_object.split('.')[1], id_row, id_columns)

        con = tdml.get_connection()

        # insert query of partition that are not attributed yet to this model
        sql_insert_query = []
        for k, v in mapper_dictionary.items():
            sql_insert_query.append(f"""
            -- ADD A NEW MAPPER ON ALL CURVES APPLY MODEL 
            CURRENT VALIDTIME INSERT INTO {self.mapper_feature}
            (ID, ID_MODEL, ID_PARTITION, STATUS, METADATA)
            SELECT
                {id_mapper} AS ID
            ,	{v} AS ID_MODEL
            ,	'{k}' AS ID_PARTITION
            ,	'enabled' AS STATUS
            ,   '{str(metadata).replace("'", '"')}'
            FROM (SEL DISTINCT STO_PARTITION_ID AS ID_PARTITION FROM ( {sub_query}) A_) A
            WHERE ID_PARTITION NOT IN (
                SEL DISTINCT ID_PARTITION FROM {self.mapper_feature}
                WHERE ID = {id_mapper}
                AND ID_MODEL = {v}
            )
            AND ID_PARTITION = '{k}'
            ;    
            """
                                    )

        con.execute(''.join(sql_insert_query))

        return

    def get_mapper_feature(self):
        return tdml.DataFrame(tdml.in_schema(self.mapper_feature.split('.')[0],
                                             self.mapper_feature.split('.')[1]))

    def get_current_mapper_feature(self):
        query = f"""
         CURRENT VALIDTIME
         SELECT * FROM {self.mapper_feature}
         """
        return tdml.DataFrame.from_query(query)

    def get_current_models(self):
        query = f"""
         CURRENT VALIDTIME
         SELECT * FROM {self.code_model_view}
         """
        return tdml.DataFrame.from_query(query)
    #################################### MAPPER TRAINING ###################################
    def insert_mapper_training(self,id_mapper, id_row, id_partition, id_fold, dataset_object, metadata,  **kwargs):
        # insert a new mapper for training engineering
        #
        # id_mapper : int.
        # dataset_object : str. name of the dataset table or view the mapper applies for.
        # metadata : dict. e.g. '{"author": "Denis Molin", "description": "computation of the "}'

        sql_query = f"""
        INSERT INTO {self.mapper_training_description}
        (ID, DATASET_OBJECT, COL_ID_ROW , COL_ID_PARTITION , COL_FOLD , METADATA) VALUES
        ({id_mapper}, '{dataset_object}', '{id_row}', '{id_partition}', '{id_fold}', '{str(metadata).replace("'", '"')}');
        """

        print(sql_query)
        con = tdml.get_connection()

        con.execute(sql_query)

        return

    def remove_mapper_training(self,id_mapper, **kwargs):
        # remove an existing mapper for training enginieering

        sql_query = f"""
        DELETE {self.mapper_training_description} 
        WHERE ID = {id_mapper};
        DELETE {self.mapper_training} 
        WHERE ID = {id_mapper};    
        """

        con = tdml.get_connection()

        con.execute(sql_query)

        return

    def mapper_training_get_dataset(self,id_mapper, **kwargs):

        return mapper_get_dataset_(id_mapper, self.mapper_training_description)

    def map_mapper_training_insert_all(self, id_mapper, id_model, metadata):
        # attribute the same model corresponding the the id_model to all partitions of the dataset object.
        # Note that the dataset object is already linked to the mapper.
        #
        # id_mapper : int. id of the mapper
        # id_model : int. id of the model
        # sto_mapper_training : str. name of the mapper training table
        # metadata : dict. e.g. {"author" :  "Denis Molin"}
        # sto_mapper_training_description : str. name of the mapper training description table

        # get the prepared dataset table/view name
        dataset_object, id_row, id_columns, _ = self.mapper_training_get_dataset(id_mapper)
        sub_query = prepared_new_colums_sql(dataset_object.split('.')[0], dataset_object.split('.')[1], id_row,
                                            id_columns)

        # insert query of partition that are not attributed yet to this model
        sql_insert_query = f"""
        -- ADD A NEW MAPPER ON ALL CURVES APPLY MODEL 
        CURRENT VALIDTIME INSERT INTO {self.mapper_training}
        (ID, ID_MODEL, ID_PARTITION, STATUS, METADATA)
        SELECT
            {id_mapper} AS ID
        ,	{id_model} AS ID_MODEL
        ,	ID_PARTITION
        ,	'enabled' AS STATUS
        ,   '{str(metadata).replace("'", '"')}'
        FROM (SEL DISTINCT STO_PARTITION_ID AS ID_PARTITION FROM ({sub_query}) A_) A
        WHERE ID_PARTITION NOT IN (
            SEL DISTINCT ID_PARTITION FROM {self.mapper_training}
            WHERE ID = {id_mapper}
            AND ID_MODEL = {id_model}
        )
        ;    
        """

        con = tdml.get_connection()

        con.execute(sql_insert_query)

        return

    def map_mapper_training_insert_some(self, id_mapper, mapper_dictionary, metadata):
        # map the partitions to the models as described in the mapper dictrionary {sto_partition_id : model_id}
        # Note that the dataset object is already linked to the mapper.
        #
        # id_mapper : int. id of the mapper
        # mapper_dictionary : dict. {sto_partition_id : model_id}
        # sto_mapper_training : str. name of the mapper training table
        # metadata : dict. e.g. {"author" :  "Denis Molin"}
        # sto_mapper_training_description : str. name of the mapper training description table

        # get the prepared dataset table/view name
        dataset_object, id_row, id_columns, _ = self.mapper_training_get_dataset(id_mapper)
        sub_query = prepared_new_colums_sql(dataset_object.split('.')[0], dataset_object.split('.')[1], id_row, id_columns)

        con = tdml.get_connection()

        # insert query of partition that are not attributed yet to this model
        sql_insert_query = []
        for k, v in mapper_dictionary.items():
            sql_insert_query.append(f"""
            -- ADD A NEW MAPPER ON ALL CURVES APPLY MODEL 
            CURRENT VALIDTIME INSERT INTO {self.mapper_training}
            (ID, ID_MODEL, ID_PARTITION, STATUS, METADATA)
            SELECT
                {id_mapper} AS ID
            ,	{v} AS ID_MODEL
            ,	'{k}' AS ID_PARTITION
            ,	'enabled' AS STATUS
            ,   '{str(metadata).replace("'", '"')}'
            FROM (SEL DISTINCT STO_PARTITION_ID AS ID_PARTITION FROM ( {sub_query}) A_) A
            WHERE ID_PARTITION NOT IN (
                SEL DISTINCT ID_PARTITION FROM {self.mapper_training}
                WHERE ID = {id_mapper}
                AND ID_MODEL = {v}
            )
            AND ID_PARTITION = '{k}'
            ;    
            """
                                    )

        con.execute(''.join(sql_insert_query))

        return


    def get_mapper_training(self):
        return tdml.DataFrame(tdml.in_schema(self.mapper_training.split('.')[0],
                                             self.mapper_training.split('.')[1]))

    def get_current_mapper_training(self):
        query = f"""
          CURRENT VALIDTIME
          SELECT * FROM {self.mapper_training}
          """
        return tdml.DataFrame.from_query(query)

    def map_mapper_training_update_status_all(self, id_mapper, new_status):
        # attribute the same model corresponding the the id_model to all partitions of the dataset object.
        # Note that the dataset object is already linked to the mapper.
        #
        # id_mapper : int. id of the mapper
        # id_model : int. id of the model
        # sto_mapper_training : str. name of the mapper training table
        # metadata : dict. e.g. {"author" :  "Denis Molin"}
        # sto_mapper_training_description : str. name of the mapper training description table

        sql_query = f"""
         CURRENT VALIDTIME UPDATE {self.mapper_training}
         SET STATUS   = '{new_status}'
         WHERE ID = {id_mapper}
        """

        con = tdml.get_connection()

        con.execute(sql_insert_query)

        return

    def insert_new_training_process(self,id_process, process_type, id_mapper, model_code_view, prepared_dataset,
                                    on_clause, results, sto_database, **kwargs):


        process_type = 'sto_training'
        mapper_table = self.mapper_training
        model_code_view = self.code_model_view
        process_catalog = self.feature_store.process_catalog
        sto_database = self.SEARCHUIFDBPATH

        id_process
        process_type = 'sto_training'
        id_mapper
        model_code_view
        prepared_dataset
        on_clause
        results
        sto_database

        insert_new_process(id_process, process_type, id_mapper, model_code_view, prepared_dataset, on_clause, results,
                           sto_database)

        return

    def create_training_process(self, id_process, id_mapper, training_fold, **kwargs):


        # get the mapper informations
        dataset_name, id_row, id_partition, id_fold = self.mapper_training_get_dataset(id_mapper)

       # create prepared dataset view
        prepared_dataset_name = f"{self.database}.V_STO_PREP_{dataset_name.split('.')[1]}_{id_mapper}"
        preparedataset_from_table(schema = prepared_dataset_name.split('.')[0],
                                  view_name = prepared_dataset_name.split('.')[1],
                                  input_table_name = dataset_name.split('.')[1],
                                  input_schema_name = dataset_name.split('.')[0],
                                  ID_Columns=id_row, Partition=id_partition,
                                  FoldID=id_fold)

        # create on_clause_view
        on_clause_view_name = f"{self.database}.V_STO_ON_CLAUSE_{dataset_name.split('.')[1]}_{id_mapper}"
        mapper_table = self.mapper_training
        code_model_view = self.code_model_view
        create_view_on_clause(on_clause_view_name, prepared_dataset_name, mapper_table, id_mapper, code_model_view
                                  , **kwargs)


        # create the process
        if type(training_fold)==type([]):
            training_fold = ','.join(training_fold)

        new_training_process = {
            'id_process': id_process,
            'process_type': 'sto_training',
            'id_mapper': id_mapper,
            'model_code_view': self.code_model_view,
            'prepared_dataset': prepared_dataset_name,
            'on_clause': on_clause_view_name,
            'results': self.trained_model_repository,
            'error_results': self.error_trained_model_repository,
            'sto_database':self.SEARCHUIFDBPATH,
            'fold': training_fold,
            'process_catalog':self.feature_store.process_catalog
        }

        insert_new_process(**new_training_process)

        return

    def create_feature_engineering_aggregate_process(self, id_process, id_mapper,  **kwargs):


        # get the mapper informations
        dataset_name, id_row, id_partition, id_fold = self.mapper_feature_get_dataset(id_mapper)

       # create prepared dataset view
        prepared_dataset_name = f"{self.database}.V_STO_PREP_FEATENGAGG_{dataset_name.split('.')[1]}_{id_mapper}"
        preparedataset_from_table(schema = prepared_dataset_name.split('.')[0],
                                  view_name = prepared_dataset_name.split('.')[1],
                                  input_table_name = dataset_name.split('.')[1],
                                  input_schema_name = dataset_name.split('.')[0],
                                  ID_Columns=id_row, Partition=id_partition,
                                  FoldID=id_fold)

        # create on_clause_view
        on_clause_view_name = f"{self.database}.V_STO_ON_CLAUSE_FEATENGAGG_{dataset_name.split('.')[1]}_{id_mapper}"
        mapper_table = self.mapper_feature
        code_model_view = self.code_model_view
        create_view_on_clause(on_clause_view_name, prepared_dataset_name, mapper_table, id_mapper, code_model_view
                                  , **kwargs)

        feature_store_table_float,feature_store_table_integer,feature_store_table_varchar, feature_store_table_json = create_features_table(self.feature_store.database,dataset_name.split('.')[-1]+'_AGG','aggregated')

        # create the process
        new_process = {
            'id_process': id_process,
            'process_type': 'sto_feature_engineering_agg',
            'id_mapper': id_mapper,
            'model_code_view': self.code_model_view,
            'prepared_dataset': prepared_dataset_name,
            'on_clause': on_clause_view_name,
            'results': ','.join([feature_store_table_float,feature_store_table_integer,feature_store_table_varchar,feature_store_table_json]),
            'error_results': self.error_feature_engineering,
            'sto_database':self.SEARCHUIFDBPATH,
            'fold': 'all',
            'process_catalog':self.feature_store.process_catalog
        }

        insert_new_process(**new_process)

        return

    def create_feature_engineering_rowlevel_process(self, id_process, id_mapper, **kwargs):


        # get the mapper informations
        dataset_name, id_row, id_partition, id_fold = self.mapper_feature_get_dataset(id_mapper)

       # create prepared dataset view
        prepared_dataset_name = f"{self.database}.V_STO_PREP_FEATENGROW_{dataset_name.split('.')[1]}_{id_mapper}"
        preparedataset_from_table(schema = prepared_dataset_name.split('.')[0],
                                  view_name = prepared_dataset_name.split('.')[1],
                                  input_table_name = dataset_name.split('.')[1],
                                  input_schema_name = dataset_name.split('.')[0],
                                  ID_Columns=id_row, Partition=id_partition,
                                  FoldID=id_fold)

        # create on_clause_view
        on_clause_view_name = f"{self.database}.V_STO_ON_CLAUSE_FEATENGROW_{dataset_name.split('.')[1]}_{id_mapper}"
        mapper_table = self.mapper_feature
        code_model_view = self.code_model_view
        create_view_on_clause(on_clause_view_name, prepared_dataset_name, mapper_table, id_mapper, code_model_view
                                  , **kwargs)

        feature_store_table_float, feature_store_table_integer, feature_store_table_varchar, feature_store_table_json = create_features_table(
            self.feature_store.database, dataset_name.split('.')[-1], 'rowlevel')

        # create the process
        new_process = {
            'id_process': id_process,
            'process_type': 'sto_feature_engineering_row_level',
            'id_mapper': id_mapper,
            'model_code_view': self.code_model_view,
            'prepared_dataset': prepared_dataset_name,
            'on_clause': on_clause_view_name,
            'results': ','.join([feature_store_table_float,feature_store_table_integer,feature_store_table_varchar,feature_store_table_json]),
            'error_results': self.error_feature_engineering,
            'sto_database':self.SEARCHUIFDBPATH,
            'fold': 'all',
            'process_catalog':self.feature_store.process_catalog
        }

        insert_new_process(**new_process)

        return

    def create_view_process_input_output(self):
        # create a view that describes the input and the output of the process

        sql_create_view = f"""
            -- GET THE INPUT AND THE TARGET FOR A GIVEN PROCESS
            REPLACE VIEW {self.process_input_output} AS
            CURRENT VALIDTIME SELECT DISTINCT
                PROCESS.ID_PROCESS
            ,   PROCESS.PROCESS_TYPE 
            ,   PROCESS.ID_MAPPER BIGINT
            ,   PROCESS.MODEL_CODE_VIEW 

            ,   PROCESS.PREPARED_DATASET 
            ,   PROCESS.ON_CLAUSE 
            ,   PROCESS.RESULTS 

            ,   PROCESS.STO_DATABASE

            ,   MAPPER.DATASET
            ,   MAPPER.DATASET_OBJECT
            ,   MAPPER.COL_ID_ROW
            ,   MAPPER.COL_ID_PARTITION
            ,   MAPPER.COL_FOLD         
            FROM {self.feature_store.process_catalog} PROCESS
            LEFT JOIN {self.mapper_training_description} MAPPER
            ON PROCESS.ID_MAPPER = MAPPER.ID;    
        """

        return sql_create_view

    def run_training_process(self, id_process, debug=False):

        process_param = self.feature_store.get_process_parameters(id_process)

        on_clause = process_param['on_clause']
        train_fold = process_param['fold']



        sql_queries = {}

        if len(train_fold)>0:
            selected_fold = "'" + "','".join(process_param['fold'].split(',')) + "'"
            filter_ = f"WHERE STO_FOLD_ID IN ({selected_fold})"
        else:
            filter_ = ''

        sql_queries['create_training_view'] = f"""
            REPLACE VIEW {on_clause}_TRAINING AS
            SEL *
            FROM {on_clause}
            {filter_}
        """

        temporary_table = f'{self.database}.TEMPORARY_MODEL_TRAINING_RESULTS'
        error_table = f'{self.database}.TEMPORARY_MODEL_TRAINING_ERROR'

        results = process_param['results']
        error_results = process_param['error_results']

        sql_queries['session'] = f'SET SESSION SEARCHUIFDBPATH = "{self.SEARCHUIFDBPATH}";'

        sql_queries['create_temporary_table'] = f"""
                    -- CREATE VOLATILE TABLE
                    CREATE TABLE {temporary_table}
                    (
                        ID_PROCESS BIGINT
                    ,   ID_PARTITION VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   ID_MODEL BIGINT
                    ,   ID_TRAINED_MODEL VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   MODEL_TYPE VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   STATUS VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   TRAINED_MODEL CLOB
                    )
                    PRIMARY INDEX (ID_PARTITION);
                    """

        sql_queries['insert_results'] = f"""
                    -- INSERT THE RESULTS
                    INSERT INTO {temporary_table}
                    SELECT 
                        {id_process} as ID_PROCESS
                    ,   ID_PARTITION
                    ,   ID_MODEL
                    ,   ID_TRAINED_MODEL
                    ,   MODEL_TYPE
                    ,   STATUS
                    ,   TRAINED_MODEL
                    FROM Script(
                        ON {on_clause}_TRAINING
                        PARTITION BY
                            STO_PARTITION_ID
                        ,	STO_MODEL_ID
                        ORDER BY STO_FAKE_ROW
                        SCRIPT_COMMAND(
                            'tdpython3 ./{self.SEARCHUIFDBPATH}/training.py;'
                        )
                        RETURNS(
                                    'ID_PARTITION VARCHAR(2000)'
                                ,	'ID_MODEL BIGINT'
                                ,	'ID_TRAINED_MODEL VARCHAR(2000)'
                                ,	'MODEL_TYPE VARCHAR(2000)'
                                ,	'STATUS VARCHAR(20000)'
                                ,	'TRAINED_MODEL CLOB'
                        )
                        CHARSET('LATIN')
                    ) AS d;
                    """

        sql_queries['insert_new_trained_models'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {results}
                    (ID_PROCESS, ID_PARTITION, ID_MODEL, ID_TRAINED_MODEL, MODEL_TYPE, STATUS, TRAINED_MODEL)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.ID_TRAINED_MODEL
                        , RESULTS.MODEL_TYPE
                        , RESULTS.STATUS
                        , RESULTS.TRAINED_MODEL
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {results} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.MODEL_TYPE = STORED_RESULTS.MODEL_TYPE
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.ID_TRAINED_MODEL <> 'STO error';
                    """



        sql_queries['insert_new_error_trained_models'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {error_results}
                    (ID_PROCESS, ID_PARTITION, ID_MODEL, ID_TRAINED_MODEL, MODEL_TYPE, STATUS, TRAINED_MODEL)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.ID_TRAINED_MODEL
                        , RESULTS.MODEL_TYPE
                        , RESULTS.STATUS
                        , RESULTS.TRAINED_MODEL
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {error_results} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.MODEL_TYPE = STORED_RESULTS.MODEL_TYPE
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.ID_TRAINED_MODEL = 'STO error';
                    """

        sql_queries['update_existing_trained_models'] = f"""
                    -- UPDATE EXISTING MODELS
                    CURRENT VALIDTIME UPDATE {results} 
                    FROM
                    (
                    CURRENT VALIDTIME SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.ID_TRAINED_MODEL
                        , RESULTS.MODEL_TYPE
                        , RESULTS.STATUS
                        , RESULTS.TRAINED_MODEL
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {results} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.MODEL_TYPE = STORED_RESULTS.MODEL_TYPE
                    WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                    AND RESULTS.ID_TRAINED_MODEL <> 'STO error'
                    ) UPDATED_MODELS
                    SET 
                        ID_TRAINED_MODEL   = UPDATED_MODELS.ID_TRAINED_MODEL,
                        STATUS             = UPDATED_MODELS.STATUS,
                        TRAINED_MODEL      = UPDATED_MODELS.TRAINED_MODEL                    
                    WHERE
                        {results}.ID_PROCESS = UPDATED_MODELS.ID_PROCESS
                    AND
                        {results}.ID_PARTITION = UPDATED_MODELS.ID_PARTITION
                    AND
                        {results}.ID_MODEL = UPDATED_MODELS.ID_MODEL
                    AND
                        {results}.MODEL_TYPE = UPDATED_MODELS.MODEL_TYPE
                    ;
                    """

        sql_queries['update_existing_error_trained_models'] = f"""
                            -- UPDATE EXISTING MODELS
                            CURRENT VALIDTIME UPDATE {error_results} 
                            FROM
                            (
                            CURRENT VALIDTIME SELECT
                                  RESULTS.ID_PROCESS
                                , RESULTS.ID_PARTITION
                                , RESULTS.ID_MODEL
                                , RESULTS.ID_TRAINED_MODEL
                                , RESULTS.MODEL_TYPE
                                , RESULTS.STATUS
                                , RESULTS.TRAINED_MODEL
                            FROM {temporary_table} RESULTS
                            LEFT JOIN {error_results} STORED_RESULTS
                            ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                            AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.MODEL_TYPE = STORED_RESULTS.MODEL_TYPE
                            WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                            AND RESULTS.ID_TRAINED_MODEL <> 'STO error'
                            ) UPDATED_MODELS
                            SET 
                                ID_TRAINED_MODEL   = UPDATED_MODELS.ID_TRAINED_MODEL,
                                STATUS             = UPDATED_MODELS.STATUS,
                                TRAINED_MODEL      = UPDATED_MODELS.TRAINED_MODEL                    
                            WHERE
                                {error_results}.ID_PROCESS = UPDATED_MODELS.ID_PROCESS
                            AND
                                {error_results}.ID_PARTITION = UPDATED_MODELS.ID_PARTITION
                            AND
                                {error_results}.ID_MODEL = UPDATED_MODELS.ID_MODEL
                            AND
                                {error_results}.MODEL_TYPE = UPDATED_MODELS.MODEL_TYPE
                            ;
                            """

        sql_queries['drop_temporary_table'] = f'DROP TABLE {temporary_table};'

        con = tdml.get_connection()

        if True:
            try:
                con.execute(sql_queries['drop_temporary_table'])
                con.execute(sql_queries['create_temporary_table'])
            except Exception as e:
                con.execute(sql_queries['create_temporary_table'])
            con.execute(sql_queries['create_training_view'])
            con.execute(sql_queries['session'])
            con.execute(sql_queries['insert_results'])
        if True:
            con.execute(sql_queries['update_existing_trained_models'])
            con.execute(sql_queries['insert_new_trained_models'])
            con.execute(sql_queries['insert_new_error_trained_models'])
            con.execute(sql_queries['update_existing_error_trained_models'])
            nb_errors = tdml.get_context().execute(
                f"SEL count(*) FROM {temporary_table} WHERE ID_TRAINED_MODEL = 'STO error'").fetchall()[0][0]
            if nb_errors > 0:
                print(f'{nb_errors} errors detected.')
                print(f'please check the {error_results} table or the corresponding view for more informations.')
            con.execute(sql_queries['drop_temporary_table'])

        if debug:
            return sql_queries

        return

    def list_trained_models(self,with_models = False, with_arguments = False):

        df = tdml.DataFrame(tdml.in_schema(self.trained_model_repository.split('.')[0],
                                           self.trained_model_repository.split('.')[1]))

        columns = df.columns
        columns = [x for x in columns if x != 'ValidPeriod']
        if with_models == False:
            columns = [x for x in columns if x != 'TRAINED_MODEL']
        if with_arguments == False:
            columns = [x for x in columns if x != 'STATUS']

        return df.select(columns)

    def list_current_trained_models(self,with_models = False, with_arguments = False):

        df = tdml.DataFrame(tdml.in_schema(self.trained_model_repository.split('.')[0],
                                           self.trained_model_repository.split('.')[1]))

        columns = df.columns
        columns = [x for x in columns if x != 'ValidPeriod']
        if with_models == False:
            columns = [x for x in columns if x != 'TRAINED_MODEL']
        if with_arguments == False:
            columns = [x for x in columns if x != 'STATUS']

        return tdml.DataFrame.from_query(f"""
                        CURRENT VALIDTIME
                        SELECT
                            {','.join(columns)}
                        FROM {self.trained_model_repository}
                    """)

    def create_scoring_process_from_training_process(self, id_process, id_training_process, scoring_fold, **kwargs):

        # get the process parameters
        training_process_param = self.feature_store.get_process_parameters(id_training_process)

        # get the dataset name
        dataset_name = self.mapper_training_get_dataset(training_process_param['id_mapper'])[0]

        # create the scoring process parameters
        if type(scoring_fold) == type([]):
            scoring_fold = ','.join(scoring_fold)
        results = f'{self.database}.STO_SCORES_{dataset_name.split(".")[1]}_{id_process}'
        on_clause = f'{self.database}.V_STO_ON_CLAUSE_SCORING_{dataset_name.split(".")[1]}_{training_process_param["id_mapper"]}'
        scoring_process_param = training_process_param.copy()
        scoring_process_param['process_type'] = 'sto_scoring'
        scoring_process_param['id_process'] = id_process
        scoring_process_param['fold'] = scoring_fold
        scoring_process_param['on_clause'] = on_clause
        scoring_process_param['results'] = results

        # create the result tables
        if tdml.db_list_tables(schema_name=results.split('.')[0], object_name=results.split('.')[1] + '%').shape[
            0] == 0:
            # tdml.get_context().execute(create_scoring_results(results,'FLOAT'))
            # tdml.get_context().execute(create_scoring_results(results,'BIGINT'))
            # tdml.get_context().execute(create_scoring_results(results,'VARCHAR(255)'))
            tdml.get_context().execute(create_scoring_results(results))

        # create on_clause_view for the scoring process
        on_clause_view = training_process_param['on_clause']

        sql_query = f"""
        REPLACE VIEW {scoring_process_param['on_clause']} AS
        SELECT 
            CODE_MODEL.*
        ,   CASE WHEN CODE_MODEL.STO_FAKE_ROW = 1 THEN TRAINED_MODEL.ID_TRAINED_MODEL END AS ID_TRAINED_MODEL
        ,   CASE WHEN CODE_MODEL.STO_FAKE_ROW = 1 THEN TRAINED_MODEL.MODEL_TYPE END AS MODEL_TYPE
        ,   CASE WHEN CODE_MODEL.STO_FAKE_ROW = 1 THEN TRAINED_MODEL.TRAINED_MODEL END AS TRAINED_MODEL
        FROM {on_clause_view} CODE_MODEL
        , (CURRENT VALIDTIME
            SEL * FROM {self.trained_model_repository}
            WHERE MODEL_TYPE = 'pickle'
            AND ID_PROCESS = {training_process_param['id_process']}) TRAINED_MODEL
        WHERE 
            CODE_MODEL.STO_PARTITION_ID = TRAINED_MODEL.ID_PARTITION
        AND CODE_MODEL.STO_MODEL_ID = TRAINED_MODEL.ID_MODEL
        """

        tdml.get_context().execute(sql_query)

        # insert the scoring process in the process catalog
        insert_new_process(**scoring_process_param)

        return

    def run_scoring_process(self, id_process):

        process_param = self.feature_store.get_process_parameters(id_process)

        on_clause = process_param['on_clause']
        scoring_fold = process_param['fold']

        temporary_table = process_param['results']

        sql_queries = {}

        if len(scoring_fold) > 0:
            selected_fold = "'" + "','".join(process_param['fold'].split(',')) + "'"
            filter_ = f"WHERE STO_FOLD_ID IN ({selected_fold})"
        else:
            filter_ = ''

        sql_queries['create_scoring_view'] = f"""
            REPLACE VIEW {on_clause}_FILTERED AS
            SEL *
            FROM {on_clause}
            {filter_}
        """

        sql_queries['session'] = f'SET SESSION SEARCHUIFDBPATH = "{self.SEARCHUIFDBPATH}";'

        sto_query = f"""
                    SELECT
                        ID_PARTITION
                    ,   ID_ROW
                    ,   FEATURE_NAME
                    ,   FEATURE_VALUE
                    ,   FEATURE_TYPE
                    ,   STATUS
                    ,   {id_process} AS ID_PROCESS
                    ,   ID_MODEL
                    ,   MODEL_TYPE
                    ,   ID_TRAINED_MODEL
                    FROM Script(
                        ON {on_clause}_FILTERED
                        PARTITION BY
                            STO_PARTITION_ID
                        ,	STO_MODEL_ID
                        ,   STO_FOLD_ID
                        ORDER BY STO_FAKE_ROW
                        SCRIPT_COMMAND(
                            'tdpython3 ./{self.SEARCHUIFDBPATH}/scoring.py;'
                        )
                        RETURNS(
                                    'ID_PARTITION VARCHAR(2000)'
                                ,   'ID_ROW VARCHAR(2000)'
                                ,	'FEATURE_NAME VARCHAR(2000)'
                                ,	'FEATURE_VALUE VARCHAR(2000)'
                                ,	'FEATURE_TYPE VARCHAR(20000)'
                                ,	'STATUS VARCHAR(2000)'
                                ,   'ID_MODEL BIGINT'
                                ,	'MODEL_TYPE VARCHAR(2000)'
                                ,	'ID_TRAINED_MODEL VARCHAR(255)'
                        )
                        CHARSET('LATIN')
                    ) AS d;
        """
        sql_queries['insert_results'] = f"""
                    -- INSERT THE RESULTS
                    INSERT INTO {temporary_table}
                    (ID_PARTITION, ID_ROW, FEATURE_NAME,FEATURE_VALUE, FEATURE_TYPE,STATUS, ID_PROCESS,
                    ID_MODEL ,  MODEL_TYPE ,  ID_TRAINED_MODEL)
                    {sto_query}
                    """

        sql_queries['create_view_sto'] = f"""
                    -- VIEW FOR SCORING RESULTS
                    REPLACE VIEW {on_clause.replace('ON_CLAUSE','STO_QUERY')} AS
                    {sto_query}
                    """

        tdml.get_context().execute(sql_queries['create_scoring_view'])
        tdml.get_context().execute(sql_queries['session'])
        tdml.get_context().execute(sql_queries['create_view_sto'])
        tdml.get_context().execute(sql_queries['insert_results'])
        print(f'results inserted in {temporary_table}')
        return



    def GetCodeNDataset(self, id_process, id_model=None, id_partition=None, id_fold=None, **kwargs):

        # Get the process
        process = self.feature_store.list_process().set_index(['ID_PROCESS']).filter(items=[id_process],
                                                                                    axis=0).to_pandas(num_rows=1)

        # Get the id_mapper of the process
        id_mapper = process.ID_MAPPER.values[0]

        # Get the folds list
        if id_fold is None:
            fold = process.FOLD.values[0]

        # Get the name of the prepared dataset table or view
        prepared_dataset = process.PREPARED_DATASET.values[0]

        # Get the mapper, id_model and id_partition when needed
        if id_model is None and id_partition is None:
            mapper = self.get_current_mapper_training().set_index(['ID']).filter(items=[id_mapper],
                                                                                        axis=0).head(1).to_pandas(num_rows=1)
            id_model = mapper.ID_MODEL.values[0]
            id_partition = mapper.ID_PARTITION.values[0]
        elif id_model is None:
            mapper = self.get_current_mapper_training().set_index(['ID', 'ID_PARTITION']).filter(
                items=[(id_mapper, id_partition)], axis=0).head(1).to_pandas(num_rows=1)
            id_model = mapper.ID_MODEL.values[0]
            id_partition = mapper.ID_PARTITION.values[0]
        elif id_partition is None:
            mapper = self.get_current_mapper_training().set_index(['ID', 'ID_MODEL']).filter(
                items=[(id_mapper, id_model)], axis=0).head(1).to_pandas(num_rows=1)
            id_model = mapper.ID_MODEL.values[0]
            id_partition = mapper.ID_PARTITION.values[0]
        else:
            mapper = self.get_current_mapper_training().set_index(['ID', 'ID_PARTITION', 'ID_MODEL']).filter(
                items=[(id_mapper, id_partition, id_model)], axis=0).head(1).to_pandas(num_rows=1)
            id_model = mapper.ID_MODEL.values[0]
            id_partition = mapper.ID_PARTITION.values[0]

            # get the code and arguments
        code = \
        self.get_current_models().set_index(['ID_MODEL']).filter(items=[id_model], axis=0).to_pandas().CODE.values[
            0].decode()
        arguments = json.loads(self.get_current_models().set_index(['ID_MODEL']).filter(items=[id_model],
                                                                                       axis=0).to_pandas().ARGUMENTS.values[
                                   0])

        # get the dataset corresponding to the partition
        df = tdml.DataFrame(tdml.in_schema(prepared_dataset.split('.')[0], prepared_dataset.split('.')[1]))
        dataset = df[df.STO_PARTITION_ID == id_partition][df.STO_FOLD_ID.isin(fold.split(','))].to_pandas(**kwargs)
        dataset = reformat(dataset, arguments)  # reformat like in-database scripts

        # get the id of the trained model
        df_ = self.list_current_trained_models(with_models=True)
        res = df_.loc[
        (df_['ID_PARTITION'] == id_partition) & (df_['ID_PROCESS'] == id_process) & (df_['ID_MODEL'] == id_model), :].to_pandas()
        id_trained_model_pickle = res.set_index('MODEL_TYPE').filter(items=['pickle'], axis=0).ID_TRAINED_MODEL.values
        id_trained_model_onnx = res.set_index('MODEL_TYPE').filter(items=['onnx'], axis=0).ID_TRAINED_MODEL.values
        if len(res)>0:
            id_trained_model_pickle = id_trained_model_pickle[0]
            id_trained_model_onnx = id_trained_model_onnx[0]

        extract_infos = {'id_process': id_process,
                         'id_mapper': id_mapper,
                         'prepared_dataset': prepared_dataset,
                         'fold': fold,
                         'id_model': id_model,
                         'id_partition': id_partition,
                         'features': arguments['model_parameters']['column_names_X'],
                         'target': arguments['model_parameters']['target'],
                         'id_trained_model_pickle': id_trained_model_pickle,
                         'id_trained_model_onnx': id_trained_model_onnx
                         }

        return code, arguments, dataset, extract_infos


    def downloadonnxmodel(self, id_trained_model_onnx, filename=None):
        df = self.list_current_trained_models(with_models=True)
        df = df.loc[
            (df['ID_TRAINED_MODEL'] == id_trained_model_onnx) & (df['MODEL_TYPE'] == 'onnx'), ['TRAINED_MODEL']].to_pandas()

        if df.shape[0] == 0:
            print(f'there is not ONNX model with id : {id_trained_model_onnx}')
            return

        onx_model = df.TRAINED_MODEL.values[0]
        onx_model_reconstructed = base64.b64decode(onx_model)

        if filename is None:
            filename = id_trained_model_onnx + '.onnx'

        try:
            with open(filename, 'wb') as f:
                f.write(onx_model_reconstructed)
            print(f'{filename} downloaded')
        except Exception as e:
            print(f'error when writing the onnx file : {e}')

        return

    def BYOMQuery(self,id_trained_model_onnx, prepared_dataset, features, id_partition, fold, **kwargs):
        query = f"""
        select * from mldb.ONNXPredict(
            on (
                select 
                  STO_ROW_ID
                , {','.join(features)}
                , STO_PARTITION_ID
                , STO_FOLD_ID
                from {prepared_dataset}
                where STO_PARTITION_ID = '{id_partition}'
                AND STO_FOLD_ID in ({','.join("'" + x + "'" for x in fold)}))
            on (
                CURRENT VALIDTIME
                select 
                  ID_TRAINED_MODEL as model_id
                --, TO_BYTES(TRANSLATE(trained_model USING LATIN_TO_UNICODE),'base64m') as model
                , TO_BYTES(trained_model,TRANSLATE('base64m' USING UNICODE_TO_LATIN)) as model
            from {self.trained_model_repository}
            where model_id='{id_trained_model_onnx}' AND model_type = 'onnx'
            ) DIMENSION
            using
                Accumulate('STO_ROW_ID', 'STO_PARTITION_ID', 'STO_FOLD_ID')
                ModelInputFieldsMap('float_input=[1:{len(features)}]')
                --ShowModelInputFieldsMap('true')
        ) as td
        """

        return query


    def run_feature_engineering_aggregate_process(self, id_process, debug=False):

        process_param = self.feature_store.get_process_parameters(id_process)

        if process_param['process_type'] != 'sto_feature_engineering_agg':
            print('this process if not a feature engineering aggregate one.')
            print('Please check your process type of your process:')
            print(process_param)
            return

        on_clause = process_param['on_clause']
        train_fold = process_param['fold']



        sql_queries = {}

        temporary_table = f'{self.database}.TEMPORARY_MODEL_FEATENGAGG_RESULTS'
        error_table = f'{self.database}.TEMPORARY_MODEL_FEATENGAGG_ERROR'

        results = process_param['results']
        error_results = process_param['error_results']

        sql_queries['session'] = f'SET SESSION SEARCHUIFDBPATH = "{self.SEARCHUIFDBPATH}";'

        sql_queries['create_temporary_table'] = f"""
                    -- CREATE VOLATILE TABLE
                    CREATE TABLE {temporary_table}
                    (
                        ID_PROCESS BIGINT
                    ,   ID_PARTITION VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   ID_MODEL BIGINT
                    ,   FEATURE_NAME VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   FEATURE_VALUE VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   FEATURE_TYPE VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   STATUS VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    )
                    PRIMARY INDEX (ID_PARTITION);
                    """

        sto_query = f"""
                    SELECT 
                        {id_process} as ID_PROCESS
                    ,   ID_PARTITION
                    ,   ID_MODEL
                    ,   FEATURE_NAME
                    ,   FEATURE_VALUE
                    ,   FEATURE_TYPE
                    ,   STATUS
                    FROM Script(
                        ON {on_clause}
                        PARTITION BY
                            STO_PARTITION_ID
                        ,	STO_MODEL_ID
                        ORDER BY STO_FAKE_ROW
                        SCRIPT_COMMAND(
                            'tdpython3 ./{self.SEARCHUIFDBPATH}/feature_engineering_reducer.py;'
                        )
                        RETURNS(
                                    'ID_PARTITION VARCHAR(2000)'
                                ,	'ID_MODEL BIGINT'
                                ,	'FEATURE_NAME VARCHAR(2000)'
                                ,	'FEATURE_VALUE VARCHAR(2000)'
                                ,	'FEATURE_TYPE VARCHAR(2000)'
                                ,	'STATUS VARCHAR(20000)'
                        )
                        CHARSET('LATIN')
                    ) AS d
                    """

        sql_queries['insert_results'] = f"""
                    -- INSERT THE RESULTS
                    INSERT INTO {temporary_table}
                    {sto_query}
                    """

        sql_queries['create_view_sto_query'] = f"""
                    REPLACE VIEW {on_clause.replace('ON_CLAUSE','STO_QUERY')} AS
                    {sto_query}
                    """


        result_float = [x for x in results.split(',') if x.split('_')[-1] == 'FLOAT'][0]
        sql_queries['insert_results_float'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {result_float}
                    (ID_PROCESS, ID_PARTITION, ID_MODEL, FEATURE_NAME, FEATURE_VALUE)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.FEATURE_NAME
                        , CAST(RESULTS.FEATURE_VALUE AS FLOAT) AS FEATURE_VALUE
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {result_float} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) like '%float%';
                    """


        sql_queries['update_results_float'] = f"""
                        -- UPDATE EXISTING MODELS
                    CURRENT VALIDTIME UPDATE {result_float} 
                    FROM
                    (   CURRENT VALIDTIME
                        SELECT
                              RESULTS.ID_PROCESS
                            , RESULTS.ID_PARTITION
                            , RESULTS.ID_MODEL
                            , RESULTS.FEATURE_NAME
                            , CAST(RESULTS.FEATURE_VALUE AS FLOAT) AS FEATURE_VALUE
                        FROM {temporary_table} RESULTS
                    LEFT JOIN {result_float} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) like '%float%'
                    ) UPDATED_FEATURES
                    SET 
                        FEATURE_VALUE  = UPDATED_FEATURES.FEATURE_VALUE                 
                    WHERE
                        {result_float}.ID_PROCESS = UPDATED_FEATURES.ID_PROCESS
                    AND
                        {result_float}.ID_PARTITION = UPDATED_FEATURES.ID_PARTITION
                    AND
                        {result_float}.ID_MODEL = UPDATED_FEATURES.ID_MODEL
                    AND
                        {result_float}.FEATURE_NAME = UPDATED_FEATURES.FEATURE_NAME
                    """

        result_integer = [x for x in results.split(',') if x.split('_')[-1] == 'INTEGER'][0]
        sql_queries['insert_results_integer'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {result_integer}
                    (ID_PROCESS, ID_PARTITION, ID_MODEL, FEATURE_NAME, FEATURE_VALUE)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.FEATURE_NAME
                        , CAST(RESULTS.FEATURE_VALUE AS BIGINT) AS FEATURE_VALUE
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {result_integer} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) like '%int%';
                    """


        sql_queries['update_results_integer'] = f"""
                        -- UPDATE EXISTING MODELS
                    CURRENT VALIDTIME UPDATE {result_integer} 
                    FROM
                    (   CURRENT VALIDTIME
                        SELECT
                              RESULTS.ID_PROCESS
                            , RESULTS.ID_PARTITION
                            , RESULTS.ID_MODEL
                            , RESULTS.FEATURE_NAME
                            , CAST(RESULTS.FEATURE_VALUE AS BIGINT) AS FEATURE_VALUE
                        FROM {temporary_table} RESULTS
                    LEFT JOIN {result_integer} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) like '%int%'
                    ) UPDATED_FEATURES
                    SET 
                        FEATURE_VALUE      = UPDATED_FEATURES.FEATURE_VALUE                 
                    WHERE
                        {result_integer}.ID_PROCESS = UPDATED_FEATURES.ID_PROCESS
                    AND
                        {result_integer}.ID_PARTITION = UPDATED_FEATURES.ID_PARTITION
                    AND
                        {result_integer}.ID_MODEL = UPDATED_FEATURES.ID_MODEL
                    AND
                        {result_integer}.FEATURE_NAME = UPDATED_FEATURES.FEATURE_NAME
                    """

        result_varchar = [x for x in results.split(',') if x.split('_')[-1] == 'VARCHAR'][0]
        sql_queries['insert_results_varchar'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {result_varchar}
                    (ID_PROCESS, ID_PARTITION, ID_MODEL, FEATURE_NAME, FEATURE_VALUE)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.FEATURE_NAME
                        , RESULTS.FEATURE_VALUE
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {result_varchar} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) not like '%float%'
                    AND lower(RESULTS.FEATURE_TYPE) not like '%int%';
                    """


        sql_queries['update_results_varchar'] = f"""
                        -- UPDATE EXISTING MODELS
                    CURRENT VALIDTIME UPDATE {result_varchar} 
                    FROM
                    (   CURRENT VALIDTIME
                        SELECT
                              RESULTS.ID_PROCESS
                            , RESULTS.ID_PARTITION
                            , RESULTS.ID_MODEL
                            , RESULTS.FEATURE_NAME
                            , RESULTS.FEATURE_VALUE
                        FROM {temporary_table} RESULTS
                    LEFT JOIN {result_varchar} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) not like '%float%'
                    AND lower(RESULTS.FEATURE_TYPE) not like '%int%'
                    ) UPDATED_FEATURES
                    SET 
                        FEATURE_VALUE  = UPDATED_FEATURES.FEATURE_VALUE                 
                    WHERE
                        {result_varchar}.ID_PROCESS = UPDATED_FEATURES.ID_PROCESS
                    AND
                        {result_varchar}.ID_PARTITION = UPDATED_FEATURES.ID_PARTITION
                    AND
                        {result_varchar}.ID_MODEL = UPDATED_FEATURES.ID_MODEL
                    AND
                        {result_varchar}.FEATURE_NAME = UPDATED_FEATURES.FEATURE_NAME
                    """

        sql_queries['insert_new_error_feature_engineering'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {error_results}
                    (ID_PROCESS, ID_PARTITION, ID_MODEL,  STATUS)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.STATUS
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {error_results} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE = 'STO error';
                    """

        sql_queries['drop_temporary_table'] = f'DROP TABLE {temporary_table};'

        con = tdml.get_connection()

        if True:
            try:
                con.execute(sql_queries['drop_temporary_table'])
                con.execute(sql_queries['create_temporary_table'])
            except Exception as e:
                con.execute(sql_queries['create_temporary_table'])
            con.execute(sql_queries['session'])
            con.execute(sql_queries['create_view_sto_query'])
            con.execute(sql_queries['insert_results'])
            con.execute(sql_queries['insert_results_float'])
            con.execute(sql_queries['update_results_float'])
            con.execute(sql_queries['insert_results_integer'])
            con.execute(sql_queries['update_results_integer'])
            con.execute(sql_queries['insert_results_varchar'])
            con.execute(sql_queries['update_results_varchar'])
            con.execute(sql_queries['insert_new_error_feature_engineering'])
            nb_errors = tdml.get_context().execute(
                f"SEL count(*) FROM {temporary_table} WHERE FEATURE_VALUE = 'STO error'").fetchall()[0][0]
            if nb_errors > 0:
                print(f'{nb_errors} errors detected.')
                print(f'please check the {error_results} table or the corresponding view for more informations.')
            else:
                print(f'no error detected. Computations successful.')
                print(f'results are insterted or updated in the following tables:')
                print(f'- {result_float}')
                print(f'- {result_integer}')
                print(f'- {result_varchar}')
            con.execute(sql_queries['drop_temporary_table'])

        if debug:
            return sql_queries

        return

    def run_feature_engineering_rowlevel_process(self, id_process, debug=False):

        process_param = self.feature_store.get_process_parameters(id_process)

        if process_param['process_type'] != 'sto_feature_engineering_row_level':
            print('this process if not a feature engineering row level one.')
            print('Please check your process type of your process:')
            print(process_param)
            return

        on_clause = process_param['on_clause']
        train_fold = process_param['fold']



        sql_queries = {}

        temporary_table = f'{self.database}.TEMPORARY_MODEL_FEATENGROW_RESULTS'
        error_table = f'{self.database}.TEMPORARY_MODEL_FEATENGROW_ERROR'

        results = process_param['results']
        error_results = process_param['error_results']

        sql_queries['session'] = f'SET SESSION SEARCHUIFDBPATH = "{self.SEARCHUIFDBPATH}";'

        sql_queries['create_temporary_table'] = f"""
                    -- CREATE VOLATILE TABLE
                    CREATE TABLE {temporary_table}
                    (
                        ID_PROCESS BIGINT
                    ,   ID_PARTITION VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   ID_ROW VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   ID_MODEL BIGINT
                    ,   FEATURE_NAME VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   FEATURE_VALUE VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   FEATURE_TYPE VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   STATUS VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    )
                    NO PRIMARY INDEX;
                    """

        sto_query = f"""
                    SELECT 
                        {id_process} as ID_PROCESS
                    ,   ID_PARTITION
                    ,   ID_ROW
                    ,   ID_MODEL
                    ,   FEATURE_NAME
                    ,   FEATURE_VALUE
                    ,   FEATURE_TYPE
                    ,   STATUS
                    FROM Script(
                        ON {on_clause}
                        PARTITION BY
                            STO_PARTITION_ID
                        ,	STO_MODEL_ID
                        ORDER BY STO_FAKE_ROW
                        SCRIPT_COMMAND(
                            'tdpython3 ./{self.SEARCHUIFDBPATH}/feature_engineering.py;'
                        )
                        RETURNS(
                                    'ID_PARTITION VARCHAR(2000)'
                                ,   'ID_ROW VARCHAR(2000)'
                                ,	'ID_MODEL BIGINT'
                                ,	'FEATURE_NAME VARCHAR(2000)'
                                ,	'FEATURE_VALUE VARCHAR(2000)'
                                ,	'FEATURE_TYPE VARCHAR(2000)'
                                ,	'STATUS VARCHAR(20000)'
                        )
                        CHARSET('LATIN')
                    ) AS d
                    """

        sql_queries['insert_results'] = f"""
                    -- INSERT THE RESULTS
                    INSERT INTO {temporary_table}
                    {sto_query}
                    """

        sql_queries['create_view_sto_query'] = f"""
                    REPLACE VIEW {on_clause.replace('ON_CLAUSE','STO_QUERY')} AS
                    {sto_query}
                    """


        result_float = [x for x in results.split(',') if x.split('_')[-1] == 'FLOAT'][0]
        sql_queries['insert_results_float'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {result_float}
                    (ID_PROCESS, ID_PARTITION, ID_ROW, ID_MODEL, FEATURE_NAME, FEATURE_VALUE)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_ROW
                        , RESULTS.ID_MODEL
                        , RESULTS.FEATURE_NAME
                        , CAST(RESULTS.FEATURE_VALUE AS FLOAT) AS FEATURE_VALUE
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {result_float} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    AND RESULTS.ID_ROW = STORED_RESULTS.ID_ROW
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) like '%float%';
                    """


        sql_queries['update_results_float'] = f"""
                        -- UPDATE EXISTING MODELS
                    CURRENT VALIDTIME UPDATE {result_float} 
                    FROM
                    (   CURRENT VALIDTIME
                        SELECT
                              RESULTS.ID_PROCESS
                            , RESULTS.ID_PARTITION
                            , RESULTS.ID_ROW
                            , RESULTS.ID_MODEL
                            , RESULTS.FEATURE_NAME
                            , CAST(RESULTS.FEATURE_VALUE AS FLOAT) AS FEATURE_VALUE
                        FROM {temporary_table} RESULTS
                    LEFT JOIN {result_float} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    AND RESULTS.ID_ROW = STORED_RESULTS.ID_ROW
                    WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) like '%float%'
                    ) UPDATED_FEATURES
                    SET 
                        FEATURE_VALUE  = UPDATED_FEATURES.FEATURE_VALUE                 
                    WHERE
                        {result_float}.ID_PROCESS = UPDATED_FEATURES.ID_PROCESS
                    AND
                        {result_float}.ID_PARTITION = UPDATED_FEATURES.ID_PARTITION
                    AND
                        {result_float}.ID_ROW = UPDATED_FEATURES.ID_ROW
                    AND
                        {result_float}.ID_MODEL = UPDATED_FEATURES.ID_MODEL
                    AND
                        {result_float}.FEATURE_NAME = UPDATED_FEATURES.FEATURE_NAME
                    """

        result_integer = [x for x in results.split(',') if x.split('_')[-1] == 'INTEGER'][0]
        sql_queries['insert_results_integer'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {result_integer}
                    (ID_PROCESS, ID_PARTITION, ID_ROW, ID_MODEL, FEATURE_NAME, FEATURE_VALUE)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_ROW
                        , RESULTS.ID_MODEL
                        , RESULTS.FEATURE_NAME
                        , CAST(RESULTS.FEATURE_VALUE AS BIGINT) AS FEATURE_VALUE
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {result_integer} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    AND RESULTS.ID_ROW = STORED_RESULTS.ID_ROW
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) like '%int%';
                    """


        sql_queries['update_results_integer'] = f"""
                        -- UPDATE EXISTING MODELS
                    CURRENT VALIDTIME UPDATE {result_integer} 
                    FROM
                    (   CURRENT VALIDTIME
                        SELECT
                              RESULTS.ID_PROCESS
                            , RESULTS.ID_PARTITION
                            , RESULTS.ID_ROW
                            , RESULTS.ID_MODEL
                            , RESULTS.FEATURE_NAME
                            , CAST(RESULTS.FEATURE_VALUE AS BIGINT) AS FEATURE_VALUE
                        FROM {temporary_table} RESULTS
                    LEFT JOIN {result_integer} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    AND RESULTS.ID_ROW = STORED_RESULTS.ID_ROW
                    WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) like '%int%'
                    ) UPDATED_FEATURES
                    SET 
                        FEATURE_VALUE      = UPDATED_FEATURES.FEATURE_VALUE                 
                    WHERE
                        {result_integer}.ID_PROCESS = UPDATED_FEATURES.ID_PROCESS
                    AND
                        {result_integer}.ID_PARTITION = UPDATED_FEATURES.ID_PARTITION
                    AND
                        {result_integer}.ID_ROW = UPDATED_FEATURES.ID_ROW
                    AND
                        {result_integer}.ID_MODEL = UPDATED_FEATURES.ID_MODEL
                    AND
                        {result_integer}.FEATURE_NAME = UPDATED_FEATURES.FEATURE_NAME
                    """

        result_varchar = [x for x in results.split(',') if x.split('_')[-1] == 'VARCHAR'][0]
        sql_queries['insert_results_varchar'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {result_varchar}
                    (ID_PROCESS, ID_PARTITION, ID_ROW, ID_MODEL, FEATURE_NAME, FEATURE_VALUE)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_ROW
                        , RESULTS.ID_MODEL
                        , RESULTS.FEATURE_NAME
                        , RESULTS.FEATURE_VALUE
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {result_varchar} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    AND RESULTS.ID_ROW = STORED_RESULTS.ID_ROW
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) not like '%float%'
                    AND lower(RESULTS.FEATURE_TYPE) not like '%int%';
                    """


        sql_queries['update_results_varchar'] = f"""
                        -- UPDATE EXISTING MODELS
                    CURRENT VALIDTIME UPDATE {result_varchar} 
                    FROM
                    (   CURRENT VALIDTIME
                        SELECT
                              RESULTS.ID_PROCESS
                            , RESULTS.ID_PARTITION
                            , RESULTS.ID_ROW
                            , RESULTS.ID_MODEL
                            , RESULTS.FEATURE_NAME
                            , RESULTS.FEATURE_VALUE
                        FROM {temporary_table} RESULTS
                    LEFT JOIN {result_varchar} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL AND RESULTS.FEATURE_NAME = STORED_RESULTS.FEATURE_NAME
                    AND RESULTS.ID_ROW = STORED_RESULTS.ID_ROW
                    WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    AND lower(RESULTS.FEATURE_TYPE) not like '%float%'
                    AND lower(RESULTS.FEATURE_TYPE) not like '%int%'
                    ) UPDATED_FEATURES
                    SET 
                        FEATURE_VALUE  = UPDATED_FEATURES.FEATURE_VALUE                 
                    WHERE
                        {result_varchar}.ID_PROCESS = UPDATED_FEATURES.ID_PROCESS
                    AND
                        {result_varchar}.ID_PARTITION = UPDATED_FEATURES.ID_PARTITION
                    AND
                        {result_varchar}.ID_ROW = UPDATED_FEATURES.ID_ROW
                    AND
                        {result_varchar}.ID_MODEL = UPDATED_FEATURES.ID_MODEL
                    AND
                        {result_varchar}.FEATURE_NAME = UPDATED_FEATURES.FEATURE_NAME
                    """

        sql_queries['insert_new_error_feature_engineering'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {error_results}
                    (ID_PROCESS, ID_PARTITION, ID_MODEL,  STATUS)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.STATUS
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {error_results} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE = 'STO error';
                    """

        sql_queries['drop_temporary_table'] = f'DROP TABLE {temporary_table};'

        con = tdml.get_connection()

        if True:
            try:
                con.execute(sql_queries['drop_temporary_table'])
                con.execute(sql_queries['create_temporary_table'])
            except Exception as e:
                con.execute(sql_queries['create_temporary_table'])
            con.execute(sql_queries['session'])
            con.execute(sql_queries['create_view_sto_query'])
            con.execute(sql_queries['insert_results'])
            con.execute(sql_queries['insert_results_float'])
            con.execute(sql_queries['update_results_float'])
            con.execute(sql_queries['insert_results_integer'])
            con.execute(sql_queries['update_results_integer'])
            con.execute(sql_queries['insert_results_varchar'])
            con.execute(sql_queries['update_results_varchar'])
            con.execute(sql_queries['insert_new_error_feature_engineering'])
            nb_errors = tdml.get_context().execute(
                f"SEL count(*) FROM {temporary_table} WHERE FEATURE_VALUE = 'STO error'").fetchall()[0][0]
            if nb_errors > 0:
                print(f'{nb_errors} errors detected.')
                print(f'please check the {error_results} table or the corresponding view for more informations.')
            else:
                print(f'no error detected. Computations successful.')
                print(f'results are insterted or updated in the following tables:')
                print(f'- {result_float}')
                print(f'- {result_integer}')
                print(f'- {result_varchar}')
            con.execute(sql_queries['drop_temporary_table'])

        if debug:
            return sql_queries

        return

    def run_feature_engineering_rowlevel_process_to_json(self, id_process, debug=False):

        process_param = self.feature_store.get_process_parameters(id_process)

        if process_param['process_type'] != 'sto_feature_engineering_row_level':
            print('this process if not a feature engineering row level one.')
            print('Please check your process type of your process:')
            print(process_param)
            return

        on_clause = process_param['on_clause']
        train_fold = process_param['fold']



        sql_queries = {}

        temporary_table = f'{self.database}.TEMPORARY_MODEL_FEATENGROW_JSON_RESULTS'
        error_table = f'{self.database}.TEMPORARY_MODEL_FEATENGROW_ERROR'

        results = process_param['results']
        error_results = process_param['error_results']

        sql_queries['session'] = f'SET SESSION SEARCHUIFDBPATH = "{self.SEARCHUIFDBPATH}";'

        sql_queries['create_temporary_table'] = f"""
                    -- CREATE VOLATILE TABLE
                    CREATE TABLE {temporary_table}
                    (
                        ID_PROCESS BIGINT
                    ,   ID_PARTITION VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   ID_ROW VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   ID_MODEL BIGINT
                    ,   FEATURE_VALUE VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    ,   STATUS VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL
                    )
                    NO PRIMARY INDEX;
                    """

        sto_query = f"""
                    SELECT 
                        {id_process} as ID_PROCESS
                    ,   ID_PARTITION
                    ,   ID_ROW
                    ,   ID_MODEL
                    ,   FEATURE_VALUE
                    ,   STATUS
                    FROM Script(
                        ON {on_clause}
                        PARTITION BY
                            STO_PARTITION_ID
                        ,	STO_MODEL_ID
                        ORDER BY STO_FAKE_ROW
                        SCRIPT_COMMAND(
                            'tdpython3 ./{self.SEARCHUIFDBPATH}/feature_engineering_jsonoutput.py;'
                        )
                        RETURNS(
                                    'ID_PARTITION VARCHAR(2000)'
                                ,   'ID_ROW VARCHAR(2000)'
                                ,	'ID_MODEL BIGINT'
                                ,	'FEATURE_VALUE VARCHAR(2000)'
                                ,	'STATUS VARCHAR(20000)'
                        )
                        CHARSET('LATIN')
                    ) AS d
                    """

        sql_queries['insert_results_temporary'] = f"""
                    -- INSERT THE RESULTS
                    INSERT INTO {temporary_table}
                    {sto_query}
                    """

        sql_queries['create_view_sto_query'] = f"""
                    REPLACE VIEW {on_clause.replace('ON_CLAUSE','STO_QUERYJSON')} AS
                    {sto_query}
                    """

        result = [x for x in results.split(',') if x.split('_')[-1] == 'JSON'][0]
        sql_queries['insert_results'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {result}
                    (ID_PROCESS, ID_PARTITION, ID_ROW, ID_MODEL, FEATURE_VALUE)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_ROW
                        , RESULTS.ID_MODEL
                        , RESULTS.FEATURE_VALUE
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {result} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL 
                    AND RESULTS.ID_ROW = STORED_RESULTS.ID_ROW
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error';
                    """


        sql_queries['update_results'] = f"""
                        -- UPDATE EXISTING MODELS
                    CURRENT VALIDTIME UPDATE {result} 
                    FROM
                    (   CURRENT VALIDTIME
                        SELECT
                              RESULTS.ID_PROCESS
                            , RESULTS.ID_PARTITION
                            , RESULTS.ID_ROW
                            , RESULTS.ID_MODEL
                            , RESULTS.FEATURE_VALUE
                        FROM {temporary_table} RESULTS
                    LEFT JOIN {result} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL 
                    AND RESULTS.ID_ROW = STORED_RESULTS.ID_ROW
                    WHERE STORED_RESULTS.ID_PROCESS IS NOT NULL
                    AND RESULTS.FEATURE_VALUE <> 'STO error'
                    ) UPDATED_FEATURES
                    SET 
                        FEATURE_VALUE  = UPDATED_FEATURES.FEATURE_VALUE                 
                    WHERE
                        {result}.ID_PROCESS = UPDATED_FEATURES.ID_PROCESS
                    AND
                        {result}.ID_PARTITION = UPDATED_FEATURES.ID_PARTITION
                    AND
                        {result}.ID_ROW = UPDATED_FEATURES.ID_ROW
                    AND
                        {result}.ID_MODEL = UPDATED_FEATURES.ID_MODEL
                    """

        sql_queries['insert_new_error_feature_engineering'] = f"""
                    -- INSERT NEW MODELS
                    CURRENT VALIDTIME INSERT INTO {error_results}
                    (ID_PROCESS, ID_PARTITION, ID_MODEL,  STATUS)
                    SELECT
                          RESULTS.ID_PROCESS
                        , RESULTS.ID_PARTITION
                        , RESULTS.ID_MODEL
                        , RESULTS.STATUS
                    FROM {temporary_table} RESULTS
                    LEFT JOIN {error_results} STORED_RESULTS
                    ON RESULTS.ID_PROCESS = STORED_RESULTS.ID_PROCESS AND RESULTS.ID_PARTITION = STORED_RESULTS.ID_PARTITION
                    AND RESULTS.ID_MODEL = STORED_RESULTS.ID_MODEL  
                    WHERE STORED_RESULTS.ID_PROCESS IS NULL
                    AND RESULTS.FEATURE_VALUE = 'STO error';
                    """

        sql_queries['drop_temporary_table'] = f'DROP TABLE {temporary_table};'

        con = tdml.get_connection()

        if True:
            try:
                con.execute(sql_queries['drop_temporary_table'])
                con.execute(sql_queries['create_temporary_table'])
            except Exception as e:
                con.execute(sql_queries['create_temporary_table'])
            con.execute(sql_queries['session'])
            con.execute(sql_queries['create_view_sto_query'])
            con.execute(sql_queries['insert_results_temporary'])
            con.execute(sql_queries['insert_results'])
            con.execute(sql_queries['update_results'])
            con.execute(sql_queries['insert_new_error_feature_engineering'])
            nb_errors = tdml.get_context().execute(
                f"SEL count(*) FROM {temporary_table} WHERE FEATURE_VALUE = 'STO error'").fetchall()[0][0]
            if nb_errors > 0:
                print(f'{nb_errors} errors detected.')
                print(f'please check the {error_results} table or the corresponding view for more informations.')
            else:
                print(f'no error detected. Computations successful.')
                print(f'results are insterted or updated in {result}.')
            con.execute(sql_queries['drop_temporary_table'])

        if debug:
            return sql_queries

        return