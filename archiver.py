import os
import logging
import time

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("archive")


def main():
    while True:
        LOG.info("still running")
        # Sleep for 1 minute
        time.sleep(60)


if __name__ == "__main__":
    main()
