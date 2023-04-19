import abc


class JSONable(abc.ABC):
    @abc.abstractmethod
    def to_json(self):
        pass
