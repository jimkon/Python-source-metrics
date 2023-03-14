
class ExtractMetrics:
    def __init__(self, python_source_obj, metrics_set):
        self._python = python_source_obj
        self._metrics = metrics_set

    def calculate_metrics(self):
        result_dict = {}
        for metric in self._metrics:
            data = self._python.calculate_metric(metric)
            result_dict[metric.name] = data
        print(result_dict)
