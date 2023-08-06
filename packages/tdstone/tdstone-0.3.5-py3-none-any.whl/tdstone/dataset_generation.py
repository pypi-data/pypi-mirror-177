from tdstone.data_distribution import EquallyDistributed,setup_table_for_model_generation
import teradataml as tdml
import re
import pandas as pd
import numpy as np


def GenerateDataSet(n_x=9, n_f=1, n_partitions=2, n_rows=5,
                    noise_classif=0.01,
                    train_test_split_ratio = 0.2,
                    database=re.findall(string=str(tdml.get_context().url),pattern=r'DATABASE=(\w+)')[0]):
    """ A SQL query that generates in database a multi-partitioned dataset.

    For each partition, a set of independent random variables are generated.
    From these variables, two variables are calculated:
        - Y1 : as a linear combination of the continuous variable. The coef-
        ficients are constant all over the partition, i.e. a linear model is
        expected to fit the Y1 from the float features. The linear coefficients
        are generated randomly.
        - Y2 : is calculated from Y1 as equal to 1 when > than the average of
        Y1 over the partition, and 0 otherwise.
    As a matter of fact, Y1 can be used to train regression models and Y2 clas-
    sification models.

    :param n_x: number of float features following. These features are
    standardized with a zero mean.
    :param n_f: number of 2-level categorical variables. Levels are 0 and 1.
    :param n_partitions: number of partitions.
    :param n_rows: number of rows per partitions. All partitions exhibit the
    same number of rows.
    :param N: this number should be should be an integer greater than n_rows
    divided by the number of rows in dbc_columns
    :param noise_classif: add a noise to the classification
    :return: a SQL query and the column names.
    """

    N = int(n_partitions * n_rows / 99999 + 1)

    setup_table_for_model_generation(database)
    if n_x < 2:
        raise ValueError('The number of float features must be > 1 !')

    if n_f < 1:
        raise ValueError('The number of categorical feature must be > 0 !')

    if n_partitions < 1:
        raise ValueError('The number of partition must be > 0 !')

    if n_rows < 5:
        raise ValueError('The number of rows per partition must be > 4 !')

    random_x = """sqrt(-2.0*ln(CAST(RANDOM(1,999999999) AS FLOAT)/1000000000))
    * cos(2.0*3.14159265358979323846 * CAST(RANDOM(0,999999999) AS FLOAT)
    /1000000000)"""
    random_f = "RANDOM(0,1)"
    random_c = """RANDOM(0,1)*sqrt(-2.0 * ln(CAST(RANDOM(1,999999999) AS
    FLOAT)/1000000000)) * cos(2.0*3.14159265358979323846 *
    CAST(RANDOM(0,999999999) AS FLOAT)/1000000000)"""

    X_names = ['X'+str(i+1) for i in range(n_x)]
    F_names = ['flag'+str(i+1) for i in range(n_f)]
    if len(F_names) == 1:
        F_names = ['flag']

    ref_table = f"""
        (
         SELECT  pd
         FROM {database}.TABLE_FOR_GENERATION
         EXPAND ON duration AS pd BY ANCHOR PERIOD ANCHOR_SECOND
         ) B
    """

    query_long = f"""
            select
                row_number() over (
                    order by  pd) as RNK
            from
                {ref_table}"""

    if N > 1:
        for iter in range(N-1):
            query_long += f"""
                UNION ALL
                select
                row_number() over (
                    order by  pd)
                + (SEL count(*) FROM {ref_table})*({iter}+1)
                as RNK
            from
                {ref_table}"""

    if train_test_split_ratio > 1:
        train_test_split_condition = f"""CASE WHEN ID<{train_test_split_ratio} THEN 'train' ELSE 'test' END"""
    else:
        train_test_split_condition = f"""CASE WHEN ID<{train_test_split_ratio*n_rows} THEN 'train' ELSE 'test' END"""

    query = f"""
        SELECT AA.*
        , CASE WHEN (AA.Y1 + {random_x}*{noise_classif}> AVG(AA.Y1)
                     OVER (PARTITION BY AA.PARTITION_ID))
        THEN 1 ELSE 0 END AS Y2
        , {train_test_split_condition} as FOLD
        FROM (
        SELECT
            A.RNK as Partition_ID
        ,   B.RNK as "ID"
        ,   {', '.join([random_x+' as '+X_names[i] for i in range(n_x)])}
        ,   {','.join([random_f+' as '+F_names[i] for i in range(n_f)])}
        ,   {'+'.join(['C1_'+str(i+1)+'*'+X_names[i] for i in range(n_x)])}
        as Y1
        FROM
            (
            -- partitions
            select
                row_number() over (
                    order by  pd) as RNK
            ,   {', '.join([random_c+' as C1_'+str(i+1) for i in range(n_x)])}
            from
                {ref_table}
            qualify RNK < {n_partitions}+1
            ) A
        ,
            (
            -- inside partitions
            select * from
                (
                    {query_long}
                ) DD
            where DD.RNK < {n_rows}+1
            ) B
            ) AA
        """

    return query, X_names+F_names+['Y1', 'Y2']+['FOLD']


