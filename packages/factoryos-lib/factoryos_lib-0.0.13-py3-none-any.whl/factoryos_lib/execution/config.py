# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved


__author__ = ["FactoryOS Team"]

import os
from pygqlc import GraphQLClient
from dotenv import load_dotenv

load_dotenv('./.env')


def setup_gql():
    gql = GraphQLClient()
    gql.addEnvironment(
        'dev',
        url=os.environ.get('API_DEV'),
        wss=os.environ.get('WSS_DEV'),
        headers={'Authorization': os.environ.get('TOKEN_DEV')},
        timeoutWebsocket=35)
    gql.addEnvironment(
        'prod',
        url=os.environ.get('API'),
        wss=os.environ.get('WSS'),
        headers={'Authorization': os.environ.get('TOKEN')},
        timeoutWebsocket=35)
    # ! Sets the environment selected in the .env file
    gql.setEnvironment(os.environ.get('ENV'))
    return gql
