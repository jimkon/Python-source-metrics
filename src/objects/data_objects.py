import abc


class AbstractObject(abc.ABC):
    def __init__(self, file_strategy=None):
        self._file_strategy = file_strategy
        self._data = None

    def data(self):
        if self._data:
            return self._data

        if self._file_strategy:
            self._data = self._file_strategy.load()

        if not self._data:
            self._data = self.build()

            if self._file_strategy and self._data:
                self._file_strategy.save()

        return self._data

    @abc.abstractmethod
    def build(self):
        return None