def introducemissingvalues(df_dataset, missing_values_proportions):
    def casewhenmissingvalues(variable, n_missing, n_total):
        return f'CASE WHEN RANDOM(1,{n_total}) < {n_total}-{n_missing} THEN {variable} END AS {variable}'

    def hasmissing(variable, missing_values_proportions):
        return variable in missing_values_proportions.keys()

    def transform(variable, missing_values_proportions):
        if hasmissing(variable, missing_values_proportions):
            return casewhenmissingvalues(variable, missing_values_proportions[variable][0],
                                         missing_values_proportions[variable][1])
        else:
            return variable

    query = f"""
    SELECT
    {','.join(list(map(lambda x: transform(x, missing_values_proportions), df_dataset.columns)))}
    FROM {df_dataset._table_name}
    """

    return query

GenerateEquallyDistributedDataSet = EquallyDistributed(GenerateDataSet)


def sql_random(distribution, data_type='float', center=None, half_width=None, one_ratio=None, total=None):
# Examples
# random_param_01 = {'data_type': 'int',
#                   'distribution': 'uniform',
#                   'center': 500,
#                   'half_width': 250
#                   }
# random_param_02 = {'data_type': 'float',
#                   'distribution': 'uniform',
#                   'center': 0,
#                   'half_width': 10
#                   }
# random_param_03 = {'data_type': 'float',
#                   'distribution': 'normal',
#                   'center': 0,
#                   'half_width': 1
#                   }
# print(sql_random(**random_param_01))
# print(sql_random(**random_param_02))
# print(sql_random(**random_param_03))

    if distribution == 'uniform':
        mu = center
        delta = half_width
        a = f'{mu} - {delta}'
        b = f'{mu} + {delta}'
        if data_type == 'int':
            return f'CAST(CAST(RANDOM(0,999999999) AS FLOAT)/999999999*(({b})-({a}))+({a}) AS BIGINT)'
        elif data_type == 'float':
            return f'CAST(RANDOM(0,999999999) AS FLOAT)/999999999*(({b})-({a}))+({a})'
    elif distribution == 'normal':
        mu = center
        sigma = half_width
        return f'''sqrt(-2.0*ln(CAST(RANDOM(1,999999999) AS FLOAT)/1000000000))*cos(2.0*3.14159265358979323846*CAST(RANDOM(0,999999999) AS FLOAT)/1000000000)*({sigma})+({mu})'''
    elif distribution == 'binomial':
        return f'CASE WHEN RANDOM(1,{total}) < {one_ratio} THEN 1 ELSE 0 END'
    return


def generaterandomsamples(df, random_params, nb_gen, id_columns='id',database=re.findall(string=str(tdml.get_context().url),pattern=r'DATABASE=(\w+)')[0]):

    setup_table_for_model_generation(database)

    def hastoberandomized(variable, random_params):
        return variable in random_params.keys()

    def transform(variable, random_params):
        if hastoberandomized(variable, random_params):
            return random_params[variable]
        else:
            return variable

    columns = [x for x in df.columns if x.lower() != id_columns.lower()]

    query = f"""
    SELECT
    {id_columns} as PARTITION_ID,
    row_number() OVER (ORDER BY {id_columns}, n__) as ID,
    {','.join(list(map(lambda x: transform(x, random_params) + f' AS {x}', columns)))}
    FROM {df._table_name} A,
    (SEL
		row_number() OVER (ORDER BY A.pd) as n__
	FROM
		(
		SELECT  pd
		FROM {database}.TABLE_FOR_GENERATION
		EXPAND ON duration AS pd BY ANCHOR PERIOD ANCHOR_SECOND
		) A
	QUALIFY n__ < {nb_gen}+1
    ) B
    """

    return tdml.DataFrame.from_query(query)

