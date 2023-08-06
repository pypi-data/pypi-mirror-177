from ctypes import *
from datetime import datetime

import numpy as np

from .helpers import prepare_coords, prepare_dt, c_double_p, DATADIR
from .echaimlib import echaimlib


def nmf2(lats: np.ndarray, lons: np.ndarray, dt: datetime) -> np.ndarray:
    lats_p, lons_p, l0 = prepare_coords(lats, lons)
    year_p, month_p, day_p, hour_p, minute_p, second_p = prepare_dt(dt, len(lats))

    output = np.empty(len(lats), dtype=np.float64)
    output_p = output.ctypes.data_as(c_double_p)

    echaimlib.pyNmF2(output_p, DATADIR.encode("utf-8"),
                     lats_p, lons_p, year_p, month_p, day_p,
                     hour_p, minute_p, second_p, l0, c_int(0))
    return output


def nmf2_storm(lats: np.ndarray, lons: np.ndarray, dt: datetime) -> np.ndarray:
    lats_p, lons_p, l0 = prepare_coords(lats, lons)
    year_p, month_p, day_p, hour_p, minute_p, second_p = prepare_dt(dt, len(lats))

    output = np.empty(len(lats), dtype=np.float64)
    output_p = output.ctypes.data_as(c_double_p)

    echaimlib.pyNmF2Storm(output_p, DATADIR.encode("utf-8"),
                          lats_p, lons_p, year_p, month_p, day_p,
                          hour_p, minute_p, second_p, l0, c_int(0))
    return output


def hmf2(lats: np.ndarray, lons: np.ndarray, dt: datetime) -> np.ndarray:
    lats_p, lons_p, l0 = prepare_coords(lats, lons)
    year_p, month_p, day_p, hour_p, minute_p, second_p = prepare_dt(dt, len(lats))

    output = np.empty(len(lats), dtype=np.float64)
    output_p = output.ctypes.data_as(c_double_p)

    echaimlib.pyHmF2(output_p, DATADIR.encode("utf-8"),
                     lats_p, lons_p, year_p, month_p, day_p,
                     hour_p, minute_p, second_p, l0, c_int(0))
    return output


def hmf1(lats: np.ndarray, lons: np.ndarray, dt: datetime) -> np.ndarray:
    lats_p, lons_p, l0 = prepare_coords(lats, lons)
    year_p, month_p, day_p, hour_p, minute_p, second_p = prepare_dt(dt, len(lats))

    output = np.empty(len(lats), dtype=np.float64)
    output_p = output.ctypes.data_as(c_double_p)

    echaimlib.pyHmF1(output_p, DATADIR.encode("utf-8"),
                     lats_p, lons_p, year_p, month_p, day_p,
                     hour_p, minute_p, second_p, l0, c_int(0))
    return output
