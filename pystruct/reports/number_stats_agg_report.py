import matplotlib.pyplot as plt


class NumberStatsAggReport:#(StoreStatsImage):
    def __init__(self, df):
        self._df = df

        self._hist()

    def _hist(self):
        plt.figure()
        res_dict = plt.boxplot(self._df['value'], showmeans=True)
        print(res_dict)
        print(res_dict['fliers'])
        print(res_dict['fliers'][0].get_data())
        print(dir(res_dict['fliers'][0].get_xdata()))
        plt.yscale('log')
        plt.grid()
        plt.show()




if __name__ == '__main__':
    import pandas as pd
    NumberStatsAggReport(pd.read_csv(r"C:\Users\jim\PycharmProjects\Python-source-metrics\files\metrics\number_of_lines.csv"))