def generatesinglesensordata(table_name, schema_name,if_exists='replace',params = [1,1000,600.,100.,500.,200.,200.,25.,10.,300.,200.,0.05,200.,100.,1,260.]):
    df = pd.DataFrame([params], columns=['id','nbpts']+['x_param'+str(i+1) for i in range(5)]+['y_param'+str(i+1) for i in range(9)])
    tdml.copy_to_sql(df,table_name=table_name,schema_name=schema_name,if_exists=if_exists)
    return tdml.DataFrame(tdml.in_schema(schema_name,table_name))


def generationmultiplesignals(df_params, id_columns='id', id_partition=None, partition_id_number=1,database=re.findall(string=str(tdml.get_context().url),pattern=r'DATABASE=(\w+)')[0]):

    setup_table_for_model_generation(database)

    if id_partition is None:
        query = f"""
        SEL
            PARTITION_ID
        ,   ID
        ,	X0 AS X
        ,	Y AS Y
        FROM
        (
            SEL
                {partition_id_number} AS PARTITION_ID
            ,	TS.{id_columns} AS ID
            ,	CASE WHEN B.n< TS.nbpts THEN B.n END AS x0
            ,	SIN(X0/TS.x_param1)*TS.x_param2 AS x1
            ,	EXP((-1.)*(x0-TS.x_param3)*(x0-TS.x_param3)/TS.x_param4/TS.x_param4)*x_param5 AS x2
            ,	x0 + x1 + x2 AS x
            ,	EXP((-1)*x/TS.y_param1) AS y0
            ,	EXP((-1)*x/TS.y_param2) AS y1
            ,	EXP((-1)*(x-TS.y_param3)*(x-TS.y_param3)/TS.y_param4/TS.y_param4) AS y2
            ,   CASE WHEN TS.y_param8 > 0.5 AND x0 > TS.y_param9 THEN 0 ELSE 1 END AS flag
            ,	(y0 + y1 + y2*flag + TS.y_param5/sqrt(2)*sqrt(-2.0*ln(CAST(RANDOM(1,999999999) AS FLOAT)/1000000000))
            * cos(2.0*3.14159265358979323846 * CAST(RANDOM(0,999999999) AS FLOAT)
            /1000000000))*TS.y_param6+TS.y_param7 AS y
            FROM
            (
            SEL
                row_number() OVER (ORDER BY A.pd) as n
            FROM
                (
                SELECT  pd
                FROM {database}.TABLE_FOR_GENERATION
                EXPAND ON duration AS pd BY ANCHOR PERIOD ANCHOR_SECOND
                ) A
            ) B,
            {df_params._table_name} TS
            WHERE x0 IS NOT NULL
        ) GEN
        """
    else:
        query = f"""
        SEL
            PARTITION_ID
        ,   ID
        ,	X0 AS X
        ,	Y AS Y
        FROM
        (
            SEL
                TS.{id_partition} AS PARTITION_ID
            ,	TS.{id_columns} AS ID
            ,	CASE WHEN B.n< TS.nbpts THEN B.n END AS x0
            ,	SIN(X0/TS.x_param1)*TS.x_param2 AS x1
            ,	EXP((-1.)*(x0-TS.x_param3)*(x0-TS.x_param3)/TS.x_param4/TS.x_param4)*x_param5 AS x2
            ,	x0 + x1 + x2 AS x
            ,	EXP((-1)*x/TS.y_param1) AS y0
            ,	EXP((-1)*x/TS.y_param2) AS y1
            ,	EXP((-1)*(x-TS.y_param3)*(x-TS.y_param3)/TS.y_param4/TS.y_param4) AS y2
            ,   CASE WHEN TS.y_param8 > 0.5 AND x0 > TS.y_param9 THEN 0 ELSE 1 END AS flag
            ,	(y0 + y1 + y2*flag + TS.y_param5/sqrt(2)*sqrt(-2.0*ln(CAST(RANDOM(1,999999999) AS FLOAT)/1000000000))
            * cos(2.0*3.14159265358979323846 * CAST(RANDOM(0,999999999) AS FLOAT)
            /1000000000))*TS.y_param6+TS.y_param7 AS y
            FROM
            (
            SEL
                row_number() OVER (ORDER BY A.pd) as n
            FROM
                (
                SELECT  pd
                FROM {database}.TABLE_FOR_GENERATION
                EXPAND ON duration AS pd BY ANCHOR PERIOD ANCHOR_SECOND
                ) A
            ) B,
            {df_params._table_name} TS
            WHERE x0 IS NOT NULL
        ) GEN
        """

    return tdml.DataFrame.from_query(query)


