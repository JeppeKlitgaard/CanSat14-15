"""
Contains the functions and classes used to calculate and/or convert
values read from the sensors.
"""

import math
from .config import CALCULATE


TEMP_GROUND = 2
PRESS_GROUND = 100


def calculate_temp_NTC(raw_val):
    """
    Converts the raw value read from the NTC temperature sensor
    module into degrees celsius.
    """
    voltage = raw_val * 5 / 1023

    resistance = (5 * 10000 / voltage) - 10000

    temp = ((3.354016 * (10**-3)) + (2.569850 * (10**-4)) *
            math.log(resistance / 10000) + (2.62013 * (10**-12)) *
            (math.log(resistance / 10000))**2 + 6.38309 * (10**-15) *
            (math.log(resistance / 10000))**3)**-1 - 273.15

    return temp


def calculate_temp_LM35(raw_val):
    """
    Converts the raw value read from the LM35 temperature sensor
    module into degrees celsius.
    """
    return (500 / 1023) * raw_val


def calculate_press(*args, **kwargs):
    """
    Converts the raw value read from the pressure sensor module
    into kilopascal.
    """
    version = kwargs["version"]
    del kwargs["version"]

    if version in ["live", "portugal2015"]:
        return _calculate_press_portugal2015(*args, **kwargs)

    elif version in ["andoeya2015"]:
        return _calculate_press_andoeya2015(*args, **kwargs)

    else:
        raise ValueError("Invalid 'version'.")


def _calculate_press_portugal2015(raw_val):
    return raw_val / 10


def _calculate_press_andoeya2015(raw_val):
    """
    Converts the raw value read from the pressure sensor module
    into kilopascal.
    """
    return ((100 / 921) * raw_val) + 10


def calculate_height(air_press, ground_press, ground_temp):
    """
    Calculates the height based on the pressure, pressure at ground level,
    and temperature at ground level.
    """
    temp = ground_temp + 273.15  # Convert to kelvin

    a = CALCULATE["height"]["temperature_gradient"]
    R = CALCULATE["height"]["gas_constant"]
    grav = CALCULATE["height"]["gravitational_accelleration"]

    height = (temp / a) * ((air_press / ground_press)**(-((a * R) / grav)) - 1)

    return height


def calculate_acc(raw_val, direction):
    """
    Converts the raw value read from the accelleration sensor module,
    taking calibration into consideration.
    """
    calibs = CALCULATE["acc"]["acc_calib"]

    if direction not in calibs.keys():
        raise ValueError("'direction' must be one of: 'x', 'y', 'z'.")

    return calibs[direction][0] * raw_val + calibs[direction][1]


def calculate_gyr(raw_val):
    """
    Converts the raw value read from the gyroscope, taking calibration
    into consideration.

    Returns the rotational speed in degrees per second.
    """
    s = CALCULATE["gyro"]["sensitivity"]
    c = CALCULATE["gyro"]["calibration_factor"]
    return (raw_val / (2**15 - 1)) * s * c


def calculate_mag(raw_val):
    """
    Converts the raw value read from the magnetometer.
    Currently does not take calibration into consideration.
    """
    result = raw_val * 2 / ((2**15) - 1)
    return result
