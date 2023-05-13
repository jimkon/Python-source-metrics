import pathlib

from pystruct.configs import PATH_ROOT
from pystruct.utils.logs import log_disk_ops
from pystruct.utils.python_utils import Singleton
from pystruct.utils.storage import DatasetsDirectory


def get_project_root_path():
    return pathlib.Path(PATH_ROOT)


class DatasetController(Singleton):
    def __init__(self):
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

    @property
    def current_dataset(self):
        return self._current_dataset

    def new(self, dir_path=None, git_url=None):
        if dir_path is not None:
            dataset_name = pathlib.Path(dir_path).name
            dataset = self._datasets.new_dataset(dataset_name)
            dataset.add_python_files_from_path(dir_path)
            self._current_dataset = dataset
            log_disk_ops(f"DatasetController: New dataset {self._current_dataset} from path.")
            return dataset
        elif git_url is not None:
            # TODO
            # source = request.form['giturl_input']
            # code_dir = source.split(':')[-1]
            # source = source.replace('/'+code_dir, '')
            # dataset_name = source.split('/')[-1].split('.')[0]
            # dataset = datasets.new_dataset(dataset_name)
            # dataset.add_python_files_from_git(source, code_dir=code_dir)
            raise NotImplementedError
        else:
            raise ValueError("At least one of dir_path or git_url parameters has to be populated.")

    def open(self, dataset_name):
        for dataset in self._datasets.get_datasets():
            if dataset.name == dataset_name:
                self._current_dataset = dataset
                log_disk_ops(f"DatasetController: Opened dataset {self._current_dataset}.")
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