def linspace(start=1, stop=100, step=1, name='n'):
    n_total = int((stop - start) / step) +1

    n_total_days = int(n_total / 24 / 60 / 60)
    n_total_hours = int((n_total - n_total_days * (24 * 60 * 60)) / (60 * 60))
    n_total_minutes = int((n_total - n_total_days * (24 * 60 * 60) - n_total_hours * (60 * 60)) / 60)
    n_total_secondes = int((n_total - n_total_days * (24 * 60 * 60) - n_total_hours * (60 * 60) - n_total_minutes * 60))

    #print(n_total, n_total_days, n_total_hours, n_total_minutes, n_total_secondes)
    query = f"""
    SELECT (row_number() OVER (ORDER BY pd) -1)*{step} + {start} AS {name}
    FROM (
        SELECT pd
        FROM (
            SEL PERIOD(TIMESTAMP '2005-02-02 00:00:00+02:00',TIMESTAMP '2005-02-02 00:00:00+02:00' 
            + INTERVAL '{n_total_days}' DAY 
            + INTERVAL '{n_total_hours}' HOUR 
            + INTERVAL '{n_total_minutes}' MINUTE
            + INTERVAL '{n_total_secondes}' SECOND) AS TIME_SLICE
            FROM (
                SEL TOP 1 * FROM dbc.dbcinfo
            ) B
        ) A
        EXPAND ON TIME_SLICE AS pd BY INTERVAL '1' SECOND
    ) A2
    """

    return query

def generaterandomsignalparams(spreading=10, one_ratio=5, total=100):
    random_params = {
        'nbpts': sql_random(distribution='uniform', center='nbpts', half_width=500, data_type='int'),
    }
    random_params.update({'x_param' + str(i): sql_random(distribution='normal', center='x_param' + str(i),
                                                         half_width='x_param' + str(i) + '/' + str(spreading),
                                                         data_type='float') for i in range(5)})
    random_params.update({'y_param' + str(i): sql_random(distribution='normal', center='y_param' + str(i),
                                                         half_width='y_param' + str(i) + '/' + str(spreading),
                                                         data_type='float') for i in range(7)})
    random_params.update({'y_param8': sql_random(distribution='binomial', one_ratio=one_ratio, total=total)})
    random_params.update({'y_param9': sql_random(distribution='normal', center='y_param9', half_width='y_param9/'+str(spreading), data_type='float')})
    del random_params['y_param5']

    return random_params


def GenerateDataSetIoT(schema_name, nb_partitions, nb_signals_per_partitions,spreading_inter=8,spreading_intra=10, one_ratio=5, total=100):
    # generation params
    singlesignalparam = generatesinglesensordata(table_name='ts_params', schema_name=schema_name)

    # randomize parameter inter partition
    random_interpartition = generaterandomsignalparams(spreading=spreading_inter, one_ratio=0, total=100)
    random_intrapartition = generaterandomsignalparams(spreading=spreading_intra, one_ratio=one_ratio, total=total)
    params_partitions = generaterandomsamples(singlesignalparam, random_interpartition, nb_partitions).drop(
        columns='PARTITION_ID')
    shape0 = params_partitions.shape

    params_signals = generaterandomsamples(params_partitions, random_intrapartition, nb_signals_per_partitions)
    shape1 = params_signals.shape
    # generate the signals
    df_signals = generationmultiplesignals(params_signals, id_columns='id', id_partition='partition_id')

    return df_signals.show_query(), ['X', 'Y']

GenerateEquallyDistributedDataSetIoT = EquallyDistributed(GenerateDataSetIoT)



