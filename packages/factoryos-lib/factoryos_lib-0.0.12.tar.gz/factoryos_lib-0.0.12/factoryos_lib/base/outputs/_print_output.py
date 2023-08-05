from factoryos_lib.base.outputs._output import Output


class PrintOutput(Output):
    def save_output(self, y):
        print(y)