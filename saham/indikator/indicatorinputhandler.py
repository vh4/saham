import pandas as pd
import numpy as np

class IndicatorInputHandler:
    """General Indicator Input Handler"""

    _fillna = False

    def _check_fillna(self, series: pd.Series, value: int = 0) -> pd.Series:
        if self._fillna:
            series_output = series.copy(deep=False)
            series_output = series_output.replace([np.inf, -np.inf], np.nan)
            if isinstance(value, int) and value == -1:
                series = series_output.fillna(method="ffill").fillna(method='bfill')
            else:
                series = series_output.fillna(method="ffill").fillna(value)
        return series
    
    @staticmethod
    def _true_range(
        high: pd.Series, low: pd.Series, prev_close: pd.Series
    ) -> pd.Series:
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        true_range = pd.DataFrame(data={"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
        return true_range


    #Basic EMA Calculation

    def _ema(series, periods: int, fillna: bool = False):
        min_periods = 0 if fillna else periods
        return series.ewm(span=periods, min_periods=min_periods, adjust=False).mean()

    # Drop NaN 
    def dropna(df: pd.DataFrame) -> pd.DataFrame:
        """Drop rows with "Nans" values"""
        df = df.copy()
        number_cols = df.select_dtypes(include=np.number).columns.tolist()
        df[number_cols] = df[number_cols][df[number_cols] < math.exp(709)]  # big number
        df[number_cols] = df[number_cols][df[number_cols] != 0.0]
        df = df.dropna()
        return df
    