from ValiotWorker.Logging import LogLevel

from factoryos_lib.base.inputs import VariableInput
from factoryos_lib.base.outputs import UpdateDatumOutput
from factoryos_lib.filters._filter import Filter, NotEnoughDataException
import numpy as np


class MovingAverage(Filter):
    """ MovingAverage
           Overview:
           - Moving average filter
            Description:
            - This job obtain input data from a variable, apply the moving average
            filter and store the filtered values on another variable

    """

    def set_inputs(self, kwargs):
        variable = kwargs["input"]["variable"]
        window = kwargs["input"]["window"]
        block_size = kwargs["input"]["block_size"]
        restart = kwargs["input"]["restart"]
        self.X_name = variable
        self.window = window
        self.block_size = block_size
        self.restart = restart
        if restart:
            self.update_context(None)

    def get_data(self):

        # Check if variable exists
        self.check_filter_variable()
        # Check if input variable have the same size as the output variable
        # If not, add more data to output to match the input
        self.check_data_count()

        var_input = VariableInput()

        data_in = var_input.get_data(self.X_name,
                                     self.block_size if self.restart else self.block_size + self.window - 1,
                                     self.restart,
                                     self.context["id_in"] if not self.restart else None,
                                     self)
        data_out = var_input.get_data(self.Y_name,
                                      self.block_size,
                                      self.restart,
                                      self.context["id_out"] if not self.restart else None,
                                      self)

        if data_out is None or len(data_out) <= self.window:
            raise NotEnoughDataException()

        self.X = list(map(lambda x: x["value"], data_in))
        self.Y_id = list(map(lambda x: x["id"], data_out))
        self.update_context({"id_in": data_in[-self.window]["id"],
                             "id_out": self.Y_id[-1]})
        self.log_callback(LogLevel.DEBUG,
                          "Updated context to {0} and {1}".format(data_in[-self.window]["id"], data_out[-1]["id"]))

    def apply_filter(self):
        self.Y = np.convolve(self.X, np.ones(self.window), 'valid') / self.window

    def post_data(self):
        if self.restart:
            list_start = [self.X[0]]
            for i in range(1, self.window - 1):
                list_start.append(np.average(self.X[0:i]))
            self.Y = [*list_start, *self.Y]

        vo = UpdateDatumOutput()
        self.log_callback(LogLevel.DEBUG, "Updating {0} and {1} datums for filter".format(len(self.Y), len(self.Y_id)))
        vo.save_output(self.Y_name, self.Y, self.Y_id, self)
        self.log_callback(LogLevel.DEBUG, f"Completed the update of  {len(self.Y)} datums for filter {self.Y_name}")
