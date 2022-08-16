import pandas as pd
import numpy as np
from saham.indikator.indicatorinputhandler import IndicatorInputHandler

class StochasticOscillator(IndicatorInputHandler):
    """Stochastic Oscillator

    Developed in the late 1950s by George Lane. The stochastic
    oscillator presents the location of the closing price of a
    stock in relation to the high and low range of the price
    of a stock over a period of time, typically a 14-day period.

    https://school.stockcharts.com/doku.php?id=technical_indicators:stochastic_oscillator_fast_slow_and_full

    Args:
        close(pandas.Series): dataset 'Close' column.
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        window(int): n period.
        smooth_window(int): sma period over stoch_k.
        fillna(bool): if True, fill nan values.
    """

    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 14,
        smooth_window: int = 3,
        fillna: bool = False,
    ):
        self._close = close
        self._high = high
        self._low = low
        self._window = window
        self._smooth_window = smooth_window
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods = 0 if self._fillna else self._window
        smin = self._low.rolling(self._window, min_periods=min_periods).min()
        smax = self._high.rolling(self._window, min_periods=min_periods).max()
        self._stoch_k = 100 * (self._close - smin) / (smax - smin)

    def stoch(self) -> pd.Series:
        """Stochastic Oscillator

        Returns:
            pandas.Series: New feature generated.
        """
        stoch_k = self._check_fillna(self._stoch_k, value=50)
        return pd.Series(stoch_k, name="stoch_k")

    def stoch_signal(self) -> pd.Series:
        """Signal Stochastic Oscillator

        Returns:
            pandas.Series: New feature generated.
        """
        min_periods = 0 if self._fillna else self._smooth_window
        stoch_d = self._stoch_k.rolling(
            self._smooth_window, min_periods=min_periods
        ).mean()
        stoch_d = self._check_fillna(stoch_d, value=50)
        return pd.Series(stoch_d, name="stoch_k_signal")