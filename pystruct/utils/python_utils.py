import pkgutil
from functools import lru_cache

@lru_cache
def all_python_builtin_packages():
    return sorted([mod.name for mod in list(pkgutil.iter_modules())])

@lru_cache
def is_python_builtin_package(pkg_name):
    return pkg_name in all_python_builtin_packages()
