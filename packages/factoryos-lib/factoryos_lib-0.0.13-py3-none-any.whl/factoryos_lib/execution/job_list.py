from ValiotWorker import QueueType

jobs = [
    {
        "model": "MovingAverage",
        "parameters": {
            "name": 'TEST_DATA_MA_FILTER',
            "alias": '',
            "description": "Description",
            "queueType": QueueType.FREQUENCY,
            "schedule": "*/60 * * * *",
            "enabled": True,
            "lockRequired": True

        },
        "input": {
            "variable": "TEST_DATA",
            "window": 10,
            "block_size": 50,
            "restart": False
        }
    }

    # ,{
    #     "model": "Snapshot",
    #     "parameters": {
    #         "name": 'SILOS_SNAPSHOT_TEST',
    #         "alias": 'Silos damper snapshot job',
    #         "description": "Script that creates a snapshot for each controller",
    #         "queueType": QueueType.FREQUENCY,
    #         "schedule": "*/1 * * * *",
    #         "enabled": False,
    #         "lockRequired": True
    #
    #     },
    #     "input": {
    #         "inputs_codes": [
    #             "^Silos_Nivel_Silo1$", "^Silos_Nivel_Silo2$", "^Silos_Nivel_Silo3$", "^Silos_Nivel_Silo4$", "^Silos_Nivel_Silo5$", "^Silos_Nivel_Silo6$",
    #             "^Silos_Humedad_Silo1$", "^Silos_Humedad_Silo2$", "^Silos_Humedad_Silo3$", "^Silos_Humedad_Silo4$", "^Silos_Humedad_Silo5$", "^Silos_Humedad_Silo6$",
    #             "^Silos_Contraccion_Silo1$", "^Silos_Contraccion_Silo2$", "^Silos_Contraccion_Silo3$", "^Silos_Contraccion_Silo4$", "^Silos_Contraccion_Silo5$", "^Silos_Contraccion_Silo6$"
    #         ],
    #         "setpoints_codes": ["^Silos_Humedad_DeMezcla_Setpoint$"],
    #         "machine_state": ["^Silos_Apertura_Silo1$", "^Silos_Apertura_Silo2$", "^Silos_Apertura_Silo3$",
    #                      "^Silos_Apertura_Silo4$", "^Silos_Apertura_Silo5$", "^Silos_Apertura_Silo6$"],
    #         "outputs_codes": ["^Silos_Apertura_Silo1_CTRL$", "^Silos_Apertura_Silo2_CTRL$", "^Silos_Apertura_Silo3_CTRL$",
    #                      "^Silos_Apertura_Silo4_CTRL$", "^Silos_Apertura_Silo5_CTRL$", "^Silos_Apertura_Silo6_CTRL$"]
    #     }
    # },
    # {
    #     "model": "Snapshot",
    #     "parameters": {
    #         "name": 'BURNER_DAMPER_SNAPSHOT_TEST',
    #         "alias": 'Burner damper snapshot job',
    #         "description": "Script that creates a snapshot for each controller",
    #         "queueType": QueueType.FREQUENCY,
    #         "schedule": "*/1 * * * *",
    #         "query": "",
    #         "enabled": False,
    #         "lockRequired": True
    #
    #     },
    #     "input": {
    #         "inputs_codes": ["^Atomizador_Rendimiento$", "^Atomizador_Humedad_PolvoAtomizado$"],
    #         "setpoints_codes": ["^Atomizador_Rendimiento_setpoint$", "^Atomizador_Humedad_PolvoAtomizado_setpoint$"],
    #         "machine_state": ["^Atomizador_Apertura_CompuertaQuemador$"],
    #         "outputs_codes": ["^Atomizador_Apertura_CompuertaQuemador_NN$",
    #                           "^Atomizador_Apertura_CompuertaQuemador_CTRL$"]
    #
    #     }
    # },
    # {
    #     "model":"NNModel",
    #     "parameters":{
    #         "name":'DEFLOCCULATING_FLOW_NN_V2',
    #         "alias":'test Liquid deflocculant Flow neural network controller',
    #         "description":"neural network model for predicting liquid deflocculant controller output",
    #         "queueType":QueueType.ON_DEMAND,
    #         "schedule":"*/60 * * * *",
    #         "enabled":True,
    #         "lockRequired":True
    #     },
    #     "input":{}
    # }

]
