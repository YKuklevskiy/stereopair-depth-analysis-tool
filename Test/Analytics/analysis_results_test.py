from analysis_results import AnalysisResults


class AnalysisResultsTestMock(AnalysisResults):
    def __init__(self):
        AnalysisResults.__init__(self)
        self.test_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def test(self):
        self.setup(*self.test_values)
        self.save_analysis_results("test.txt")
        self.read_analysis_results("test.txt")
        for metric_id in self.metrics_dict:
            print(f"{metric_id}: {self.metrics_dict[metric_id].value}")

        print("-" * 50)
        self.print_metrics()


if __name__ == "__main__":
    AnalysisResultsTestMock().test()