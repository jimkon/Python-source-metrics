import abc

from src.utils.logs import log_red


class AbstractObject(abc.ABC):
    def __init__(self, file_strategy=None):
        self._file_strategy = file_strategy
        self._data = None

    def data(self):
        try:
            return self._prepare_data()
        except Exception as e:
            log_red(str(e))
            return f"{self.__class__.__name__}: {e}"

    def _prepare_data(self):
        if self._data:
            return self._data

        if self._file_strategy:
            self._data = self._file_strategy.load()

        if not self._data:
            self._data = self.build()

            if self._file_strategy and self._data:
                self._file_strategy.save(self._data)

        return self._data

    @abc.abstractmethod
    def build(self):
        return None

