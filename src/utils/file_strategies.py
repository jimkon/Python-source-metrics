import abc
import os
import json
import pandas as pd

from src.configs import PATH_FILES_DIR
from src.utils.logs import log_yellow, log_green, log_red, log_pink


class AbstractFileStrategy(abc.ABC):
    def __init__(self, obj, file_ext, load_kwargs=None, save_kwargs=None):
        self._obj = obj
        self._root_dir = PATH_FILES_DIR+"/objs/"  # root_dir
        self._file_ext = file_ext
        self._cached_data = None
        self._load_kwargs, self._save_kwargs = load_kwargs, save_kwargs

    @property
    def filename(self):
        return f"{type(self._obj).__name__}.{self._file_ext}"

    @property
    def filepath(self):
        return os.path.join(self._root_dir, self.filename)

    def load(self):
        if self._cached_data:
            log_green(f"(CACHED) {self.__class__.__name__}: File {self.filepath} is cached in memory.")
            return self._cached_data
        elif os.path.exists(self.filepath):
            log_yellow(f"(LOADING) {self.__class__.__name__}: File {self.filepath} found in disk.")
            self._cached_data = self.load_from_file(self.filepath, **self._load_kwargs if self._load_kwargs else {})
            return self._cached_data
        else:
            log_pink(f"(BUILDING) {self.__class__.__name__}: File {self.filepath} not found.")
            return None

    def save(self, data):
        log_yellow(f"(STORING) {self.__class__.__name__}: File {self.filepath} is created.")
        self._cached_data = data
        self.save_to_file(data, self.filepath, **self._save_kwargs if self._save_kwargs else {})

    @abc.abstractmethod
    def load_from_file(self, filepath, **kwargs):
        pass

    @abc.abstractmethod
    def save_to_file(self, data, filepath, **kwargs):
        pass


class JsonFile(AbstractFileStrategy):
    def __init__(self, obj, load_kwargs=None, save_kwargs=None):
        super().__init__(obj, file_ext='json', load_kwargs=load_kwargs, save_kwargs=save_kwargs)

    def load_from_file(self, filepath, **kwargs):
        with open(filepath, 'r') as f:
            return json.load(f)

    def save_to_file(self, data, filepath, **kwargs):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)


class HTMLFile(AbstractFileStrategy):
    def __init__(self, obj, load_kwargs=None, save_kwargs=None):
        super().__init__(obj, file_ext='html', load_kwargs=load_kwargs, save_kwargs=save_kwargs)

    def load_from_file(self, filepath, **kwargs):
        with open(filepath, 'r') as f:
            return f.read()

    def save_to_file(self, data, filepath, **kwargs):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(data)


class DataframeFile(AbstractFileStrategy):
    def __init__(self, obj, load_kwargs=None, save_kwargs=None):
        super().__init__(obj, file_ext='csv', load_kwargs=load_kwargs, save_kwargs=save_kwargs)

    def load_from_file(self, filepath, **kwargs):
        return pd.read_csv(filepath, **kwargs)

    def save_to_file(self, data, filepath, **kwargs):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data.to_csv(filepath, **kwargs)
