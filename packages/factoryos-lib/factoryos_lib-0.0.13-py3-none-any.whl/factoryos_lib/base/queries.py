# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved


__author__ = ["FactoryOS Team"]

from retrying import retry
from ValiotWorker.Logging import  LogLevel
from pygqlc import GraphQLClient

gql = GraphQLClient()


class QueryException(Exception):
    pass


def retry_if_query_exception(exception):
    return isinstance(exception, QueryException)


VARIABLE_DATA = '''query($Code:String){
  variable(findBy:{code:$Code}){
    data(orderBy:{desc:INSERTED_AT}){value}
  }
}'''

VARIABLE_DATA_AND_ID = '''query($Code:String){
  variable(findBy:{code:$Code}){
    data(orderBy:{desc:INSERTED_AT}){value id}
  }
}'''

VARIABLE_DATA_AND_ID_LIMIT = '''query($Code:String,$Limit:Int){
  variable(findBy:{code:$Code}){
    data(orderBy:{desc:INSERTED_AT} limit:$Limit){value id}
  }
}'''

CONTROLLER_DATA = '''query($Name:String){
  controller(findBy:{name:$Name}){
    modelHistory(orderBy:{desc:INSERTED_AT}){model}
  }
}'''

CONTROLLER_MODEL_WITH_ALERTS_ID = '''query($Name:String){
  controller(findBy:{name:$Name}){
    modelHistory(orderBy:{desc:INSERTED_AT}){model}
    controlOutputAlert
    feedbackAlert
  }
}'''

ENABLED_CONTROLLERS = '''query{
  controllers(filter: { enabled: true }
    orderBy: { asc: ID }){
    modelHistory(orderBy:{desc:INSERTED_AT} limit:1){model}
    name
  }
}'''

TRAINING_DATA = '''query($Name:String){
  controller(findBy:{name:$Name}){
    trainingDataHistory(orderBy:{desc: INSERTED_AT}){trainingData}
  }
}'''

NEWEST_TRAINING_DATA_BATCH = '''query($ControllerName:String, $Cursor:Int, $BatchSize:Int){
  trainingDataPaginate(
    filter: { controllerName: $ControllerName }
    cursor: $Cursor
    orderBy: { asc: ID }
    limit: $BatchSize
  ) {
    edge {
      trainingData
      id
      insertedAt
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}'''

GET_VALIDATION_DATA_BATCH = '''query($ControllerName:String, $Cursor:Int, $BatchSize:Int){
  validationDataPaginate(
    filter: { controllerName: $ControllerName }
    cursor: $Cursor
    orderBy: { asc: ID }
    limit: $BatchSize
  ) {
    edge {
      validationData
      id
      insertedAt
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}'''

GET_ALL_UNSOLVED_CONTROLLER_EXECUTION = '''query($ControllerName:String){
  controllerExecutions(
    filter: { controllerName: $ControllerName trainingDatumAvailable: false}
    orderBy: { desc: INSERTED_AT }
    limit: 1000
  ) {
    _requestId
    inputs(orderBy: { asc: ID }){input, setPoint}
    outputs(orderBy: { asc: ID }){output, currentValue, feedback}
    trainingDatumAvailable
    alertEvent
    id
  }
}'''

GET_ALL_UNSOLVED_ALERT_EVENTS_BY_ALERT_ID = '''query($ID:ID){
  alert(id: $ID)
  {
    events(orderBy: {desc: INSERTED_AT} filter: {resolved: false}){
      resolvedBy
      resolved
      id
    },
  }
}'''

CHECK_ALERT_EVENT_RESOLVED = '''query($ID:ID){
  alertEvent(id: $ID)
  {
    resolved
    _requestId
  }
}'''

GET_VARIABLE_DATA_BY_ID = '''query($ID:ID){
  datum(id: $ID)
  {
    value
  }
}'''

GET_LAST_TD_WITH_A_SPECIFIC_INPUT = '''query($ControllerName:String, $inputs:String){
  trainingData(
    filter: {controllerName: $ControllerName trainingData: {contains: $inputs}}
    orderBy: { desc: INSERTED_AT }
    limit: 1
  ) {
    insertedAt
  }
}'''

GET_REPEATED_TDS = '''query($ControllerName:String, $inputs:String, $afterDate:DateTime, $beforeDate:DateTime){
  trainingData(
    filter: {
      controllerName: $ControllerName
      trainingData: {contains: $inputs} 
      before: {date: $beforeDate, attribute: INSERTED_AT}
      after: {date: $afterDate, attribute: INSERTED_AT}
    }
    orderBy: { desc: INSERTED_AT }
  ) {
    insertedAt
  }
}'''


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getVariableDataAndId(variableCode, caller=None):
    value = None
    id = None
    errors = []
    errors = []
    data, errors = gql.query_one(VARIABLE_DATA_AND_ID,
                                 variables={'Code': variableCode})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getVariableDataAndId error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    if type(data).__name__ == 'list':
        value = float(data[0]["value"])
        id = data[0]["id"]
    elif data:
        value = float(data["value"])
        id = data["id"]

    return id, value, errors

