"""

"""

from enum import Enum
from abc import ABCMeta, abstractmethod
from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport


class MissingValueHandleStrategyType(Enum):
    deletion = "Deletion"
    mean_imputation = "MeanImputation"
    median_imputation = "MedianImputation"
    mode_imputation = "ModeImputation"
    locf_imputation = "LOCFImputation"
    bocf_imputation = "BOCFImputation"
    # constant_imputation = "ConstantImputation"
    # seasonality-based imputation

    linear_interpolation = "LinearInterpolation"
    lagrange_interpolation = "LagrangeInterpolation"
    cubic_spline_interpolation = "CubicSplineInterpolation"

    # k_nn_imputation = "KNNImputation" #multi
    # mice_imputation = "MICEImputation" #multi
    # regression # multi
    # stochastic regressioin # multi
    # hot_deck_imputation = "HOT_DECK_IMPUTATION" multi

    # todo: continous update
    # todo: where cross-informated strategy will be
    # todo: enhance
    # todo: process exceptions with sufficient test coverage


class MissingValueHandleStrategy(metaclass=ABCMeta):
    """
    Missing
    """

    @abstractmethod
    def handle(
        self, missed_ts: DataFrame, time_col_name: str, data_col_name: str, handled_col_name: str, **kwargs
    ) -> DataFrame:
        pass
