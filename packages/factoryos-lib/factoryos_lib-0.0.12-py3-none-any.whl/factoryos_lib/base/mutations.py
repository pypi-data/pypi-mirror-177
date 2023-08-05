# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved


__author__ = ["FactoryOS Team"]

import pydash as __
from pygqlc import GraphQLClient
from retrying import retry
from ValiotWorker.Logging import LogLevel
from ValiotWorker.Logging import log
import json

gql = GraphQLClient()


class MutationException(Exception):
    pass


def retry_if_mutation_exception(exception):
    return isinstance(exception, MutationException)


CREATE_DATUM_RETURNING_ID = '''mutation($code: String, $value: Float){
    createDatum(
        variableCode:$code
        value:$value
    )
    {
        result{id insertedAt}, 
        successful
        messages{message field}
    }
}'''

CREATE_CONTROLLER_EXECUTION = '''mutation($controllerName:String, $inputs:[CreateControllerInputNestedParams], $outputs:[CreateControllerOutputNestedParams], $feedback_alert_event_id:ID){
  createControllerExecution(
    controllerName:$controllerName
    createInputs:$inputs
    createOutputs:$outputs
    alertEvent:$feedback_alert_event_id
  ){
    successful
    messages{message code field}
  }
}'''

CREATE_CONTROLLER_EXECUTION = '''mutation($controllerName:String, $inputs:[CreateControllerInputNestedParams], $outputs:[CreateControllerOutputNestedParams], $feedback_alert_event_id:ID){
  createControllerExecution(
    controllerName:$controllerName
    createInputs:$inputs
    createOutputs:$outputs
    alertEvent:$feedback_alert_event_id
  ){
    successful
    messages{message code field}
  }
}'''

CREATE_ALERT_EVENT = '''mutation($description:Text,$alertId:ID,$triggeredAt:DateTime){
  createAlertEvent(
    alertId: $alertId
    resolved: false
    description: $description,
    triggeredAt: $triggeredAt
  )
  {
    successful
    result{
      id
    }
  }
}'''

UPDATE_VARIABLE = '''mutation($code: String, $value: Float){
    createDatum(
        variableCode:$code
        value:$value
    )
    {
        successful
        messages{message field}
    }
}'''

UPDATE_TRAINING_DATA = '''mutation($controllerName:String,$trainingData:Jsonb){
  createTrainingDatum(
      controllerName:$controllerName,
      trainingData:$trainingData){
    result{
      id
      trainingData
      controller{
        name
      }
    },
    successful
    messages{message field}
  }
}'''

CREATE_BULK_TRAINING_DATA = '''mutation($TDs: [CreateBulkTrainingDatumParams]){
  createBulkTrainingData(trainingData: $TDs)
  {
    successful
    result{
      trainingData{id insertedAt}
    }
  }
}'''

CREATE_BULK_TRAINING_DATA2 = '''mutation{
  createBulkTrainingData(trainingData: [{controllerName: "DEFLOCCULATING_FLOW_NN", trainingData:"{}"}])
  {
    successful
    result{
      trainingData{id insertedAt}
    }
  }
}'''

UPDATE_MODEL = '''mutation($controllerName:String,$model:Jsonb){
  createControllerModel(
      controllerName:$controllerName,
      model:$model){
    result{
      id
      model
      controller{
        name
      }
    },
    successful
    messages{message field}
  }
}'''

UPDATE_BULK_CONTROLLER_EXECUTIONS = '''mutation($CEs:[UpdateBulkControllerExecutionParams]){
  updateBulkControllerExecutions(controllerExecutions: $CEs)
  {
    successful
    result{
     controllerExecutions{trainingDatumAvailable}
    }
  }
}'''

