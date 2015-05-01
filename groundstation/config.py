"""
Contains the configuration parameters used by the groundstation module.
"""

BIND_ADDRESS = "0.0.0.0"

PRESENTER = {
    "port": 80,
    "address": BIND_ADDRESS,
    "debug": True,
}

FAKER = {
    "min_value": -1023,
    "max_value": 1023,
    "data_interval": 1,  # Seconds
    "malformed_line_chance": 0.1  # decimal 1 = 100%
}

GENERAL = {
    "com_file": "listener_com.log",
    "data_base_path": "data",
    "data_config": "data_config.json"
}

CALCULATE = {
    "gyro": {
        "sensitivity": 2000,
        "calibration_factor": 1.1
    },
    "height": {
        "temperature_gradient": -0.0065,
        "gas_constant": 287.06,
        "gravitational_accelleration": 9.82
    }
}
# PRESS_GROUND = 100.75  # in kilopascal, droptest
# TEMP_GROUND = 7.2  # in degrees celsius, droptest
TEMP_GROUND = 5.3
PRESS_GROUND = 98.8

# POST PROCESSING
MIN_TIME = 1564364
MAX_TIME = 9999999
PRESSURE_AVERAGE_AMOUNT = 30
