from factoryos_lib.base.inputs._input import Input


class ManualInput(Input):

    def __init__(self, x):
        self.x = x

    def get_data(self):
        return x