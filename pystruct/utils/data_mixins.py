import abc


class JSONableMixin(abc.ABC):
    @abc.abstractmethod
    def to_json(self):
        pass


class HTMLMixin(abc.ABC):
    @abc.abstractmethod
    def to_html(self):
        pass