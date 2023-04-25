import re
from urllib.error import URLError
from urllib.request import urlopen
import pkgutil
from functools import lru_cache
import logging


@lru_cache
def all_python_builtin_packages():
    return sorted([mod.name for mod in list(pkgutil.iter_modules())])


@lru_cache
def is_python_builtin_package(pkg_name):
    """
    If the machine is connected to the internet it will try to fetch the python built-in
    packages from the original Python docs site. Otherwise, it will fetch them from pkgutil
    library. The difference is that the pkgutil will fetch all the python packages visible to the app
    including the ones that were pip-installed. So for example is_python_builtin_package('pandas') may
    return True if it is installed locally.
    :param pkg_name:
    :return: bool:
    """
    try:
        pkgs = fetch_python_builtin_packages_from_python_docs()
    except URLError:
        logging.getLogger('tech').warning(f"WARNING: Fetching built-in Python packages failed. You might find discrepancies between built-in and other python libraries.")
        pkgs = all_python_builtin_packages()
    return pkg_name in pkgs


@lru_cache
def fetch_python_builtin_packages_from_python_docs():
    url = "https://docs.python.org/3/py-modindex.html"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    packages = [pkg.split(r'library/')[1].split(r'.html')[0] for pkg in re.findall('<a href=\"library/\w+\.html', html)]
    return packages


def subclasses_of_class(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in subclasses_of_class(c)])