import os
import sys

import pandas as pd

from crawler import adana, mersin

import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
urllib3.disable_warnings(category=InsecureRequestWarning)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crawler.py <city-name>")
        sys.exit(1)

    if not os.path.exists("data"):
        os.mkdir("data")

    city = sys.argv[1]
    if city == "Adana":
        data = adana.AOSBCrawler().crawl_each_sector()
        pd.DataFrame(data).to_csv("data/aosb.csv", index=False)
    
    if city == "Mersin":
        data = mersin.MTOSBCrawler().crawl_each_page()
        pd.DataFrame(data).to_csv("data/mtosb.csv", index=False)
