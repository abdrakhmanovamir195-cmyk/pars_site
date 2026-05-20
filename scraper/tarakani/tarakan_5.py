import requests
from bs4 import BeautifulSoup
from time import sleep

def parse():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    results = []

    for page in range(21, 26):
        sleep(1)
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all("article", class_="product_pod")
        for i in data:
            name = i.find("h3").find("a")["title"]
            price = i.find("p", class_="price_color").text
            url_img = "https://books.toscrape.com/" + i.find("img")["src"].replace("../", "")
            results.append({"name": name, "price": price, "url_img": url_img})

    return results

if __name__ == "__main__":
    results = parse()
    for item in results:
        print(item)