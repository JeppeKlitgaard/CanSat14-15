"""
Contains the configuration parameters used by the groundstation module.
"""

BIND_ADDRESS = "0.0.0.0"

DATA_BASE_PATH = "data"
DATA_CONFIG_FILE = "data_config.json"

PRESENTER = {
    "port": 80,
    "address": BIND_ADDRESS,
    "debug": True,
    "database": "sqliteext:///presenter.db"
}

FAKER = {
    "min_value": -1023,
    "max_value": 1023,
    "data_interval": 1,  # Seconds
    "malformed_line_chance": 0.1  # decimal 1 = 100%
}

FEEDER = {
    "cache_size": 100,
    "port": 8081,
    "frequency": 10  # ms
}

GENERAL = {
    "com_file": "com_file",
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

EXAMPLE_DATA_CONFIG = {
    "id": "identifier",
    "name": "name",
    "file": "file.log",
    "start_time": 0,
    "end_time": -1,
    "ground_temperature": 0,
    "ground_pressure": 100
}
