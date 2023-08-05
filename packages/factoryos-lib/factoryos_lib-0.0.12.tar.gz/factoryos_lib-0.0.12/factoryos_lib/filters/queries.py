from ValiotWorker.Logging import LogLevel
from pygqlc import GraphQLClient
from retrying import retry

gql = GraphQLClient()


class QueryException(Exception):
    pass


def retry_if_query_exception(exception):
    return isinstance(exception, QueryException)


VARIABLE = '''query($Code:String){
  variable(findBy:{code:$Code}){
    name
    code
    unit{id}
  }
}
'''

VARIABLE_DATA = '''
query($Code:String, $IdFrom:Float){
  variable(findBy:{code:$Code},){
    data(
      orderBy:{asc:ID}
      limit:200
      filter:{compare:{attribute:ID,greater:$IdFrom}}){id insertedAt updatedAt value}
  }
}}'''

VARIABLE_DATA_START = '''query($Code:String, $BlockSize:Int){
  variable(findBy:{code:$Code}){
    data(
        orderBy:{asc:ID}
        limit:$BlockSize
    ){id insertedAt value}
  }
}'''


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_variable_data(code, block, from_id, caller=None):
    data = None
    errors = None
    if from_id is None:
        data, errors = gql.query_one(VARIABLE_DATA_START,
                                     variables={'Code': code,
                                                'BlockSize': block})
    else:
        data, errors = gql.query_one(VARIABLE_DATA,
                                     variables={'Code': code,
                                                'BlockSize': block,
                                                'IdFrom': float(from_id)})

    if errors:
        if caller:
            caller.log_callback(LogLevel.DEBUG, f"getVariableData error: {errors} ({code})")
        raise QueryException(errors)

    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def exist_variable(code, caller=None):
    data, errors = gql.query_one(VARIABLE,
                                 variables={'Code': code})
    if errors:
        if caller:
            caller.log_callback(LogLevel.DEBUG, f"existVariable error: {errors} ({code})")
        return False

    return True


GET_VARIABLE_COUNT = '''query($Code:String){
    variable(findBy:{code:$Code}){
        id
        dataAggregates(aggregate:{count:VALUE}){count}
    }
}
'''


def get_variable_count(variable, caller=None):
    data, errors = gql.query_one(GET_VARIABLE_COUNT,
                                 variables={
                                     'Code': variable
                                 })
    if errors:
        if caller:
            caller.log_callback(LogLevel.INFO, f'Error getting variable  {errors}...')
        raise QueryException()

    if data and data["dataAggregates"] and data["dataAggregates"]["count"]:
        return data["dataAggregates"]["count"]
    else:
        return 0

