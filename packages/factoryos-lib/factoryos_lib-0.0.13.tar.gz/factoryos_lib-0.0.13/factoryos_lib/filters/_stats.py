from factoryos_lib.base.inputs import AllVariableInput
from factoryos_lib.base.outputs import UpdateDatumOutput
from factoryos_lib.filters._filter import Filter
import numpy as np
from . import queries as q
from factoryos_lib.base import mutations as m


class Stats(Filter):

    def set_inputs(self, kwargs):
        self.X_name = kwargs["input"]["variable"]

    def get_data(self):
        self.check_filter_variable()
        count_variable_in = q.get_variable_count(self.Y_name, self)
        if count_variable_in == 0:
            m.create_datum(self.Y_name, 0, self)
            m.create_datum(self.Y_name, 0, self)

        var_input = AllVariableInput()

        data_in = var_input.get_data(self.X_name,
                                     self)
        data_out = var_input.get_data(self.Y_name,
                                      self)

        self.X = list(map(lambda x: x["value"], data_in))
        self.Y_id = list(map(lambda x: x["id"], data_out))
        self.Y = [0, 0]

    def apply_filter(self):
        self.Y[0] = np.std(self.X)
        self.Y[1] = np.var(self.X)

    def post_data(self):
        vo = UpdateDatumOutput()
        vo.save_output(self.Y_name, self.Y, self.Y_id, self)