@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getVariableDataAndId(variableCode, limit, caller=None):
    value = None
    id = None
    errors = []
    errors = []
    data, errors = gql.query_one(VARIABLE_DATA_AND_ID_LIMIT,
                                 variables={'Code': variableCode, "Limit":limit})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getVariableDataAndId error: {errors} ({caller.job_name})")
        raise QueryException(errors)



    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getModelWithAlertsID(jobName, caller=None):
    model = {}
    errors = []
    data, errors = gql.query_one(CONTROLLER_MODEL_WITH_ALERTS_ID, variables={'Name': jobName})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getModelWithAlertsID error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    model = data["modelHistory"][0]["model"]
    controlOutputAlertID = data["controlOutputAlert"]
    feedbackAlertID = data["feedbackAlert"]

    return feedbackAlertID, controlOutputAlertID, model


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getAllEnabledControllers(caller=None):
    errors = []
    data, errors = gql.query_one(ENABLED_CONTROLLERS)

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getAllEnabledControllers error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getVariableData(variableCode, caller=None):
    value = None
    errors = []
    data, errors = gql.query_one(VARIABLE_DATA,
                                 variables={'Code': variableCode})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getVariableData error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    if data:
        if type(data).__name__ == 'list':
            value = float(data[0]["value"])
        else:
            value = data
    return value, errors


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getModel(jobName, caller=None):
    model = {}
    errors = []
    data, errors = gql.query_one(CONTROLLER_DATA, variables={'Name': jobName})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getModel error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    if data:
        if type(data).__name__ == 'dict':
            data = [{'model': data}]
    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getTD(jobName, caller=None):
    td = {}
    errors = []
    data, errors = gql.query_one(TRAINING_DATA, variables={'Name': jobName})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getTD error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    if data:
        if type(data).__name__ == 'dict':
            data = [{'trainingData': data}]
    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getTDBatch(jobName, cursor, batchSize, caller=None):
    jobNameRegex = "^" + jobName + "$"
    data, errors = gql.query_one(NEWEST_TRAINING_DATA_BATCH, variables={
        'ControllerName': jobNameRegex, 'Cursor': cursor, 'BatchSize': batchSize})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getTDBatch error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getAllUnsolvedControllerExecution(model_name, caller=None):
    model_name_regex = "^" + model_name + "$"
    data, errors = gql.query_one(GET_ALL_UNSOLVED_CONTROLLER_EXECUTION, variables={
        'ControllerName': model_name_regex})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getAllUnsolvedControllerExecution error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    if data == None:
        data = []

    if type(data).__name__ != 'list':
        data = [data]

    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getAllUnsolvedAlertEvents(id, caller=None):
    data, errors = gql.query_one(GET_ALL_UNSOLVED_ALERT_EVENTS_BY_ALERT_ID, variables={
        'ID': id})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getAllUnsolvedAlertEvents error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    if data == None:
        data = []

    if type(data).__name__ != 'list':
        data = [data]

    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def checkAlertEventResolved(alert_id, caller=None):
    data, errors = gql.query_one(CHECK_ALERT_EVENT_RESOLVED, variables={
        'ID': alert_id})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"checkAlertEventResolved error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    if data != [] or data != None:
        return data["resolved"]
    else:
        return False


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getVariableDatabyId(data_id, caller=None):
    data, errors = gql.query_one(GET_VARIABLE_DATA_BY_ID, variables={
        'ID': int(data_id)})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getVariableDatabyId error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getVDBatch(jobName, cursor, batchSize, caller=None):
    jobNameRegex = "^" + jobName + "$"
    data, errors = gql.query_one(GET_VALIDATION_DATA_BATCH, variables={
        'ControllerName': jobNameRegex, 'Cursor': cursor, 'BatchSize': batchSize})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getVDBatch error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getLastTDWithSpecificInput(jobName, inputs, caller=None):
    jobNameRegex = "^" + jobName + "$"
    inputs = '{\"inputs\": ' + f"{inputs}" + "}"
    errors = []
    data, errors = gql.query_one(GET_LAST_TD_WITH_A_SPECIFIC_INPUT, variables={
        'ControllerName': jobNameRegex, 'inputs': inputs})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getLastTDWithSpecificInput error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    return data


@retry(retry_on_exception=retry_if_query_exception, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getRepeatedTDs(jobName, inputs, before, after, caller=None):
    jobNameRegex = "^" + jobName + "$"
    inputs = '{\"inputs\": ' + f"{inputs}" + "}"

    before = before.strftime("%Y-%m-%dT%H:%M:%SZ")
    after = after.strftime("%Y-%m-%dT%H:%M:%SZ")

    errors = []
    data, errors = gql.query_one(GET_REPEATED_TDS, variables={
        'ControllerName': jobNameRegex, 'inputs': inputs, 'beforeDate': before, 'afterDate': after})

    if errors:
        if caller:
            caller.log_callback(
                LogLevel.DEBUG, f"getLastTDWithSpecificInput error: {errors} ({caller.job_name})")
        raise QueryException(errors)

    if data is None:
        data = []
    elif type(data).__name__ != 'list':
        data = [data]

    return data
