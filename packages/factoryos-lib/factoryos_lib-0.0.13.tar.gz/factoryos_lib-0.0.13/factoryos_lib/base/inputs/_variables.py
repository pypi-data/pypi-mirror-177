from factoryos_lib.base.inputs import VariableInput


class VariablesInput(Input):

    def get_data(self, variables, log):
        vi = VariableInput()

        return [vi.get_data(v.variables, v.size, v.window, v.restart, v.id_in, log)
                for v in variables]
