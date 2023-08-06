"""

"""


from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType, StructField, LongType
from univariate.sampling.utils import freq_to_period_map
from datetime import datetime, timedelta
from typing import Optional


def construct_range_df(sampling_period: int, first_start: int, last_start: int) -> DataFrame:
    """
    Construct spark dataframe that contains each row {"start", "end"} cols representing [start, end) ranges
    Note: Each range is half-closed interval
    :param time_col_name:
    :param sampling_period:
    :param first_start:
    :param last_start:
    :return:
    """
    start_series = range(first_start, last_start + 1, sampling_period)
    end_series = range(first_start + sampling_period, last_start + sampling_period + 1, sampling_period)

    schema = StructType([
        StructField("start", LongType(), False),
        StructField("end", LongType(), False)
    ])
    range_df = SparkSession.getActiveSession().createDataFrame(data=[start_series, end_series], schema=schema)

    return range_df


def find_start_timestamp_by_freq(observed_at: int, sampling_period: int) -> int:
    """
    Find start timestamp of range which observed_at arguments are belonged
    :param observed_at:
    :param sampling_period:
    :return:
    """
    start_timestamp: int
    try:
        freq = list(freq_to_period_map.keys())[list(freq_to_period_map.values()).index(sampling_period)]
    except Exception as e:
        raise ValueError(f"can't convert sampling period {sampling_period} to freq")
    observed_date = datetime.fromtimestamp(observed_at / 1000)
    if freq == 'A':  # yearly
        start_timestamp = datetime(year=observed_date.year, month=1, day=1).timestamp() * 1000
    elif freq == 'Q':
        start_timestamp = datetime(year=observed_date.year,
                                   month=3 * ((observed_date.month - 1) // 3) + 1,
                                   day=1).timestamp() * 1000
    elif freq == 'M':
        start_timestamp = datetime(year=observed_date.year, month=observed_date.month, day=1).timestamp() * 1000
    elif freq == 'W':
        start_of_week = observed_date - timedelta(days=observed_date.weekday())
        start_timestamp = datetime(year=start_of_week.year, month=start_of_week.month, day=start_of_week.day).timestamp() * 1000
    elif freq == 'D':
        start_timestamp = datetime(year=observed_date.year, month=observed_date.month, day=observed_date.day).timestamp() * 1000
    elif freq == 'H':
        start_timestamp = datetime(year=observed_date.year, month=observed_date.month, day=observed_date.day, hour=observed_date.hour).timestamp() * 1000
    else:
        raise ValueError(f"freq {freq} has no converting rule")
    return start_timestamp
