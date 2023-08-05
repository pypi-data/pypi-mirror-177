from ValiotWorker.Logging import LogLevel
from pygqlc import GraphQLClient

from factoryos_lib.base.inputs._input import Input
from factoryos_lib.base.queries import QueryException

gql = GraphQLClient()


class AllVariableInput(Input):
    VARIABLE_STATS = '''
        query($Code:String, $IdFrom:Float){
            variable(findBy:{code:$Code},){
            dataAggregates(aggregate:{
                count:VALUE
                average:VALUE
                sum:VALUE
            }){count average sum}        
        }
        }
    '''

    ALL_VARIABLE_DATA = '''
        query($Code:String){
           variable(findBy:{code:$Code},){          
                data(orderBy:{asc:ID})
                    {id value}
              }
            }
       '''

    @staticmethod
    def get_variable_data(code, caller=None):
        data, errors = gql.query_one(AllVariableInput.ALL_VARIABLE_DATA,
                                     variables={'Code': code})

        if errors:
            if caller:
                caller.log_callback(LogLevel.DEBUG, f"getVariableData error: {errors} ({code})")
            raise QueryException(errors)

        return data

    def get_data(self, variable_name, log):
        return AllVariableInput.get_variable_data(variable_name, log)
