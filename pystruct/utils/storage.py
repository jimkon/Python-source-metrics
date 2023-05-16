import pathlib
from io import StringIO
import shutil

from git import Repo

from pystruct.utils.python_utils import MultiSingleton
from pystruct.utils.logs import log_disk_ops


class Directory:
    def __init__(self, path):
        self._path = pathlib.Path(path) if isinstance(path, str) else path
        self._path.mkdir(exist_ok=True)

    @property
    def path(self):
        return self._path

    def __repr__(self):
        return f"{self.__class__.__name__} path: {self._path}"

    def exists(self):
        return self.path.exists()


class Dataset(Directory, MultiSingleton):
    def __init__(self, dataset_path):
        super().__init__(dataset_path)
        self._dataset_name = self.path.stem

        self._project_dir = None
        self._git_dir = None
        self._code_dir = None
        self._init_code_dir()

        self._objs_dir = pathlib.Path(self.path, 'objs')

    def _init_code_dir(self):
        self._project_dir = pathlib.Path(self.path, 'project')
        self._project_dir.mkdir(exist_ok=True)

        int_dir_names = {path.name for path in  self._project_dir.iterdir() if path.is_dir()}

        if 'git' in int_dir_names:
            int_dir_names.remove('git')
            self._git_dir = self._project_dir / 'git'
            log_disk_ops(f"Dataset: Found git directory {self._git_dir}")

        if len(int_dir_names) > 0:
            self._code_dir = self._project_dir / int_dir_names.pop()
            log_disk_ops(f"Dataset: Found code directory {self._code_dir}")

    @property
    def name(self):
        return self._dataset_name

    @property
    def code_directory(self):
        return self._code_dir

    @property
    def git_directory(self):
        return self._git_dir

    @property
    def objects_directory(self):
        return self._objs_dir

    def add_python_files_from_path(self, python_source):
        log_disk_ops(f"Dataset: Fetching python files from {str(python_source)} ...")

        python_source_path = pathlib.Path(python_source)

        self._code_dir = pathlib.Path(self._project_dir, python_source_path.name)
        if self._code_dir.exists():
            shutil.rmtree(self._code_dir)
        self._code_dir.mkdir()

        files_to_fetch = list(python_source_path.rglob('*.py'))
        for from_filepath in files_to_fetch:
            self._copy_code_file(from_filepath, python_source_path)
        log_disk_ops(f"Dataset: Fetched {len(files_to_fetch)} python files from {str(python_source)} to {str(self._code_dir)}")

    def _copy_code_file(self, from_filepath, source_filepath):
        relative_filepath = from_filepath.relative_to(source_filepath)
        to_filepath = self.code_directory / relative_filepath
        for parent_path in list(to_filepath.parents)[::-1]:
            parent_path.mkdir(exist_ok=True)
        to_filepath.write_text(from_filepath.read_text())
        log_disk_ops(f"Dataset: Copied from {str(from_filepath)} to {str(to_filepath)}")

    def add_python_files_from_git(self, git_url, code_dir=None, branch='master'):
        download_dir = self._project_dir / 'git'
        if download_dir.exists():
            shutil.rmtree(download_dir)

        if code_dir is None:
            code_dir = self._find_code_dir(git_url)

        log_disk_ops(f"Dataset: Accessing git repository {str(download_dir)}...")
        Repo.clone_from(git_url, download_dir, branch=branch)
        log_disk_ops(f"Dataset: Downloaded git repository {str(download_dir)}.")
        self.add_python_files_from_path(download_dir / code_dir)

    def _find_code_dir(self, dir_path):
        init_files = dir_path.rglob('*/__init__.py')
        if len(init_files) > 0:
            code_dir = init_files[0].parent
            log_disk_ops(f"Dataset: Discovered python package {code_dir}")
            return code_dir
        else:
            python_files = dir_path.rglob('*.py')
            if len(python_files) > 0:
                code_dir = python_files[0].parent
                log_disk_ops(f"Dataset: Discovered directory containing python files {code_dir}")
                return code_dir
            else:
                raise FileNotFoundError(f"Dataset: No python files found in {dir_path}")


class FileDirectory(Directory):  # TODO redundant. maybe delete
    def __init__(self, obj_dir):
        super().__init__(obj_dir)
        self.path.mkdir(exist_ok=True)

    def read_file(self, _dir, file):
        file_path = self.path / _dir / file
        return StringIO(file_path.read_text())

    def write_file(self, content, _dir, file):
        file_path = self.path / _dir / file
        file_path.write_text(content)

    def delete_file(self, _dir, file):
        file_path = self.path / _dir / file
        file_path.unlink()


class DatasetsDirectory(Directory):
    def __init__(self, dir_path):
        super().__init__(dir_path)
        log_disk_ops(f"DatasetsDirectory: Datasets directory {str(self.path)}")

    def get_datasets(self):
        all_dataset_paths = [path for path in self.path.iterdir() if path.is_dir()]
        datasets = [Dataset(path) for path in all_dataset_paths]
        return datasets

    def new_dataset(self, dataset_name):
        dataset_path = self.path / dataset_name

        if dataset_path.exists():
            self.delete_dataset(dataset_name)

        dataset = Dataset(dataset_path)
        return dataset

    def delete_dataset(self, dataset_name):
        dataset_path = self.path / dataset_name
        log_disk_ops(f"DatasetsDirectory: Deleting {str(dataset_path)}")
        shutil.rmtree(dataset_path)





