from modulefinder import Module
import numpy as np
import pandas as pd
import resampling_rs

DOWNSAMPLE_F = 'downsample'

def switch_mod_with_y(y_dtype: np.dtype, mod: Module, downsample_func: str = DOWNSAMPLE_F):
    """The x-data is not considered in the downsampling
    
    Assumes equal binning.

    Parameters
    ----------
    y_dtype : np.dtype
        The dtype of the y-data
    mod : Module
        The module to select the appropriate function from
    downsample_func : str, optional
        The name of the function to use, by default DOWNSAMPLE_FUNC.
    """
    # FLOATS
    if np.issubdtype(y_dtype, np.floating):
        if y.dtype == np.float16:
            return getattr(mod, downsample_func + '_f16')
        elif y_dtype == np.float32:
            return getattr(mod, downsample_func + '_f32')
        elif y_dtype == np.float64:
            return getattr(mod, downsample_func + '_f64')
    # INTS
    elif np.issubdtype(y_dtype, np.integer):
        if y_dtype == np.int16:
            return getattr(mod, downsample_func + '_i16')
        elif y_dtype == np.int32:
            return getattr(mod, downsample_func + '_i32')
        elif y_dtype == np.int64:
            return getattr(mod, downsample_func + '_i64')
    # UINTS
    elif np.issubdtype(y_dtype, np.unsignedinteger):
        if y_dtype == np.uint16:
            return getattr(mod, downsample_func + '_u16')
        elif y_dtype == np.uint32:
            return getattr(mod, downsample_func + '_u32')
        elif y_dtype == np.uint64:
            return getattr(mod, downsample_func + '_u64')
    # BOOLS
    # TODO: support bools
    # elif data_dtype == np.bool:
        # return mod.downsample_bool
    raise ValueError(f"Unsupported data type (for y): {y_dtype}")

def switch_mod_with_x_and_y(x_dtype: np.dtype, y_dtype: np.dtype, mod: Module):
    """The x-data is considered in the downsampling
    
    Parameters
    ----------
    x_dtype : np.dtype
        The dtype of the x-data
    y_dtype : np.dtype
        The dtype of the y-data
    mod : Module
        The module to select the appropriate function from
    """
    # FLOATS
    if np.issubdtype(x_dtype, np.floating):
        if x_dtype == np.float16:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_f16')
        elif x_dtype == np.float32:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_f32')
        elif x_dtype == np.float64:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_f64')
    # INTS
    elif np.issubdtype(x_dtype, np.integer):
        if x_dtype == np.int16:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_i16')
        elif x_dtype == np.int32:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_i32')
        elif x_dtype == np.int64:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_i64')
    # UINTS
    elif np.issubdtype(x_dtype, np.unsignedinteger):
        if x_dtype == np.uint16:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_u16')
        elif x_dtype == np.uint32:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_u32')
        elif x_dtype == np.uint64:
            return switch_mod_with_y(y_dtype, mod, f'{DOWNSAMPLE_F}_u64')
    # BOOLS
    # TODO: support bools
    # elif data_dtype == np.bool:
        # return mod.downsample_bool
    raise ValueError(f"Unsupported data type (for x): {x_dtype}")

class ResamplingInterface():

    def __init__(self, resampling_mod: Module) -> None:
        self._mod = resampling_mod
        if hasattr(self.mod, 'simd'):
            self.mod_single_core = self._mod.simd
            self.mod_multi_core = self._mod.simd_parallel
        else:
            self.mod_single_core = self._mod.scalar
            self.mod_multi_core = self._mod.scalar_parallel
        
    def _aggregate_without_x(self, s: pd.Series, n_out: int) -> pd.Series:
        downsample_method = switch_mod_with_y(s.dtype, self.mod_single_core)
        idxs = downsample_method(s.values, n_out)
        return s.iloc[idxs]
    
    def _aggregate_with_x(self, s: pd.Series, n_out: int) -> pd.Series:
        downsample_method = switch_mod_with_x_and_y(s.index.dtype, s.dtype, self.mod_single_core)
        idxs = downsample_method(s.index.values, s.values, n_out)
        return s.iloc[idxs]

    def _aggregate_without_x_parallel(self, s: pd.Series, n_out: int) -> pd.Series:
        downsample_method = switch_mod_with_y(s.dtype, self.mod_multi_core)
        idxs = downsample_method(s.values, n_out)
        return s.iloc[idxs]
    
    def _aggregate_with_x_parallel(self, s: pd.Series, n_out: int) -> pd.Series:
        downsample_method = switch_mod_with_x_and_y(s.index.dtype, s.dtype, self.mod_multi_core)
        idxs = downsample_method(s.index.values, s.values, n_out)
        return s.iloc[idxs]

    def aggregate(self, s: pd.Series, n_out: int, parallel: bool = False) -> pd.Series:
        if s.index.freq is None:  # TODO: or the other way around??
            if parallel:
                return self._aggregate_without_x_parallel(s, n_out)
            else:
                return self._aggregate_without_x(s, n_out)
        else:
            if parallel:
                return self._aggregate_with_x_parallel(s, n_out)
            else:
                return self._aggregate_with_x(s, n_out)


# -----------------------------

MinMaxAggregator = ResamplingInterface(resampling_rs.minmax)
M4Aggregator = ResamplingInterface(resampling_rs.m4)
LTTBAggregator = ResamplingInterface(resampling_rs.lttb)
MinMaxLTTBAggregator = ResamplingInterface(resampling_rs.minmax_lttb)
