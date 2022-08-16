import pandas as pd
import numpy as np
from saham.indikator.indicatorinputhandler import IndicatorInputHandler

class CCIIndicator(IndicatorInputHandler):
    """Commodity Channel Index (CCI)

    CCI measures the difference between a security's price change and its
    average price change. High positive readings indicate that prices are well
    above their average, which is a show of strength. Low negative readings
    indicate that prices are well below their average, which is a show of
    weakness.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:commodity_channel_index_cci

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
        constant(int): constant.
        fillna(bool): if True, fill nan values.
    """

    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 20,
        constant: float = 0.015,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._constant = constant
        self._fillna = fillna
        self._run()

    def _run(self):
        def _mad(x):
            return np.mean(np.abs(x - np.mean(x)))

        min_periods = 0 if self._fillna else self._window
        typical_price = (self._high + self._low + self._close) / 3.0
        self._cci = (
            typical_price
            - typical_price.rolling(self._window,
                                    min_periods=min_periods).mean()
        ) / (
            self._constant
            * typical_price.rolling(self._window, min_periods=min_periods).apply(
                _mad, True
            )
        )

    def cci(self) -> pd.Series:
        """Commodity Channel Index (CCI)

        Returns:
            pandas.Series: New feature generated.
        """
        cci_series = self._check_fillna(self._cci, value=0)
        return pd.Series(cci_series, name="cci")