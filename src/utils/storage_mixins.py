import json
from abc import ABC, abstractmethod

from src.configs import PATH_STORE_PYTHON_SOURCE_OBJECTS


class StoreData(ABC):
    @abstractmethod
    def data_to_store(self):
        pass

    @abstractmethod
    def path_to_store(self):
        pass

    @abstractmethod
    def save(self):
        pass


class StoreJSON(StoreData, ABC):
    def save(self):
        with open(self.path_to_store(), 'w') as fp:
            json.dump(self.data_to_store(), fp, indent=4)


class StorePythonSourceObj(StoreJSON):
    def path_to_store(self):
        return PATH_STORE_PYTHON_SOURCE_OBJECTS


class StoreCSV(StoreData, ABC):
    def save(self):
        path = self.path_to_store()
        df = self.data_to_store()
        df.to_csv(path, index=False)
