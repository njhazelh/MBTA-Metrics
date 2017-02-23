import os
import logging
import time

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%m/%d %H:%M:%S', level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("archive")

def helper_function():
    return 1

def main():
    while True:
        LOG.info("still running")
        # Sleep for 1 minute
        time.sleep(60)
    LOG.info("finished")

if __name__ == "__main__":
    main()
