import requests
from bs4 import BeautifulSoup

def serialize_text(text):
    text = text.strip()
    return None if text == "" else text

class OOSBCrawler:
    def __init__(self):
        self.session = requests.session()
        self.session.verify = False
        self.root_url = "https://www.oosb.org.tr/firmalar.php"
        self.main_root_url = "https://www.oosb.org.tr"

    def __parse_table_row(self, table_row):
        td = table_row.find_all("td")
        td = [None if i.text == "" else i.text.strip() for i in td[1:]]
        d = {
            "Title": td[0],
            "Sector": td[1],
            "Phone": td[2],
            "Email": td[3],
            "Fax": td[4],
        }
        return d

    def __crawl_company_page(self, company_url):
        response = self.session.get(f"{self.main_root_url}/{company_url}")
        soup = BeautifulSoup(response.text, "lxml")

        div = soup.find("div", class_="firmaBilgiler sol").find_all("div", class_="sol")

        d = {
            "Title": serialize_text(div[1].text),
            "Sector": serialize_text(div[5].text),
            "Phone": serialize_text(div[9].text),
            "Fax": serialize_text(div[11].text),
            "Website": serialize_text(div[13].text),
            "Email": serialize_text(div[15].text),
            "Address": serialize_text(div[17].text),
        }
        return d

    def __crawl_company_tables(self):
        response = self.session.get(self.root_url)
        soup = BeautifulSoup(response.text, "lxml")
        data = []

        tr = soup.table.find_all("tr")[1:]  # First one is header

        for i in tr:
            company_url = i.find_all("td")[1].a.get("href")
            d = self.__crawl_company_page(company_url)
            data.append(d)

        return data

    def run_crawler(self):
        return self.__crawl_company_tables()
