import abc
import os
import json
import pandas as pd

from src.configs import PATH_FILES_DIR
from src.utils.logs import log_yellow


class AbstractFileStrategy(abc.ABC):
    def __init__(self, obj, file_ext):
        self._obj = obj
        self._root_dir = PATH_FILES_DIR+"/objs/"  # root_dir
        self._file_ext = file_ext
        self._cached_data = None

    @property
    def filename(self):
        return f"{type(self._obj).__name__}.{self._file_ext}"

    @property
    def filepath(self):
        return os.path.join(self._root_dir, self.filename)

    def load(self):
        if self._cached_data:
            log_yellow(f"{self.__class__.__name__}: File {self.filepath} is cached in memory.")
            return self._cached_data
        elif os.path.exists(self.filepath):
            log_yellow(f"{self.__class__.__name__}: File {self.filepath} found in disk.")
            self._cached_data = self.load_from_file(self.filepath)
            return self._cached_data
        else:
            log_yellow(f"{self.__class__.__name__}: File {self.filepath} not found.")
            return None

    def save(self, data):
        log_yellow(f"{self.__class__.__name__}: File {self.filepath} is created.")
        self._cached_data = data
        self.save_to_file(data, self.filepath)

    @abc.abstractmethod
    def load_from_file(self, filepath, *args, **kwargs):
        pass

    @abc.abstractmethod
    def save_to_file(self, data, filepath, *args, **kwargs):
        pass


class JsonFile(AbstractFileStrategy):
    def __init__(self, obj):
        super().__init__(obj, file_ext='json')

    def load_from_file(self, filepath, *args, **kwargs):
        with open(filepath, 'r') as f:
            return json.load(f)

    def save_to_file(self, data, filepath, *args, **kwargs):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)


class HTMLFile(AbstractFileStrategy):
    def __init__(self, obj):
        super().__init__(obj, file_ext='html')

    def load_from_file(self, filepath, *args, **kwargs):
        with open(filepath, 'r') as f:
            return f.read()

    def save_to_file(self, data, filepath, *args, **kwargs):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(data)


class DataframeFile(AbstractFileStrategy):
    def __init__(self, obj):
        super().__init__(obj, file_ext='csv')

    def load_from_file(self, filepath, *args, **kwargs):
        return pd.read_csv(filepath, **kwargs)

    def save_to_file(self, data, filepath, *args, **kwargs):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data.to_csv(filepath, **kwargs)
