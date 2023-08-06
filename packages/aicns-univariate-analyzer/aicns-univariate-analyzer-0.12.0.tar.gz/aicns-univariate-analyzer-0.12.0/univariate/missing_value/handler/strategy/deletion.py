"""

"""

from univariate.missing_value.handler.strategy import MissingValueHandleStrategy
from pyspark.sql import DataFrame


class Deletion(MissingValueHandleStrategy):
    """
    Delete data missing values in dataframe(na, null)
    """

    def handle(
        self, missed_ts: DataFrame, time_col_name: str, data_col_name
    ) -> DataFrame:
        return missed_ts.dropna(subset=data_col_name)
