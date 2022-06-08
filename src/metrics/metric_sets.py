from src.metrics.code_obj_metrics import NumberOfCodeLinesMetric, NumberOfArgsInFunctionsMetric

ALL_METRICS = [
    NumberOfCodeLinesMetric(),
    NumberOfArgsInFunctionsMetric()
]

