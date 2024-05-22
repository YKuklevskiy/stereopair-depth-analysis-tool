from collections import OrderedDict


def get_universal_analysis_filepath(filename):
    return f"Analytics/Results/{filename}"


def get_universal_analysis_table_filepath(filename):
    return f"Analytics/Tables/{filename}"



class Metric:
    def __init__(self, name: str, value):
        self.name = name
        self.value = value
        self.configure_spacing(len(name))

    def configure_spacing(self, max_len):
        self.characters_before_value = max_len + 4

    def print(self):
        prompt = f"{self.name}:".ljust(self.characters_before_value)
        print(f"{prompt}{self.value}")

    def add_to_string(self, string):
        return string + f"{self.value} "

    def add_to_string_with_name(self, string):
        return string + f"{self.name.strip()}, {self.value}\n"


class AnalysisResults:
    def __init__(self):
        self.metrics_dict = OrderedDict()

    def setup(self, min_diff, max_diff, mean_diff, mean_abs_diff,
              median_diff, median_abs_diff, std_diff, std_abs_diff_MAD,
              calc_far_ratio, real_far_ratio, false_negative_ratio, false_positive_ratio):
        self.metrics_dict["min_diff"] =             Metric("Минимальная разница", min_diff)
        self.metrics_dict["max_diff"] =             Metric("Максимальная разница", max_diff)
        self.metrics_dict["mean_diff"] =            Metric("Средняя разница", mean_diff)
        self.metrics_dict["mean_abs_diff"] =        Metric("Средняя абсолютная разница", mean_abs_diff)
        self.metrics_dict["median_diff"] =          Metric("Медиана разницы рассчитанной и реальной глубины", median_diff)
        self.metrics_dict["median_abs_diff"] =      Metric("Медиана абсолютной разницы", median_abs_diff)
        self.metrics_dict["std_diff"] =             Metric("Cреднеквадратичное отклонение", std_diff)
        self.metrics_dict["std_abs_diff_MAD"] =     Metric("Cреднее абсолютное отклонение MAD", std_abs_diff_MAD)
        self.metrics_dict["calc_far_ratio"] =       Metric("Процент дальних пикселей на SGBM", calc_far_ratio)
        self.metrics_dict["real_far_ratio"] =       Metric("Процент дальних пикселей из движка", real_far_ratio)
        self.metrics_dict["false_negative_ratio"] = Metric("Процент ложно-отрицательных дальних пикселей", false_negative_ratio)
        self.metrics_dict["false_positive_ratio"] = Metric("Процент ложно-положительных дальних пикселей", false_positive_ratio)

        self.configure_all_spacing()

    def configure_all_spacing(self):
        max_len = max([len(metric.name) for metric in self.metrics_dict.values()])
        for metric in self.metrics_dict.values():
            metric.configure_spacing(max_len)

    def print_metrics(self):
        for metric in self.metrics_dict.values():
            metric.print()

    def save_analysis_results(self, filename):
        filepath = get_universal_analysis_filepath(filename)

        resulting_contents = ""
        for metric in self.metrics_dict.values():
            resulting_contents = metric.add_to_string(resulting_contents)

        with open(filepath, "w") as f:
            f.write(resulting_contents)

    def save_analysis_results_as_table(self, filename):
        filepath = get_universal_analysis_table_filepath(filename)

        resulting_contents = ""
        for metric in self.metrics_dict.values():
            resulting_contents = metric.add_to_string_with_name(resulting_contents)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(resulting_contents)

    def read_analysis_results(self, filename):
        filepath = get_universal_analysis_filepath(filename)

        with open(filepath, "r") as f:
            self.setup(*map(float, f.readline().split()))
