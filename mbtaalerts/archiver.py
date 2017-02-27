"""
The archiver module will perform the function of querying
the MBTA APIs that contain relevant data and archiving them
to our database.
"""

import os
import logging
import time

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%m/%d %H:%M:%S',
    level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("archive")

def helper_function():
    """
    A simple function to test that tests can access code
    :return: It returns 1
    """
    return 1

def main():
    """
    The entry point for the program
    """
    while True:
        LOG.info("still running")
        # Sleep for 1 minute
        time.sleep(60)
    LOG.info("finished")

if __name__ == "__main__":
    main()
