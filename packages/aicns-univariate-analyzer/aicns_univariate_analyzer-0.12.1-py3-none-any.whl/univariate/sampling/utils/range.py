"""

"""
import pendulum
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType
from univariate.sampling.utils import freq_to_period_map
from datetime import datetime, timedelta
from typing import List, Tuple
from pendulum import period


def construct_range_array(sampling_period: int, first_start: int, last_start: int, by_freq: bool) -> Tuple[List[int], List[int]]:
    """
    Construct range tuple that contains each ("start", "end") array representing (2, n) shape
    Note: Each range is half-closed interval
    :param sampling_period:
    :param first_start:
    :param last_start:
    :param by_freq:
    :return:
    """
    if by_freq:
        start = pendulum.from_timestamp(int(first_start / 1000))
        end = pendulum.from_timestamp(int(last_start / 1000))
        period = pendulum.period(start, end)

        #unit_dict = {'A': 'years', 'M': 'months', 'W': 'weeks', 'D': 'days', 'H': 'hours', 'Q': 'months'}
        try:
            freq = list(freq_to_period_map.keys())[list(freq_to_period_map.values()).index(sampling_period)]
        except Exception as e:
            raise ValueError(f"Can't convert sampling period {sampling_period} to freq")
        if freq == "A":
            start_series = list(map(lambda x: int(x.timestamp() * 1000), period.range("years")))
            end_series = list(map(lambda x: int(x.add(years=1).timestamp() * 1000), period.range("years")))
        elif freq == "M":
            start_series = list(map(lambda x: int(x.timestamp() * 1000), period.range("months")))
            end_series = list(map(lambda x: int(x.add(months=1).timestamp() * 1000), period.range("months")))
        elif freq == "W":
            start_series = list(map(lambda x: int(x.timestamp() * 1000), period.range("weeks")))
            end_series = list(map(lambda x: int(x.add(weeks=1).timestamp() * 1000), period.range("weeks")))
        elif freq == "D":
            start_series = list(map(lambda x: int(x.timestamp() * 1000), period.range("days")))
            end_series = list(map(lambda x: int(x.add(days=1).timestamp() * 1000), period.range("days")))
        elif freq == "H":
            start_series = list(map(lambda x: int(x.timestamp() * 1000), period.range("hours")))
            end_series = list(map(lambda x: int(x.add(hours=1).timestamp() * 1000), period.range("hours")))
        elif freq == 'Q':
            start_series = list(map(lambda x: int(x.timestamp() * 1000), period.range("months", 3)))
            end_series = list(map(lambda x: int(x.add(months=3).timestamp() * 1000), period.range("months", 3)))
        else:
            raise ValueError(f"Freq {freq} has no rule")
    else:
        start_series = list(range(first_start, last_start + 1, sampling_period))
        end_series = list(range(first_start + sampling_period, last_start + sampling_period + 1, sampling_period))

    return start_series, end_series


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
