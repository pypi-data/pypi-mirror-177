from __future__ import annotations

from ctypes import *
from datetime import datetime
from .helpers import prepare_coords, prepare_dt, c_double_p, DATADIR
import numpy as np
from .echaimlib import echaimlib
from collections.abc import Collection


def density_profile(lats: np.ndarray, lons: np.ndarray, alts: np.ndarray, dt: datetime | Collection, storm: bool = True,
                    precip: bool = True, dregion: bool = True) -> np.ndarray:
    if alts.ndim != 1:
        raise ValueError("Array of altitudes must be 1D")
    l1 = c_int(len(alts))

    lats = lats.astype(np.float64)
    lons = lons.astype(np.float64)
    alts = alts.astype(np.float64)

    alts_p = alts.ctypes.data_as(c_double_p)
    lats_p, lons_p, l0 = prepare_coords(lats, lons)
    year_p, month_p, day_p, hour_p, minute_p, second_p = prepare_dt(dt, len(lats))

    output = np.zeros(len(alts)*len(lats), dtype=np.float64)

    output_p = output.ctypes.data_as(c_double_p)

    echaimlib.pyDensityProfile(output_p, DATADIR.encode("utf-8"),
                               lats_p, lons_p,
                               year_p, month_p, day_p,
                               hour_p, minute_p, second_p,
                               c_int(storm), c_int(precip), c_int(dregion),
                               l0, alts_p, l1, c_int(0))

    return output.reshape((len(lats), len(alts)))


def density_path(lats: np.ndarray, lons: np.ndarray, alts: np.ndarray, dt: datetime, storm: bool = True,
                 precip: bool = True, dregion: bool = True) -> np.ndarray:
    lats = lats.astype(np.float64)
    lons = lons.astype(np.float64)
    alts = alts.astype(np.float64)
    if not lats.size == lons.size == alts.size:
        raise ValueError("Shapes of lat, lon and alt arrays must be the same.")
    if not alts.ndim == lons.ndim == lats.ndim == 1:
        raise ValueError("Lat, lon and alt arrays must be 1D.")

    alts_p = alts.ctypes.data_as(c_double_p)
    lats_p, lons_p, l0 = prepare_coords(lats, lons)
    year_p, month_p, day_p, hour_p, minute_p, second_p = prepare_dt(dt, len(lats))

    output = np.empty(len(alts), dtype=np.float64)
    output_p = output.ctypes.data_as(c_double_p)

    echaimlib.pyDensityPath(output_p, DATADIR.encode("utf-8"),
                            lats_p, lons_p, alts_p,
                            year_p, month_p, day_p,
                            hour_p, minute_p, second_p,
                            c_int(storm), c_int(precip), c_int(dregion),
                            l0, c_int(0))
    return output
