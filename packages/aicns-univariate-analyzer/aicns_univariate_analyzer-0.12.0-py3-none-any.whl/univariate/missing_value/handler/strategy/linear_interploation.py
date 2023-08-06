"""

"""

from univariate.missing_value.handler.strategy import MissingValueHandleStrategy, MissingValueHandleStrategyType
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from univariate.analyzer import AnalysisReport
from univariate.analyzer import DescriptiveStatAnalyzer
from typing import Optional
from pyspark.sql.window import Window


class LinearInterpolation(MissingValueHandleStrategy):
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
        # https://stackoverflow.com/questions/53077639/pyspark-interpolation-of-missing-values-in-pyspark-dataframe-observed
        # create row number over window and a column with row number only for non missing values
        window = Window.orderBy(time_col_name)
        new_df = missed_ts.withColumn('rn', F.row_number().over(window))
        new_df = new_df.withColumn('rn_not_null', F.when(F.col(data_col_name).isNotNull(), F.col('rn')))

        # create relative references to the start value (last value not missing)
        w_start = Window.orderBy(time_col_name).rowsBetween(Window.unboundedPreceding, -1)
        new_df = new_df.withColumn('start_val', F.last(data_col_name, True).over(w_start))
        new_df = new_df.withColumn('start_rn', F.last('rn_not_null', True).over(w_start))

        # create relative references to the end value (first value not missing)
        w_end = Window.orderBy(time_col_name).rowsBetween(0, Window.unboundedFollowing)
        new_df = new_df.withColumn('end_val', F.first(data_col_name, True).over(w_end))
        new_df = new_df.withColumn('end_rn', F.first('rn_not_null', True).over(w_end))

        # create references to gap length and current gap position
        new_df = new_df.withColumn('diff_rn', F.col('end_rn') - F.col('start_rn'))
        new_df = new_df.withColumn('curr_rn', F.col('diff_rn') - (F.col('end_rn') - F.col('rn')))

        # calculate linear interpolation value
        lin_interp_func = (
                    F.round(F.col('start_val') + (F.col('end_val') - F.col('start_val')) / F.col('diff_rn') * F.col('curr_rn'), 3))
        new_df = new_df.withColumn(handled_col_name,
                                   F.when(F.col(data_col_name).isNull(), lin_interp_func).otherwise(F.col(data_col_name)))

        new_df = new_df.drop('rn', 'rn_not_null', 'start_val', 'end_val', 'start_rn', 'end_rn', 'diff_rn', 'curr_rn')
        return new_df
