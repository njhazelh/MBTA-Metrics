"""
This configuration module will allow a path to the config file to be
passed as an environment variable. Other modules can route through
this configuration module to read the variant-specific file (eg,
a production config, dev config, tests config)
"""
import configparser
import os
import logging

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%m/%d %H:%M:%S',
    level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("config")

mbta_config_path = ""

try:
    mbta_config_path = os.environ['CONFIG']
    if not os.path.isfile(mbta_config_path):
        raise FileNotFoundError("Couldn't open CONFIG file: " + mbta_config_path)

except KeyError as ky_err:
    LOG.error("Couldn't find CONFIG environment variable.")
    LOG.error("Example: CONFIG='<file_location>' python -m mbtalerts.<module>")
    raise

directed_config = configparser.ConfigParser()
directed_config.read(mbta_config_path)

def get(section, key):
    """Pass the call down to configparser"""
    return directed_config.get(section, key)

def main():
    pass

if __name__ == "__main__":
    main()
