import math
from .config import GYRO_SENSITIVITY, GYRO_CALIBRATION_FACTOR
from .config import (PRESS_GROUND, TEMP_GROUND, TEMPERATURE_GRADIENT,
                     R_CONSTANT, GRAVITATIONAL_ACCELLERATION)


def calculate_temp_LM35(raw_val):
    """
    """
    return (500 / 1023) * raw_val


def calculate_temp_NTC(raw_val):
    """
    raw_val = a
    """
    voltage = raw_val * 5 / 1023

    resistance = (5 * 10000 / voltage) - 10000

    temp = ((3.354016 * (10**-3)) + (2.569850 * (10**-4)) *
            math.log(resistance / 10000) + (2.62013 * (10**-12)) *
            (math.log(resistance / 10000))**2 + 6.38309 * (10**-15) *
            (math.log(resistance / 10000))**3)**-1 - 273.15

    return temp


def calculate_press(raw_val):
    return ((100 / 921) * raw_val) + 10


def calculate_height(press_air):
    """
    :type temp: an integer with the temperature at ground level in celsius
    """
    temp = TEMP_GROUND + 273.15  # Convert to kelvin

    a = TEMPERATURE_GRADIENT
    R = R_CONSTANT
    grav = GRAVITATIONAL_ACCELLERATION

    height = (temp / a) * ((press_air / PRESS_GROUND)**(-((a * R) / grav)) - 1)

    return height


def calculate_acc_x(raw_val):
    return 0.0072339 * raw_val + 0.45212


def calculate_acc_y(raw_val):
    return 0.0072472 * raw_val - 0.39860


def calculate_acc_z(raw_val):
    return 0.0071289 * raw_val + 0.62377


def calculate_gyr(raw_val):
    """
    :rtype: integer, degrees per second.
    """
    return (raw_val / (2**15 - 1)) * GYRO_SENSITIVITY * GYRO_CALIBRATION_FACTOR


def calculate_mag(raw_val):
    result = raw_val * 2 / ((2**15) - 1)
    return result
