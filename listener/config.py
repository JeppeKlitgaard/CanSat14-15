import time

# ### FAKER ###
FAKER_MAX = 1023
FAKER_MIN = -1023

# ### MINITERM ###


def miniterm_get_log_file():
    return "cansat_{}.log".format(str(int(time.time())))


# ### COMMUNICATIONS FILE ###
COM_FILE = "listener_com.log"


# GYRO
GYRO_SENSITIVITY = 2000
GYRO_CALIBRATION_FACTOR = 1.1

# HEIGHT
TEMPERATURE_GRADIENT = -0.0065
R_CONSTANT = 287.06
GRAVITATIONAL_ACCELLERATION = 9.82
# PRESS_GROUND = 100.75  # in kilopascal, droptest
# TEMP_GROUND = 7.2  # in degrees celsius, droptest
TEMP_GROUND = 5.3
PRESS_GROUND = 98.8

# POST PROCESSING
MIN_TIME = 1564364
MAX_TIME = 9999999
PRESSURE_AVERAGE_AMOUNT = 30
