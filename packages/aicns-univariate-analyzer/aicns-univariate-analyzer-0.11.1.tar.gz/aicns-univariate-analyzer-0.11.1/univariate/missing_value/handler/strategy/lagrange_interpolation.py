"""

"""

from univariate.missing_value.handler.strategy import MissingValueHandleStrategy, MissingValueHandleStrategyType
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from univariate.analyzer import AnalysisReport
from univariate.analyzer import DescriptiveStatAnalyzer
from typing import Optional
from pyspark.sql.window import Window
from scipy.interpolate import lagrange
import numpy as np
from pyspark.sql.types import ArrayType, StructType, StructField, LongType, FloatType


__all__ = ["LagrangeInterpolation"]


class LagrangeInterpolation(MissingValueHandleStrategy):
    """ """

    def handle(
            self, missed_ts: DataFrame, time_col_name: str, data_col_name, handled_col_name: str, k: Optional[int] = 3
    ) -> DataFrame:
        """
        todo: explain "pointwise lagrange"
        :param missed_ts:
        :param time_col_name:
        :param data_col_name:
        :param handled_col_name:
        :param k:
        :return:
        """
        # todo: documentation

        # todo: adjusted k, parameterized
        separated_df = missed_ts.withColumn('not_null_timestamp', F.when(F.col(data_col_name).isNotNull(), F.col(time_col_name)))
        not_null_df = missed_ts.filter(F.col(data_col_name).isNotNull())

        left_window = Window.orderBy(time_col_name).rowsBetween(-k + 1, Window.currentRow)
        right_window = Window.orderBy(time_col_name).rowsBetween(Window.currentRow, k - 1)
        left_stretched_df = not_null_df.select(
            F.col(time_col_name).alias('center'),
            F.collect_list(time_col_name).over(left_window).alias("left_timestamps"),
            F.collect_list(data_col_name).over(left_window).alias("left_values"),
        )
        right_stretched_df = not_null_df.select(
            F.col(time_col_name).alias('center'),
            F.collect_list(time_col_name).over(right_window).alias("right_timestamps"),
            F.collect_list(data_col_name).over(right_window).alias("right_values"),
        )

        # create relative references to the start value (last value not missing)
        w_start = Window.orderBy(time_col_name).rowsBetween(Window.unboundedPreceding, -1)
        w_end = Window.orderBy(time_col_name).rowsBetween(0, Window.unboundedFollowing)
        bounded_df = separated_df.withColumn('left_not_null_timestamp', F.when(F.col(data_col_name).isNull(),
                                                                               F.last('not_null_timestamp', True).over(
                                                                                   w_start))) \
            .withColumn('right_not_null_timestamp',
                        F.when(F.col(data_col_name).isNull(), F.first('not_null_timestamp', True).over(w_end)))
        joined_df = bounded_df.join(left_stretched_df,
                                    bounded_df['left_not_null_timestamp'] == left_stretched_df['center'], "left") \
            .join(right_stretched_df, bounded_df['right_not_null_timestamp'] == right_stretched_df['center'],
                  "left")

        select_k_nearest_udf = F.udf(select_k_nearest, ArrayType(StructType([
            StructField("timestamp", LongType()),
            StructField("value", FloatType()),
        ])))

        nearest_df = joined_df.withColumn("nearest", F.when(F.col(data_col_name).isNull(),
                                                            select_k_nearest_udf(F.col("event_time"),
                                                                                 F.col("left_values"),
                                                                                 F.col("left_timestamps"),
                                                                                 F.col("right_values"),
                                                                                 F.col("right_timestamps"),
                                                                                 F.lit(k))))

        interpolate_with_lagrange_udf = F.udf(interpolate_with_lagrange, FloatType())
        filled_df = nearest_df.withColumn(handled_col_name, F.when(F.col("input_data").isNull(),
                                                           interpolate_with_lagrange_udf(F.col("nearest"), F.col(
                                                               "event_time"))).otherwise(F.col("input_data"))).drop('not_null_timestamp', 'left_not_null_timestamp', 'right_not_null_timestamp', 'center', 'left_timestamps', 'left_values', 'right_timestamps', 'right_values', 'nearest').sort(time_col_name)
        return filled_df


def select_k_nearest(timestamp, left_values, left_timestamps, right_values, right_timestamps, k=10):
    cnt = 0
    left = 0
    right = 0
    left_size = len(left_values) if left_values is not None else 0
    right_size = len(right_values) if right_values is not None else 0

    nearest = []
    while cnt < k and (left < left_size or right < right_size):
        if right >= right_size:
            left = left + 1
            nearest.append([left_timestamps[left_size - left], left_values[left_size - left]])
        elif left >= left_size:
            nearest.append([right_timestamps[right], right_values[right]])
            right = right + 1
        elif (timestamp - left_timestamps[left_size - left - 1]) <= (right_timestamps[right] - timestamp):
            left = left + 1
            nearest.append([left_timestamps[left_size - left], left_values[left_size - left]])
        else:
            nearest.append([right_timestamps[right], right_values[right]])
            right = right + 1
        cnt = cnt + 1

    return nearest


def interpolate_with_lagrange(observations, timestamp):
    if observations is None:
        return None
    x = np.array([observation[0] for observation in observations])
    xm = np.mean(x)
    xscale = np.std(x)

    y = np.array([observation[1] for observation in observations])
    ym = np.mean(y)
    yscale = np.std(y)

    x = (x - xm) / xscale
    y = (y - ym) / yscale

    poly = lagrange(x, y)
    y_hat = poly((timestamp - xm) / xscale)

    estimate = (y_hat * yscale + ym).item()
    return estimate
