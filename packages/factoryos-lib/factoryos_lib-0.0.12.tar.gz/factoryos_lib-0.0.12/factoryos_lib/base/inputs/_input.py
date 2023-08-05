from abc import abstractmethod


class Input:

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass
