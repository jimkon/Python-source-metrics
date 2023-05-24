import abc
import sys
import inspect

from pystruct.objects.data_objects import AbstractObject
from pystruct.objects.imports_data_objects import *
from pystruct.objects.metric_tables import *
from pystruct.objects.metric_obj import *
from pystruct.objects.uml_graph_obj import *
from pystruct.objects.dependencies import *
from pystruct.objects.full_report import *
from pystruct.utils.python_utils import subclasses_of_class


def get_object_class_from_class_name(class_name):
    return getattr(sys.modules[__name__], class_name)


def get_all_object_classes():
    return subclasses_of_class(AbstractObject)


def get_all_concrete_object_classes():
    return [_cls for _cls in get_all_object_classes() if not inspect.isabstract(_cls)]
