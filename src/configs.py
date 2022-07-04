from os.path import join

PYTHON_FILE_EXTENSION = '.py'

PATH_ROOT = r"C:\Users\jim\PycharmProjects\Python-source-metrics"

PATH_FILES_DIR = join(PATH_ROOT, "files")

PATH_STORE_JOINT_STAT_TABLE_CSV = join(PATH_FILES_DIR, "joint_stats.csv")

PATH_STORE_PYTHON_OBJECTS_DIR = join(PATH_FILES_DIR, "python_objects")

PATH_STORE_PYTHON_SOURCE_OBJECTS_JSON = join(PATH_STORE_PYTHON_OBJECTS_DIR, "python_source_object.json")

PATH_STORE_METRIC_RESULTS_DIR = join(PATH_FILES_DIR, "metrics")

PATH_STORE_UML_DIR = join(PATH_FILES_DIR, "uml")

PATH_STORE_UML_CLASS_TXT = join(PATH_STORE_UML_DIR, "class_uml.txt")
PATH_STORE_UML_CLASS_RELATION_TXT = join(PATH_STORE_UML_DIR, "class_rel_uml.txt")
PATH_STORE_IMPORTS_DICT = join(PATH_STORE_UML_DIR, "module_imports.csv")

PATH_RES = join(PATH_ROOT, "res")
PATH_RES_HTML = join(PATH_RES, "html_templates")
PATH_RES_HTML_TABLE = join(PATH_RES_HTML, "table.html")
PATH_RES_HTML_TABS = join(PATH_RES_HTML, "tabs.html")
PATH_RES_HTML_IMAGE = join(PATH_RES_HTML, "image.html")

VERBOSITY = 2