UPDATE_BULK_ALERT_EVENTS = '''mutation($AlertEvents:  [UpdateBulkAlertEventParams]){
  updateBulkAlertEvents(alertEvents: $AlertEvents)
  {
    successful
    result{
      alertEvents{
        resolved
      }
    }
    messages{
      code
      message
      field
    }
  }
}'''


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def postControllerExecution(controllerName, inputs, outputs,
                            feedback_alert_event_id, caller=None):
    if feedback_alert_event_id != None:
        feedback_alert_event_id = int(feedback_alert_event_id)
    else:
        feedback_alert_event_id = ""

    data, errors = gql.mutate(CREATE_CONTROLLER_EXECUTION,
                              variables={
                                  'controllerName':
                                      controllerName,
                                  'inputs':
                                      inputs,
                                  'outputs':
                                      outputs,
                                  'feedback_alert_event_id':
                                      feedback_alert_event_id
                              })
    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"postControllerExecution error: {errors} ({caller.job_name})")
        raise MutationException(errors)

    return data


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def postAlertEvent(alertId, description, triggeredAt, caller=None):
    data, errors = gql.mutate(CREATE_ALERT_EVENT,
                              variables={
                                  'alertId': int(alertId),
                                  'description': description,
                                  'triggeredAt': triggeredAt
                              })
    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"postAlertEvent error: {errors} ({caller.job_name})")
        raise MutationException(errors)

    alert_id = data["result"]["id"]
    return alert_id


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def postOutputData(variableCode, value, caller=None):
    data, errors = gql.mutate(CREATE_DATUM_RETURNING_ID,
                              variables={
                                  'code': variableCode,
                                  'value': float(value)
                              })
    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"postOutputData error: {errors} ({caller.job_name})")
        raise MutationException(errors)

    output_id = data["result"]["id"]
    output_insertedAt = data["result"]["insertedAt"]

    return output_id, output_insertedAt


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def postVariableData(variableCode, value, caller=None):
    data, errors = gql.mutate(UPDATE_VARIABLE,
                              variables={
                                  'code': variableCode,
                                  'value': float(value)
                              })
    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"postVariableData error: {errors} ({caller.job_name})")
        raise MutationException(errors)


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def postTrainingData(name, value, caller=None):
    json_value = json.dumps(value)
    data, errors = gql.mutate(UPDATE_TRAINING_DATA,
                              variables={
                                  'controllerName': name,
                                  'trainingData': json_value
                              })
    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"postTrainingData error: {errors} ({caller.job_name})")
        raise MutationException(errors)


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def postBulkTrainingData(tds, caller=None):
    # td = {"controllerName": "DEFLOCCULATING_FLOW_NN", "trainingData":json.dumps({})}
    # tds = [td]
    data, errors = gql.mutate(CREATE_BULK_TRAINING_DATA,
                              variables={'TDs': tds})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"postBulkTrainingData error: {errors} ({caller.job_name})")
        raise MutationException(errors)


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def postModel(ctrl_name, controller_model_json, caller=None):
    data, errors = gql.mutate(UPDATE_MODEL,
                              variables={
                                  'controllerName': ctrl_name,
                                  'model': controller_model_json
                              })
    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"postModel error: {errors} ({caller.job_name})")
        raise MutationException(errors)


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def updateBulkControllerExecutions(ces, caller=None):
    # ce = {"id": 148, "controllerExecution": {"trainingDatumAvailable": False}}
    # ces = [ce]
    data, errors = gql.mutate(UPDATE_BULK_CONTROLLER_EXECUTIONS,
                              variables={'CEs': ces})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"postBulkTrainingData error: {errors} ({caller.job_name})")
        raise MutationException(errors)


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def updateBulkAlertEvents(aes, caller=None):
    # ae = {"alertEvent": {"resolved": true}, "id": 1169}
    # aes = [ae]
    data, errors = gql.mutate(UPDATE_BULK_ALERT_EVENTS,
                              variables={'AlertEvents': aes})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"updateBulkAlertEvents error: {errors} ({caller.job_name})")
        raise MutationException(errors)


CREATE_VARIABLE = '''mutation ($Name: String){
  createVariable(
        code:$Name
        enabled:true
        name:$Name
        unitId:1
    ){
    successful
    messages{message}
   }
}
'''


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def create_variable(name, caller=None):
    data, errors = gql.mutate(CREATE_VARIABLE,
                              variables={
                                  'Name':
                                      name
                              })
    if errors:
        if caller:
            caller.log_callback(LogLevel.INFO, f'Error creating variable {errors}...{name}')

        raise MutationException(errors)

    return data


CREATE_DATUM = '''mutation($Variable:String, $Value: Float){
createDatum(
    variableCode: $Variable
    value:$Value
  ){
    successful
    messages{message}
  }
}
'''


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def create_datum(variable, value, caller=None):
    data, errors = gql.mutate(CREATE_DATUM,
                              variables={
                                  'Variable':
                                      variable,
                                  'Value':
                                      value
                              })
    if errors:
        if caller:
            caller.log_callback(LogLevel.INFO, f'Error creating datum {errors}...{value}')
        raise MutationException(errors)

    return data


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


@retry(retry_on_exception=retry_if_mutation_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def update_datum(id_datum, value, code, caller=None):
    data, errors = gql.mutate(UPDATE_DATUM,
                              variables={
                                  'Datum':
                                      id_datum,
                                  'Value':
                                      value,
                                  'Code':
                                      code
                              })
    if errors:
        if caller:
            caller.log_callback(LogLevel.INFO, f'Error updating datum {errors}...{value}')
        raise MutationException(errors)

    return data
