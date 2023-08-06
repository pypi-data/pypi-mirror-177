from ctypes import *
from datetime import datetime
from .helpers import prepare_coords, prepare_dt, c_double_p, DATADIR
import numpy as np
from .echaimlib import echaimlib


def update_echaim_data(force: bool = False):
    result = c_int(-1)
    print("Updating E-CHAIM database...")
    echaimlib.update_database(byref(result), DATADIR.encode("utf-8"), c_int(force))
    if result.value == 0 or result.value == 3:
        print("The E-CHAIM database was updated.")
    else:
        print("The E-CHAIM database was not updated. Try forcing the update.")