def GenerateDatasetSeries(table_name, nb_partitions=20000,nb_coeffs=6, noise = 0.01, series_length=120,database=re.findall(string=str(tdml.get_context().url),pattern=r'DATABASE=(\w+)')[0]):
    coeffs = ','.join(['CAST(RANDOM(-9999999,9999999) AS FLOAT)/2/9999999*EXP((-10.)*(1-1)) AS A'+str(i+1) for i in range(nb_coeffs)])
    module = 'SQRT('+'+'.join(['A'+str(i+1)+'**2' for i in range(nb_coeffs)])+')'
    normalized_coeffs = ','.join([f'A{i+1} / Module*0.99 AS A{i+1}_' for i in range(nb_coeffs)])

    N =int( nb_partitions/9999)+1

    ref_table = f"""
            (
             SELECT  pd
             FROM {database}.TABLE_FOR_GENERATION
             EXPAND ON duration AS pd BY ANCHOR PERIOD ANCHOR_SECOND
             ) B
        """

    query_long = f"""
            select
                row_number() over (
                    order by  pd) as pd
            from
                {ref_table}"""

    if N > 1:
        for iter in range(N-1):
            query_long += f"""
                UNION ALL
                select
                row_number() over (
                    order by  pd)
                + (SEL count(*) FROM {ref_table})*({iter}+1)
                as pd
            from
                {ref_table}"""


    query_coeffs = f"""
    CREATE TABLE {database}.TEMP_COEFFS AS
    (
    SEL
        CASE WHEN E.n< {nb_partitions}+1 THEN E.n END AS PARTITION_ID
    ,	CASE WHEN B.n< 2 THEN B.n END AS ID
    ,	{coeffs}
    ,	{module} as Module
    ,	{normalized_coeffs}
    FROM
    (
    SEL
        row_number() OVER (ORDER BY A.pd) as n
    FROM
        (
        SELECT  pd
        FROM {database}.TABLE_FOR_GENERATION
        EXPAND ON duration AS pd BY ANCHOR PERIOD ANCHOR_SECOND
        ) A
    ) B
    ,
    (
    SEL
        row_number() OVER (ORDER BY A.pd) as n
    FROM
        (
        {query_long}
        ) A
    ) E
    WHERE PARTITION_ID IS NOT NULL AND ID IS NOT NULL
    ) WITH DATA
    NO PRIMARY INDEX
    """

    variables = ','.join(['X'+str(i+1) for i in range(nb_coeffs)])
    init_variables = ','.join(['CAST(RANDOM(-9999999,9999999) AS FLOAT)/2/9999999/10 AS X'+str(i+1) for i in range(nb_coeffs)])
    calculated_variables = '+'.join([f'direct.X{i+1}*coeffs.A{i+1}_' for i in range(nb_coeffs)])
    shifted_variables = ','.join([f'direct.X{i+1} as X{i+2}' for i in range(nb_coeffs-1)])

    query_generation = f"""
    CREATE TABLE {database}.{table_name} AS
    (
    WITH RECURSIVE temp_table (PARTITION_ID, ID, {variables}, depth) AS
    ( 
        SEL
            PARTITION_ID
        ,	ID
        ,	{init_variables}
        ,	0 as depth
        FROM
        {database}.TEMP_COEFFS coeffs
    UNION ALL
      SELECT 
            direct.PARTITION_ID as ID
      ,		direct.ID + 1 as ID
      ,		{calculated_variables}*0.9 + CAST(RANDOM(-9999999,9999999) AS FLOAT)/2/9999999*{noise}  as X1
      ,		{shifted_variables}
      ,     direct.depth+1 AS newdepth
      FROM temp_table direct, {database}.TEMP_COEFFS coeffs
      WHERE direct.PARTITION_ID = coeffs.PARTITION_ID
      AND newdepth < {series_length+1}
    )
    SELECT PARTITION_ID, ID, X1 as Y FROM temp_table
    ) WITH DATA
    PRIMARY INDEX (PARTITION_ID)
    """

    try:
        tdml.get_context().execute(f'DROP TABLE {database}.TEMP_COEFFS')
    except:
        print(f'unable to drop {database}.TEMP_COEFFS')
    tdml.get_context().execute(query_coeffs)
    print(f'{database}.TEMP_COEFFS created')
    try:
        tdml.get_context().execute(f'DROP TABLE {database}.{table_name}')
    except:
        print(f'unable to drop {database}.{table_name}')
    tdml.get_context().execute(query_generation)
    print(f'{database}.{table_name} created')

    return tdml.DataFrame(tdml.in_schema(database,table_name))