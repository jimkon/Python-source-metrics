import json
from abc import ABC, abstractmethod

import plantuml

from src.configs import *


def _write_text_to_file(filepath, data):
    with open(filepath, 'w') as fp:
        fp.write(data)


def _produce_uml_diagram_from_text_file(input_text_filepath):
    pl = plantuml.PlantUML('http://www.plantuml.com/plantuml/img/')
    pl.processes_file(input_text_filepath, directory='')


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


class StoreText(StoreData, ABC):
    def save(self):
        _write_text_to_file(self.path_to_store(), self.data_to_store())


class StoreUMLTextAsDiagramPNG(StoreText, ABC):
    def save(self):
        super().save()
        _produce_uml_diagram_from_text_file(self.path_to_store())


class StoreClassUML(StoreUMLTextAsDiagramPNG, ABC):
    def path_to_store(self):
        return PATH_STORE_UML_CLASS_TXT


class StoreClassRelationUML(StoreUMLTextAsDiagramPNG, ABC):
    def path_to_store(self):
        return PATH_STORE_UML_CLASS_RELATION_TXT


class StoreJSON(StoreData, ABC):
    def save(self):
        with open(self.path_to_store(), 'w') as fp:
            json.dump(self.data_to_store(), fp, indent=4)


class StorePythonSourceObj(StoreJSON, ABC):
    def path_to_store(self):
        return PATH_STORE_PYTHON_SOURCE_OBJECTS


class StoreCSV(StoreData, ABC):
    def save(self):
        path = self.path_to_store()
        df = self.data_to_store()
        df.to_csv(path, index=False)

