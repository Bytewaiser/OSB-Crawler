import requests
from bs4 import BeautifulSoup

class MTOSBCrawler:
    def __init__(self):
        self.session = requests.session()
        self.session.verify = False
        self.root_url = "http://www.mtosb.org.tr/firmalar/"
        self.map = {
            "Adres": "Address",
            "Telefon": "Tel",
            "Fax": "Fax",
            "E-posta": "Email",
            "Sektör": "Sector",
            "Üretim": "Production",
            "Web": "Website"
        }

    def __parse_each_post(self, post):
        title = post.h2.text.strip()
        li_list = post.find_all("li")
        d = {"Title": title}
        for i in li_list:
            text = i.strong.text.strip()
            if i.strong.text in self.map:
                t = ""
                for j in i.strong.next_siblings:
                    t += j.text.strip()
                d[self.map[text]] = t[2:] # First two character is : and space
        return d
        

    def crawl_each_page(self, page_count=35):
        data = []
        for page_number in range(1, page_count + 1):
            url = f"{self.root_url}/?SayfaNo={page_number}"
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            posts = soup.find_all("div", class_="blog-info")
            for post in posts:
                data.append(self.__parse_each_post(post))
        return data

