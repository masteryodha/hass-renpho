from datetime import timedelta
from typing import Final

"""Constants for constants sake"""

DOMAIN: Final = "renpho_weight"
VERSION: Final = "0.0.2"

CONF_EMAIL: Final = 'email'
CONF_PASSWORD: Final = 'password'
CONF_REFRESH: Final = 'refresh'
CONF_WEIGHT_UNITS: Final = 'weight_units'

DEFAULT_CONF_WEIGHT_UNITS: Final = 'kg'
DEFAULT_CONF_REFRESH: Final = timedelta(hours=3)
MASS_KILOGRAMS: Final = "kg"
MASS_POUNDS: Final = "lbs"

KG_TO_LB_MULTIPLICATOR: Final = 2.2046226218

CONF_PUBLIC_KEY: Final = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+25I2upukpfQ7rIaaTZtVE744\nu2zV+HaagrUhDOTq8fMVf9yFQvEZh2/HKxFudUxP0dXUa8F6X4XmWumHdQnum3zm\nJr04fz2b2WCcN0ta/rbF2nYAnMVAk2OJVZAMudOiMWhcxV1nNJiKgTNNr13de0EQ\nIiOL2CUBzu+HmIfUbQIDAQAB\n-----END PUBLIC KEY-----'