import json
import os.path
from abc import ABC, abstractmethod

from pystruct.configs import *
from pystruct.utils.io_files import write_text_to_file


class StoreData(ABC):
    @abstractmethod
    def data_to_store(self):
        pass

    def path_to_store(self):
        return join(self.path(), self.filename())

    @abstractmethod
    def path(self):
        pass

    @abstractmethod
    def filename(self):
        pass

    @abstractmethod
    def save(self):
        pass

    def delete(self):
        if os.path.exists(self.path_to_store()):
            os.remove(self.path_to_store())
        else:
            raise ValueError(f"WARNING: The file ({self.path_to_store()}) does not exist")


class StoreText(StoreData, ABC):
    def save(self):
        write_text_to_file(self.path_to_store(), self.data_to_store())


class StoreUMLTextAsDiagramPNG(StoreText, ABC):
    def save(self):
        raise NotImplemented
        # super().save()
        # print("WARNING _produce_uml_diagram_from_text_file(self.path_to_store()) ")
        # _produce_uml_diagram_from_text_file(self.path_to_store())


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
        return PATH_STORE_PYTHON_SOURCE_OBJECTS_JSON


class StoreCSV(StoreData, ABC):
    def save(self):
        path = self.path_to_store()
        df = self.data_to_store()
        df.to_csv(path, index=False)


class StoreStatsImage(StoreData, ABC):# TODO to implement
    pass


class StoreHTMLBuilds(StoreText):
    def __init__(self, filename, html_builder):
        self._filename = filename
        self._html_builder = html_builder

    def filename(self):
        return self._filename

    def data_to_store(self):
        return self._html_builder.html

    def path(self):
        return PATH_STORE_HTML_BUILDS_DIR


class StoreHTMLImageBuilds(StoreHTMLBuilds):
    def __init__(self, html_image_builder):
        super(StoreHTMLBuilds, self).__init__(html_image_builder.image_path, html_image_builder)


class StoreReports(StoreText, ABC):
    def __init__(self, report_file):
        self._report_file = report_file

    def path_to_store(self):
        return os.path.join(PATH_STORE_REPORTS_DIR, self._report_file)

