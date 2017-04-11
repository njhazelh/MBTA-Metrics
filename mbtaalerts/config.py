"""
This configuration module will allow a path to the config file to be
passed as an environment variable. Other modules can route through
this configuration module to read the variant-specific file (eg,
a production config, dev config, tests config)
"""
import configparser
import os

config = configparser.ConfigParser()
config.read(os.getenv("CONFIG", "settings.cfg"))
