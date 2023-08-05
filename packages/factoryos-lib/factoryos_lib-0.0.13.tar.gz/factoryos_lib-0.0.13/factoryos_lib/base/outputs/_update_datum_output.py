from ValiotWorker.Logging import LogLevel

from factoryos_lib.base.mutations import MutationException
from factoryos_lib.base.outputs._output import Output
from pygqlc import GraphQLClient

gql = GraphQLClient()


class UpdateDatumOutput(Output):
    UPDATE_DATUM = '''mutation update_datum($Datum:ID, $Value: Float, $Code:String){
     updateDatum(
        id:$Datum
        datum:{value:$Value variableCode:$Code}
        ){
            successful
            messages{message}
        }
    }
    '''

    @staticmethod
    def update_datum(id_datum, value, code, caller=None):
        data, errors = gql.mutate(UpdateDatumOutput.UPDATE_DATUM,
                                  variables={
                                      'Datum': id_datum,
                                      'Value': value,
                                      'Code': code
                                  })
        if errors:
            if caller:
                caller.log_callback(LogLevel.INFO, f'Error updating datum {errors}...{value}')
            raise MutationException(errors)

        return data

    def save_output(self, variable_name, y, y_id, log):
        for i in range(len(y)):
            UpdateDatumOutput.update_datum(y_id[i], y[i], variable_name, log)
