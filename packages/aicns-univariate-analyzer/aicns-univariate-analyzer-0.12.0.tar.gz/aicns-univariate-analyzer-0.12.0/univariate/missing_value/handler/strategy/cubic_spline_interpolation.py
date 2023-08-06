"""

"""

from univariate.missing_value.handler.strategy import MissingValueHandleStrategy, MissingValueHandleStrategyType
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from univariate.analyzer import AnalysisReport
from univariate.analyzer import DescriptiveStatAnalyzer
from typing import Optional
from pyspark.sql.window import Window
from scipy.interpolate import CubicSpline
import numpy as np
from pyspark.sql.types import FloatType
from typing import Tuple

__all__ = ["CubicSplineInterpolation"]


class CubicSplineInterpolation(MissingValueHandleStrategy):
    """ """

    def handle(
            self, missed_ts: DataFrame, time_col_name: str, data_col_name, handled_col_name: str
    ) -> DataFrame:
        """

        :param missed_ts:
        :param time_col_name:
        :param data_col_name:
        :param handled_col_name:
        :return:
        """
        # todo: documentation
        xm, xscale, ym, yscale, poly = model_spline_interpolator(missed_ts, time_col_name, data_col_name)
        interpolate_cubic_spline_udf = F.udf(lambda x: (poly((x - xm) / xscale) * yscale + ym).item(), FloatType())
        filled_spline_df = missed_ts.withColumn(handled_col_name, F.when(F.col(data_col_name).isNull(),
            interpolate_cubic_spline_udf(F.col(time_col_name))).otherwise(F.col(data_col_name)))
        return filled_spline_df


def model_spline_interpolator(ts: DataFrame, time_col_name: str, data_col_name: str) -> Tuple[np.float64, np.float64, np.float64, np.float64, CubicSpline]:
    not_null_pd = ts.filter(F.col(data_col_name).isNotNull()).sort(time_col_name).toPandas()
    x = not_null_pd[time_col_name].values
    y = not_null_pd[data_col_name].values

    xm = np.mean(x)
    xscale = np.std(x)

    ym = np.mean(y)
    yscale = np.std(y)

    x = (x - xm) / xscale
    y = (y - ym) / yscale

    poly = CubicSpline(x, y)
    return xm, xscale, ym, yscale, poly
