import pandas as pd
import numpy as np
from saham.indikator.indicatorinputhandler import IndicatorInputHandler

class MFIIndicator(IndicatorInputHandler):
    """Money Flow Index (MFI)

    Uses both price and volume to measure buying and selling pressure. It is
    positive when the typical price rises (buying pressure) and negative when
    the typical price declines (selling pressure). A ratio of positive and
    negative money flow is then plugged into an RSI formula to create an
    oscillator that moves between zero and one hundred.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:money_flow_index_mfi

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        window(int): n period.
        fillna(bool): if True, fill nan values.
    """

    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        volume: pd.Series,
        window: int = 14,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        typical_price = (self._high + self._low + self._close) / 3.0
        up_down = np.where(
            typical_price > typical_price.shift(1),
            1,
            np.where(typical_price < typical_price.shift(1), -1, 0),
        )
        mfr = typical_price * self._volume * up_down

        # Positive and negative money flow with n periods
        min_periods = 0 if self._fillna else self._window
        n_positive_mf = mfr.rolling(self._window, min_periods=min_periods).apply(
            lambda x: np.sum(np.where(x >= 0.0, x, 0.0)), raw=True
        )
        n_negative_mf = abs(
            mfr.rolling(self._window, min_periods=min_periods).apply(
                lambda x: np.sum(np.where(x < 0.0, x, 0.0)), raw=True
            )
        )

        # n_positive_mf = np.where(mf.rolling(self._window).sum() >= 0.0, mf, 0.0)
        # n_negative_mf = abs(np.where(mf.rolling(self._window).sum() < 0.0, mf, 0.0))

        # Money flow index
        mfi = n_positive_mf / n_negative_mf
        self._mfi = 100 - (100 / (1 + mfi))

    def money_flow_index(self) -> pd.Series:
        """Money Flow Index (MFI)

        Returns:
            pandas.Series: New feature generated.
        """
        mfi = self._check_fillna(self._mfi, value=50)
        return pd.Series(mfi, name=f"mfi_{self._window}")