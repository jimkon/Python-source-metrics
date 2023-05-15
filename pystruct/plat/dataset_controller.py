import pathlib

from pystruct.configs import PATH_ROOT
from pystruct.utils.logs import log_disk_ops
from pystruct.utils.python_utils import Singleton
from pystruct.utils.storage import DatasetsDirectory


def get_project_root_path():
    return pathlib.Path(PATH_ROOT)


class DatasetController:
    __initialized = None

    @classmethod
    def get_instance(cls):
        if not cls.__initialized:
            cls.__initialized = DatasetController()
            log_disk_ops(f"DatasetController: Instance is created.")
        return cls.__initialized

    def __init__(self):
        log_disk_ops(f"DatasetController: Initialising...")
        root = pathlib.Path(get_project_root_path())
        datasets_dir = root / 'datasets'

        self._datasets = DatasetsDirectory(datasets_dir)
        self._current_dataset = None

        self._reset_current_dataset()

    def _reset_current_dataset(self):
        datasets = self._datasets.get_datasets()
        if len(datasets) > 0:
            self._current_dataset = datasets[0]
        else:
            self._current_dataset = None
        log_disk_ops(f"DatasetController: Reset dataset {self._current_dataset}.")

    @property
    def all_datasets(self):
        return self._datasets.get_datasets()

    @property
    def current_dataset(self):
        if self._current_dataset is not None and not self._current_dataset.exists():
            log_disk_ops(f"DatasetController: Current dataset needs to reset dataset {self._current_dataset}: exists={self._current_dataset.exists()}.")
            self._reset_current_dataset()
        return self._current_dataset

    def new(self, dir_path=None, git_url=None, code_dir=None, branch='master'):
        if dir_path is not None:
            dataset_name = pathlib.Path(dir_path).name
            dataset = self._datasets.new_dataset(dataset_name)
            dataset.add_python_files_from_path(dir_path)
            self._current_dataset = dataset
            log_disk_ops(f"DatasetController: New dataset {self._current_dataset} from path.")
            return dataset
        elif git_url is not None:
            dataset_name = git_url.split('/')[-1].split('.')[0]
            dataset_name += f"{branch}" if branch != 'master' else ''
            dataset = self._datasets.new_dataset(dataset_name)
            dataset.add_python_files_from_git(git_url, code_dir=code_dir, branch=branch)
            self._current_dataset = dataset
            log_disk_ops(f"DatasetController: New dataset {self._current_dataset} from Git repo.")
        else:
            raise ValueError("At least one of dir_path or git_url parameters has to be populated.")

    def open(self, dataset_name):
        log_disk_ops(f"DatasetController: Attempting to open dataset {dataset_name}.")
        for dataset in self._datasets.get_datasets():
            if dataset.name == dataset_name:
                self._current_dataset = dataset
                log_disk_ops(f"DatasetController: Opened dataset {self._current_dataset}.")
                break
        else:
            log_disk_ops(f"DatasetController: Failed to open dataset {dataset_name} (Not found in {self._datasets.path}).")
        return self._current_dataset

    def delete(self, dataset_name):
        for dataset in self._datasets.get_datasets():
            if dataset.name == dataset_name:
                self._datasets.delete_dataset(dataset_name)
                log_disk_ops(f"DatasetController: Deleted dataset {dataset}.")
                self._reset_current_dataset()
        else:
            log_disk_ops(f"DatasetController: Failed to delete dataset {dataset_name} (Not found).")
        return self._current_dataset