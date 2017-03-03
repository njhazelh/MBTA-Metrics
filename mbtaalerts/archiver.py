import os
import logging
import time
import requests

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%m/%d %H:%M:%S', level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("archive")

def main():
    requestUrl = "http://realtime.mbta.com/developer/api/v2/alerts?api_key=wX9NwuHnZU2ToO7GmGR9uw&include_access_alerts=true&include_service_alerts=true&format=json"
    r = requests.get(requestUrl)
    print(r.json())
    while True:
        LOG.info("still running")
        # Sleep for 1 minute
        time.sleep(60)
    LOG.info("finished")

if __name__ == "__main__":
    main()
