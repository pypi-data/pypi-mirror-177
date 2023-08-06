"""

"""

from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport
from univariate.anomaly.detector import AnomalyDetector
from typing import Optional
import pyspark.sql.functions as F
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from numpy import ndarray


class IQROutlierDetector(AnomalyDetector):
    """

    """
    @staticmethod
    def detect(ts: DataFrame, data_col_name: str, q1: Optional[float], median: Optional[float], q3: Optional[float], ad_hoc: bool = False) -> AnalysisReport:
        """

        :param ts:
        :param data_col_name:
        :param q1:
        :param median:
        :param q3:
        :param ad_hoc: If ad_hoc is True, than Q1, median, Q3 will be estminated on ts by itself and q1, median, q3 parameter will be ignored. Default is False.
        :return:
        """
        # validate parameters #1: if ad_hoc is false, then q1, median, q3 must be passed
        if not ad_hoc and (q1 is None or median is None or q3 is None):
            raise TypeError("If ad_hoc is false(default), then q1, median, q3 must be passed")

        # ad-hoc statistics Q1, median, Q3
        if ad_hoc:
            stat_dict = ts.agg(
                F.expr(f"percentile_approx({data_col_name}, 0.5)").alias(
                    "median"
                ),
                F.expr(f"percentile_approx({data_col_name}, 0.25)").alias(
                    "Q1"
                ),
                F.expr(f"percentile_approx({data_col_name}, 0.75)").alias(
                    "Q3"
                )
            ).first().asDict()
            # shadow parameters
            q1 = stat_dict['Q1']
            median = stat_dict['median']
            q3 = stat_dict['Q3']

        # detect outliers (classify)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        outlier_detected_df = ts.withColumn("is_anomaly_by_iqr_method", F.when(((F.col(data_col_name) < lower_fence) | (F.col(data_col_name) > upper_fence)), True)
                                            .otherwise(False))  # checked 221107 youngmin-an null -> false, # todo: testcase..

        # boxplot
        x = ts.select(data_col_name).toPandas().values.reshape((-1,))
        boxplot = IQROutlierDetector.__build_boxplot(x, q1, median, q3, lower_fence, upper_fence)

        # build report
        report = AnalysisReport()
        report.parameters["ground_truth_ts"] = ts
        report.parameters["outliers"] = outlier_detected_df
        report.plots["boxplot"] = boxplot

        return report

    @staticmethod
    def __build_boxplot(x: ndarray, q1: float, median: float, q3: float, lower_fence: float, upper_fence: float) -> Figure:
        fig = go.Figure()
        # Use x instead of y argument for horizontal plot
        fig.add_trace(go.Box(x=[x], y=["data"], boxpoints="outliers"))  # todo: feature name to y

        fig.update_traces(q1=[q1], median=[median],
                          q3=[q3], lowerfence=[lower_fence],
                          upperfence=[upper_fence], orientation="h")
        fig.update_layout(title_text="IQR method of outlier detection")

        fig.add_vline(
            x=q1, annotation_position="bottom", annotation_text="Q1", line_width=1, line_dash="dash"
        )
        fig.add_vline(
            x=median, annotation_position="top", annotation_text="median", line_width=1, line_dash="dash"
        )
        fig.add_vline(
            x=q3, annotation_position="bottom", annotation_text="Q3", line_width=1, line_dash="dash"
        )
        fig.add_vline(
            x=lower_fence, annotation_position="left top", annotation_text="lower_fence", line_width=1, line_dash="dash"
        )
        fig.add_vline(
            x=upper_fence, annotation_position="right top", annotation_text="upper_fence", line_width=1,
            line_dash="dash"
        )
        return fig
