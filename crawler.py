import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class AOSBCrawler:
    def __init__(self, root_url):
        self.session = requests.session()
        self.session.verify = False
        self.root_url = root_url

    def crawl_sector_links(self):
        r = self.session.get(self.root_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, features="lxml")

            return [
                link.a.get("href")
                for link in soup.find_all("span", class_="gd-cptcat-cat-right")
                if int(link.find("span", class_="gd-cptcat-count").text) > 0
            ]

    def __parse_each_post(self, post):
        title = post.h2.a.text.strip()
        url = post.h2.a.get("href").strip()
        info = post.find("div", class_="geodir-output-location")
        try:
            category = info.find("div", class_="geodir-field-post_category").a.text
        except Exception:
            category = ""
        try:
            tel = info.find("div", class_="geodir-field-phone").text[len("Telefon: ") :]
        except Exception:
            tel = ""
        try:
            fax = info.find("div", class_="geodir-field-fax").text[len("Fax: ") :]
        except Exception:
            fax = ""
        try:
            mail = info.find("div", class_="geodir-field-email").text[len("Email: ") :]
        except Exception:
            mail = ""
        try:
            website = info.find("div", class_="geodir-field-website").a.get("href")
        except Exception:
            website = ""

        d = {
            "title": title,
            "url": url,
            "category": category,
            "tel": tel,
            "fax": fax,
            "mail": mail,
            "website": website,
        }
        return d

    def crawl_each_sector(self):
        links = self.crawl_sector_links()

        data = []
        for link in links:
            r = self.session.get(link)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, features="lxml")
                posts = soup.main.find("div", class_="post-content").find_all(
                    "div", class_="gd-list-item-right"
                )
                for post in posts:
                    data.append(self.__parse_each_post(post))
        return data


aosb_url = "https://www.adanaorganize.org.tr/firmalar/"
crawler = AOSBCrawler(aosb_url)
data = crawler.crawl_each_sector()

pd.DataFrame(data).to_csv("aosb.csv", index=False)
