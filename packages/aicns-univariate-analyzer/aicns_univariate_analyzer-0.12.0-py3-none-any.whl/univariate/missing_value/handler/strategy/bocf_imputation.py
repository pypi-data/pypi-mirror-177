"""

"""

from univariate.missing_value.handler.strategy import MissingValueHandleStrategy, MissingValueHandleStrategyType
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.sql.window import Window


class BOCFImputation(MissingValueHandleStrategy):
    """ """

    def handle(
        self, missed_ts: DataFrame, time_col_name: str, data_col_name, handled_col_name: str) -> DataFrame:
        """

        :param missed_ts:
        :param time_col_name:
        :param data_col_name:
        :param handled_col_name:
        :return:
        """
        window = Window.orderBy(time_col_name).rowsBetween(Window.currentRow, Window.unboundedFollowing)
        filled_ts = missed_ts.withColumn(handled_col_name, F.first(data_col_name, ignorenulls=True).over(window))
        return filled_ts
