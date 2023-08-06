"""

"""

from univariate.sampling.strategy import SamplingStrategy
from univariate.sampling.utils import find_start_timestamp_by_freq, construct_range_array
from pyspark.sql import DataFrame, SparkSession
from typing import Optional, List, Tuple
from pyspark.sql import functions as F
from pyspark.sql.types import LongType, IntegerType


class MeanDownsampling(SamplingStrategy):
    """

    """
    @staticmethod
    def sample(ts: DataFrame, time_col_name: str, data_col_name: str, period: int, sampling_period: int, by_freq: bool, count_flag_cols: List[str], display_point: Optional[str] = "first") -> DataFrame:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :param period:
        :param sampling_period:
        :param by_freq:
        :param count_flag_cols:
        :param display_point:
        :return:
        """
        logger = SparkSession.getActiveSession()._jvm.org.apache.log4j.LogManager.getLogger(
            __name__
        )
        # todo: validate display_point parameter
        # first range's start timestamp
        if by_freq:
            first_timestamp = ts.sort(time_col_name).first().asDict()[time_col_name]
            first_start = find_start_timestamp_by_freq(first_timestamp, sampling_period)
            last_timestamp = ts.sort(time_col_name).tail(1)[0].asDict()[time_col_name]
            last_start = find_start_timestamp_by_freq(last_timestamp, sampling_period)

            start_series, end_series = construct_range_array(sampling_period, first_start, last_start, True)
            logger.info(f"start_series {start_series}")
            logger.info(f"end_series {end_series}")
            # partition col by intervals
            partitioned_df = ts.withColumn("_range_start", partitionize_udf(start_series, end_series)(F.col(time_col_name)))

        # aggregation
        agg_cols = [F.mean(data_col_name).alias(data_col_name),  F.count("*").alias("count")]
        select_cols = ["_range_start", data_col_name, "count"]
        cnt_cond = lambda cond: F.sum(F.when(cond, 1).otherwise(0))
        if len(count_flag_cols) > 0:
            agg_cols.extend([cnt_cond(F.col(col)).alias(col + "_count") for col in count_flag_cols])
            select_cols.extend([col + "_count" for col in count_flag_cols])


        agg_df = partitioned_df.groupBy("_range_start").agg(*agg_cols).select(*select_cols)

        # display_name
        if display_point == "first":
            sampled_df = agg_df.withColumnRenamed("_range_start", time_col_name)
        elif display_point == "middle":
            sampled_df = agg_df.withColumn(time_col_name, F.col("_range_start") + F.lit(sampling_period // 2)).drop("_range_start")
        elif display_point == "last":
            sampled_df = agg_df.withColumn(time_col_name, F.col("_range_start") + F.lit(sampling_period)).drop("_range_start")

        # sort
        return sampled_df.sort(time_col_name)

'''
def calc_range_start(timestamp: int, first_start: int, sampling_period: int) -> int:
    """

    :param timestamp:
    :param first_start:
    :param sampling_period:
    :return:
    """
    return ((timestamp - first_start) // sampling_period) * sampling_period + first_start
'''


def partitionize(timestamp: int, start_series: List[int], end_series: List[int]) -> int:
    """

    :param timestamp:
    :param start_series:
    :param end_series:
    :return:
    """
    for i in range(len(start_series)):
        if start_series[i] <= timestamp and end_series[i] > timestamp:
            return start_series[i]


def partitionize_udf(start_series: List[int], end_series: List[int]):
    return F.udf(lambda t: partitionize(t, start_series, end_series))
