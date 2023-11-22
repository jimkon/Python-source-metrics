import abc

import pandas as pd
from json2html import json2html

from pystruct.utils import logs
from pystruct.utils.file_adapters import DataframeFile, HTMLFile, JsonFile, TextFile
from pystruct.utils.mixins import NameMixin, HTMLMixin
from pystruct.utils.string_utils import split_camel_case_string
from pystruct.utils.python_utils import Singleton


class AbstractObject(abc.ABC, Singleton, HTMLMixin, NameMixin):
    """
    AbstractObject manages the lifecycle of objects and the data they contain. It
    is responsible for building, caching, and saving the data, as well as loading
    and returning the data if it already exists. The main responsibility of this class
    is to provide an easy-to-extend interface and handle all data management operations
    efficiently and invisibly from the user.

    To use this class, you need to provide an implementation of the build method responsible
    for creating the data. If you provide a file adapter, AbstractObject will use it to store
    data after creation and to load it if there is such a file. To obtain the data, you only
    need to call the data method.

    HOW TO EXTEND:
    > If extended by another abstract class, for example another type of objects like JSON,
    it is encouraged to provide additional methods for obtaining data, for example a json()
    method for a JSON object to provide more specific information about what the data is and
    potentially any needed validation and logging.

    > If extended by another abstract class, for example another category of object like a
    multi-tab html element, where build instructions are extended, it is recommended to add
    an abstract `build_[object-category]` (for example `build_multitabs_page`) which will be
    called by `build`.

    If extended by a concrete class, for example an actual final object, just implement the
    corresponding `build*` method, and use the corresponding `data` method for the output.

    `build` calls `build_[type]`, 'data' calls `[data_type]`

    IMPLEMENTATIONS
    * abc.ABC: AbstractObject is an abstract class and cannot be used as it is. build method will
      have to be implemented when extended.
    * Singleton: Ensures that if two objects get instantiated at different times in the same
      execution, the data will be cached the second time, saving an extra loading operation.
    * HTMLMixin: Adds the to_html implementation to ensure that every implementation will have
      an HTML representation.
    * PrettifiedClassNameMixin: Provides class_name and prettified_class_name methods that
      make it easier to access the class name and a prettified version of it.
    """

    def __init__(self, file_adapter=None):
        self._file_adapter = file_adapter
        self._data = None

    def data(self):
        logs.log_obj_stage(f"{self.name()} data.")
        return self._prepare_data()

    def _prepare_data(self):
        if self._data is not None:  # if self._data breaks in Dataframes
            return self._data

        if self._file_adapter:
            self._data = self._file_adapter.load()

        if self._data is None:
            logs.log_general(f"{self.name()} object is building.")
            self._data = self.build()
            logs.log_general(f"{self.name()} object finished.")

            if self._file_adapter and self._data is not None:  # if self._data breaks in Dataframes
                self._file_adapter.save(self._data)

        return self._data

    def delete(self):
        self._data = None
        if self._file_adapter:
            self._file_adapter.delete_file()

    @abc.abstractmethod
    def build(self):
        return None

    def to_html(self):
        return f"{self.data()}"

    @classmethod
    def name(cls):
        return split_camel_case_string(cls.__name__)


class TextObjectABC(AbstractObject, abc.ABC):
    def __init__(self, file_ext):
        super().__init__(TextFile(self, file_ext=file_ext))

    def text(self):
        data = self.data()
        if not isinstance(data, str):
            raise TypeError(
                f"Wrong return type: build method of TextObject objects must return string. got {type(data)}")
        return data

    def to_html(self):
        return f"<h2>Text:</h2>{self.text()}"


class DataframeObjectABC(AbstractObject, abc.ABC):
    def __init__(self, read_csv_kwargs=None, to_csv_kwargs=None):  # TODO default values for DF objects
        read_csv_kwargs = {'index_col': None} if read_csv_kwargs is None else read_csv_kwargs
        to_csv_kwargs = {'index': False} if to_csv_kwargs is None else to_csv_kwargs
        super().__init__(DataframeFile(self,
                                       save_kwargs=to_csv_kwargs,
                                       load_kwargs=read_csv_kwargs))

    def dataframe(self):
        build_res = self.data()
        if not isinstance(build_res, pd.DataFrame) and not isinstance(build_res, pd.Series):
            raise TypeError(
                f"Wrong return type: build method of DataframeObject objects must return pandas.DataFrame or pandas.Series. got {type(build_res)}")
        return build_res

    def to_html(self):
        return self.dataframe().to_html()


class JSONObjectABC(AbstractObject, abc.ABC):
    def __init__(self):
        super().__init__(JsonFile(self))

    def json(self):
        build_res = self.data()
        if not isinstance(build_res, list) and not isinstance(build_res, dict):
            raise TypeError(
                f"Wrong return type: build method of JSONObject objects must return a JSON object (list of dicts or dict). got {type(build_res)}")
        return build_res

    def to_html(self):
        return json2html.convert(json=self.json())


class HTMLObjectABC(AbstractObject, abc.ABC):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def html(self):
        build_res = self.data()
        if not isinstance(build_res, str):
            raise TypeError(
                f"Wrong return type: build method of HTMLObject objects must return string. got {type(build_res)}")
        return build_res

    def to_html(self):
        return self.html()


class HTMLTableObjectABC(HTMLObjectABC, abc.ABC):
    def __init__(self):
        super().__init__()

    def title(self):
        return self.name()

    @abc.abstractmethod
    def build_dataframe(self):
        pass

    def build(self):
        build_res = self.build_dataframe()
        if not isinstance(build_res, pd.DataFrame):
            raise TypeError(
                f"Wrong return type: build_dataframe method of HTMLTableObject objects must return pandas.DataFrame. got {type(build_res)}")

        title = self.title() if self.title() else ''
        table_html = build_res.to_html(index=False, justify='center')
        return f"<h3>{title}</h3>{table_html}<br>"


class PlantUMLDocumentObjABC(JSONObjectABC, abc.ABC):
    @staticmethod
    def _validate_doc(doc):
        if not isinstance(doc, str):
            raise TypeError(f"PlantUML documents must be of type 'str'. got {type(doc)}")
        if not doc.startswith('@startuml'):
            raise TypeError(f"PlantUML documents must start with ''. got {doc[:min(len(doc), 9)]}")
        if not doc.strip().endswith('@enduml'):
            raise TypeError(f"PlantUML documents must end with ''. got {doc[-min(len(doc), 7):]}")

    def documents(self):
        docs = self.json()

        if isinstance(docs, str):
            docs = [docs]

        doc_values = docs.values() if isinstance(docs, dict) else docs
        for doc in doc_values:
            self._validate_doc(doc)

        return docs


# TODO Report objects
# TODO plantUMLDOc objects
# TODO HTMLTableObject objects can be DataframeObjects (to_html will do the job)
# TODO similar for umlgrapphs
# TODO organise objects methods so:
#   * abstract objects define a build_[object] method calling build or build_[object] for super class
#   * abstract objects define a valudate_[object] method
#   * make sure subclasses use the child concrete classes' methods

