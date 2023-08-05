from abc import abstractmethod


class Output:
    @abstractmethod
    def save_output(self, *args, **kwargs):
        pass
