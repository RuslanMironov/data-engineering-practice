import os

import requests
from bs4 import BeautifulSoup

urls = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2024/"


def url_check(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    date_search = "2024-06-02 09:55"
    for row in soup.find_all("tr"):
        if date_search in row.text:
            return url + row.find("a").text


def download_file(url):
    filename = os.path.basename(url)
    # response = requests.get(url)
    with requests.get(url) as response:
        if response.ok:
            with open(filename, "wb") as file:
                file.write(response.content)
        else:
            print(f"Download failed: {filename}")


def main():
    download_file(url_check(urls))


if __name__ == "__main__":
    main()
