import abc

from utils.string_utils import split_camel_case_string


class JSONableMixin(abc.ABC):
    @abc.abstractmethod
    def to_json(self):
        pass


class HTMLMixin:
    def to_html(self):
        return f"<h2>to_html:'{self}'</h2>"


class NameMixin:
    @classmethod
    def name(cls):
        return cls.__name__
