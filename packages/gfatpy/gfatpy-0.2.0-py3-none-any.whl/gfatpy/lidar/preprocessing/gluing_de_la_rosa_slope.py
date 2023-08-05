from typing import Callable
from warnings import warn


import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from gfatpy.utils.optimized import best_slope_fit
from gfatpy.utils.utils import moving_average


def create_smoother(window_size: int) -> Callable[[np.ndarray], np.ndarray]:
    def smooth(row: np.ndarray) -> np.ndarray:
        return savgol_filter(row / np.nanmean(row), window_size, 4)

    return smooth


def take_mid_value(arr: np.ndarray) -> float:
    shape = arr.shape[0]
    return arr[shape // 2]


def gluing(
    signal_an: xr.DataArray,
    signal_pc: xr.DataArray,
    range_min: float = 1500,
    range_max: float = 5000,
    criteria_half_window: float = 1000,
    adjustment_half_window: float = 1000,
):

    sel_signal_an = signal_an.sel(
        range=slice(range_min - criteria_half_window, range_max + criteria_half_window)
    )
    sel_signal_pc = signal_pc.sel(
        range=slice(range_min - criteria_half_window, range_max + criteria_half_window)
    )

    sel_range = sel_signal_pc.range.values
    window_size_bins = int((criteria_half_window * 2) / (sel_range[1] - sel_range[0]))

    smooth_window = 11  # window_size_bins // 2

    sm_sel_signal_an = moving_average(sel_signal_an.values, window_size=10)
    sm_sel_signal_pc = moving_average(sel_signal_pc.values, window_size=10)
    # sm_sel_signal_an = np.apply_along_axis(
    #     create_smoother(smooth_window), 0, sel_signal_an.values
    # )
    # sm_sel_signal_pc = np.apply_along_axis(
    #     create_smoother(smooth_window), 0, sel_signal_pc.values
    # )

    signal_glued = signal_pc.values.copy()

    gluing_bins = best_slope_fit(
        sm_sel_signal_an / take_mid_value(sm_sel_signal_an),
        sm_sel_signal_pc / take_mid_value(sm_sel_signal_pc),
        window=window_size_bins,
    )

    plt.plot(gluing_bins)
    plt.show()
    gluing_ranges = sel_range[gluing_bins]

    shift_ratio = 0.4

    for idx, gluing_range in enumerate(gluing_ranges[:]):
        near_idx = (
            sel_range > (gluing_range - shift_ratio * adjustment_half_window)
        ) & (sel_range < (gluing_range + (1 + shift_ratio) * adjustment_half_window))

        # sel_an = sel_signal_an[dict(time=idx)][near_idx]
        # sel_pc = sel_signal_pc[dict(time=idx)][near_idx]

        sel_an = sm_sel_signal_an[idx, near_idx]
        sel_pc = sm_sel_signal_pc[idx, near_idx]

        r_gluing = np.corrcoef(sel_an, sel_pc)[0, 1]

        fit_values = np.polyfit(
            sel_an,  # type: ignore
            sel_pc,  # type: ignore
            1,
        )

        plt.scatter(sel_an, sel_pc)
        plt.plot(sel_an, np.polyval(fit_values, sel_an), label=f"{r_gluing}")
        plt.legend()
        plt.show()

        if r_gluing < 1:  # TODO: Adjust threshold
            signal_an2pc = np.polyval(fit_values, signal_an.values[idx, :])
            signal_glued[idx, :] = np.concatenate(
                [
                    signal_an2pc[signal_pc.range.values < gluing_range],
                    signal_pc[idx, signal_pc.range.values >= gluing_range],
                ]
            )
        else:
            warn(
                f"r2 thereshold condition not satisfied for profile in time index {idx}"
            )
            # TODO: warn or implement filling method

    return signal_glued
