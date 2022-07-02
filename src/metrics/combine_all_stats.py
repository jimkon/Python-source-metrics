import os

import pandas as pd

from src.configs import PATH_STORE_METRIC_RESULTS_DIR, PATH_STORE_JOINT_STAT_TABLE_CSV
from src.utils.storage_mixins import StoreCSV


class JointStatTable(StoreCSV):
    def __init__(self):
        self._all_dfs = {}
        self._final_df = None

        self.load_dfs()
        self.combine()

        self.save()
    
    def load_dfs(self):
        for file in os.listdir(PATH_STORE_METRIC_RESULTS_DIR):
            path = os.path.join(PATH_STORE_METRIC_RESULTS_DIR, file)
            self._all_dfs[file] = pd.read_csv(path).rename(columns={'value': file.replace('.csv', '')})

    def combine(self):
        # print(self._all_dfs)
        for name, df in self._all_dfs.items():
            if self._final_df is None:
                self._final_df = df
            else:
                self._final_df = self._final_df.merge(df, on='name', how='outer')

        print("results\n", self._final_df.shape)
        return self._final_df

    def path_to_store(self):
        return PATH_STORE_JOINT_STAT_TABLE_CSV

    def data_to_store(self):
        return self._final_df


