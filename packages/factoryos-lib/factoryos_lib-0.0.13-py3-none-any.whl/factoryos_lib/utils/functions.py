from random import randrange

import matplotlib.pyplot as plt

from factoryos_lib.base import mutations as m
from factoryos_lib.filters import queries as q
from factoryos_lib.execution.config import setup_gql

gql = setup_gql()

repository_variable_id = 751
code = "REPOSITORY_DATUM"


def add_random_data(variable_name, num_points):
    x = 10
    for i in range(num_points):
        m.create_datum(variable_name, x)
        x = x + randrange(-10, 10)


def empty_data(variable, block):
    raw = q.get_variable_data(variable, block, None, None)
    ids = list(map(lambda x: x["id"], raw))
    for i in ids:
        m.update_datum(i, 0, code)


def clear_data(variable, block):
    raw = q.get_variable_data(variable, block, None, None)
    ids = list(map(lambda x: x["id"], raw))
    for i in ids:
        m.update_datum(i, 0, variable)


def plot_variable(variable_1, variable_2, size):
    raw_x = q.get_variable_data(variable_1, size, None, None)
    y_points = list(map(lambda x: x["value"], raw_x))

    raw_x_2 = q.get_variable_data(variable_2, size, None, None)
    y_points_2 = list(map(lambda x: x["value"], raw_x_2))

    plt.plot(y_points, color="blue")
    plt.plot(y_points_2, color="red")

    plt.show()


plot_variable("TEST_DATA", "TEST_DATA_EMA_FILTER", 150)
