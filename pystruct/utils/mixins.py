import abc


class JSONableMixin(abc.ABC):
    @abc.abstractmethod
    def to_json(self):
        pass


class HTMLMixin:
    def to_html(self):
        raise NotImplementedError


class NameMixin:
    @classmethod
    def name(cls):
        return cls.__name__
