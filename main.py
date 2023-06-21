import os
import sys

import pandas as pd

from crawler import adana, mersin, osmaniye

import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
urllib3.disable_warnings(category=InsecureRequestWarning)

cities = ["adana", "mersin", "osmaniye"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crawler.py <city-name | all>")
        sys.exit(1)

    if not os.path.exists("data"):
        os.mkdir("data")

    city = sys.argv[1].lower()
    if city == "adana":
        data = adana.AOSBCrawler().run_crawler()
        pd.DataFrame(data).to_csv("data/aosb.csv", index=False)
    
    if city == "mersin":
        data = mersin.MTOSBCrawler().run_crawler()
        pd.DataFrame(data).to_csv("data/mtosb.csv", index=False)
    
    if city == "osmaniye":
        data = osmaniye.OOSBCrawler().run_crawler()
        pd.DataFrame(data).to_csv("data/oosb.csv", index=False)
