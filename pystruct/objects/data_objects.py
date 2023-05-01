import abc

import pandas as pd
from json2html import json2html

from pystruct.utils import logs
from pystruct.utils.file_adapters import DataframeFile, HTMLFile, JsonFile, TextFile
from pystruct.utils.mixins import PrettifiedClassNameMixin, HTMLMixin


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        else:
            logs.log_general(f"SingletonClass: Object {cls.__name__} is already initialized.")
        return cls.instance


class AbstractObject(abc.ABC, Singleton, HTMLMixin, PrettifiedClassNameMixin):
    """
    AbstractObject manages the lifecycle of objects and the data they contain. It
    is responsible for building, caching, and saving the data, as well as loading
    and returning the data if it already exists. The main responsibility of this class
    is to provide an easy-to-extend interface and handle all data management operations
    efficiently and invisibly from the user.

    To use this class, you need to provide an implementation of the build method responsible
    for creating the data. If you provide a file adapter, AbstractObject will use it to store
    data after creation and to load it if there is such a file. To obtain the data, you only
    need to call the data method. It is encouraged to provide additional methods for obtaining
    data, for example, a json() method for a JSON object to provide more specific information
    about what the data is and potentially any needed validation and logging.

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
        logs.log_obj_stage(f"{self.class_name()} data.")
        return self._prepare_data()

    def _prepare_data(self):
        if self._data is not None:  # if self._data breaks in Dataframes
            return self._data

        if self._file_adapter:
            self._data = self._file_adapter.load()

        if self._data is None:
            logs.log_general(f"{self.class_name()} object is building.")
            self._data = self.build()
            logs.log_general(f"{self.class_name()} object finished.")

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
        return f"to_html:{self.data()}"


class TextObject(AbstractObject, abc.ABC):
    def __init__(self, file_ext):
        super().__init__(TextFile(file_ext=file_ext))

    @property
    def text(self):
        build_res = self.build()
        if not isinstance(build_res, str):
            raise TypeError(f"Wrong return type: build method of TextObject objects must return string. got {type(build_res)}")
        return build_res

    def to_html(self):
        return f"<h2>Text:</h2>{self.text}"


class DataframeObject(AbstractObject, abc.ABC):
    def __init__(self, read_csv_kwargs=None, to_csv_kwargs=None):  # TODO default values for DF objects
        super().__init__(DataframeFile(self,
                                       save_kwargs=to_csv_kwargs,
                                       load_kwargs=read_csv_kwargs))

    @property
    def dataframe(self):
        build_res = self.build()
        if not isinstance(build_res, pd.DataFrame) and not isinstance(build_res, pd.Series):
            raise TypeError(f"Wrong return type: build method of DataframeObject objects must return pandas.DataFrame or pandas.Series. got {type(build_res)}")
        return build_res

    def to_html(self):
        return f"to_html:{self.dataframe.to_html()}"


class JSONObject(AbstractObject, abc.ABC):
    def __init__(self):
        super().__init__(JsonFile)

    @property
    def json(self):
        build_res = self.build()
        if not isinstance(build_res, list) and not isinstance(build_res, dict):
            raise TypeError(
                f"Wrong return type: build method of JSONObject objects must return a JSON object (list of dicts or dict). got {type(build_res)}")
        return build_res

    def to_html(self):
        return f"to_html:{json2html.convert(json = self.json)}"


class HTMLObject(AbstractObject, abc.ABC):
    def __init__(self):
        super().__init__(HTMLFile(self))

    @property
    def html(self):
        build_res = self.build()
        if not isinstance(build_res, str):
            raise TypeError(f"Wrong return type: build method of HTMLObject objects must return string. got {type(build_res)}")
        return build_res

    def to_html(self):
        return self.html


class HTMLTableObject(HTMLObject, abc.ABC):
    def __init__(self):
        super().__init__()

    def title(self):
        # def _space_before_upper_case(s):
        #     return ''.join([(f" {c}" if c.isupper() else c) for c in s])
        # return _space_before_upper_case(self.__class__.__name__)
        return self.prettified_class_name()

    @abc.abstractmethod
    def build_dataframe(self):
        pass

    def build(self):
        build_res = self.build_dataframe()
        if not isinstance(build_res, pd.DataFrame):
            raise TypeError(
                f"Wrong return type: build_dataframe method of HTMLTableObject objects must return pandas.DataFrame. got {type(build_res)}")

        # html_table_str = SimpleHTMLTable(build_res).html
        # return html_table_str
        title = self.title() if self.title() else ''
        table_html = build_res.to_html(index=False, justify='center')
        return f"<h3>{title}</h3>{table_html}<br>"


# class MultiPlantUMLDocumentsObject(JSONObject, abc.ABC):
    # def build
    #
    # @abc.abstractmethod
    # def build_documents(self):
    #     pass
    #
    # @property
    # def documents(self):


# class MultiTabHTMLObject(HTMLObject, abc.ABC):
#     @abc.abstractmethod
#     def build_tabs_dict(self):
#         pass
#
#     def build(self):
#         tabs_dict = self.build_tabs_dict()
#         html_builder = TabsHTML()
#         for title, obj_class in tabs_dict.items():
#             html_builder.add_tab(title, obj_class().data())
#         return html_builder.html()

# TODO store files in groups based on abstract type (dfs, jsons, htmls)
# TODO Report objects
# TODO plantUMLDOc objects
# TODO HTMLTableObject objects can be DataframeObjects (to_html will do the job)
# TODO similar for umlgrapphs
# TODO organise objects methods so:
#   * abstract objects define a build_[object] method calling build or build_[object] for super class
#   * abstract objects define a valudate_[object] method
#   * make sure subclasses use the child concrete classes' methods
