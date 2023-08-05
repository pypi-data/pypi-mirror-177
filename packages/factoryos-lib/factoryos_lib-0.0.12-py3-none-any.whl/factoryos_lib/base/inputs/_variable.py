from ValiotWorker.Logging import LogLevel
from pygqlc import GraphQLClient

from factoryos_lib.base.inputs._input import Input
from factoryos_lib.base.queries import QueryException

gql = GraphQLClient()


class VariableInput(Input):
    VARIABLE_DATA = '''
        query($Code:String, $BlockSize:Int, $IdFrom:Float){
            variable(findBy:{code:$Code}){
            data(
                orderBy:{asc:INSERTED_AT}
                limit:$BlockSize
              filter:{compare:{attribute:ID,greater:$IdFrom}})
            {id insertedAt value}
      }
    }'''

    VARIABLE_DATA_START = '''query($Code:String, $BlockSize:Int){
      variable(findBy:{code:$Code}){
        data(
            orderBy:{asc:ID}
            limit:$BlockSize
        ){id insertedAt value}
      }
    }'''

    @staticmethod
    def get_variable_data(code, block, restart, from_id, caller=None):
        data = None
        errors = None
        if restart:
            data, errors = gql.query_one(VariableInput.VARIABLE_DATA_START,
                                         variables={'Code': code,
                                                    'BlockSize': block})
        else:
            data, errors = gql.query_one(VariableInput.VARIABLE_DATA,
                                         variables={'Code': code,
                                                    'BlockSize': block,
                                                    'IdFrom': float(from_id)})

        if errors:
            if caller:
                caller.log_callback(LogLevel.DEBUG, f"getVariableData error: {errors} ({code})")
            raise QueryException(errors)

        return data

    def get_data(self, variable_name, size, restart, id_in, log):
        data_in = []
        if restart:
            data_in = VariableInput.get_variable_data(variable_name, size, restart, None, log)
        else:
            data_in = VariableInput.get_variable_data(variable_name, size, restart, id_in, log)

        return data_in
