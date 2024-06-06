import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
from bs4 import BeautifulSoup

urls = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2024/"
columns_name = "HourlyDryBulbTemperature"
date_search = "2024-06-05 20:15"


def url_check(url) -> str | None:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for row in soup.find_all("tr"):
        if date_search in row.text:
            return url + row.find("a").text
    return None


def download__read_file(url) -> pd.DataFrame:
    try:
        filename = os.path.basename(url)
        with requests.get(url) as response:
            if response.ok:
                with open(filename, "wb") as file:
                    file.write(response.content)
                return pd.read_csv(filename)

    except Exception as e:
        print(e)
        raise Exception(f"Download failed: {e}")


def main():
    with ThreadPoolExecutor(max_workers=4) as executor:
        urls_list = [urls]
        future = list(executor.map(url_check, urls_list))
        try:
            result = list(executor.map(download__read_file, future))

            result_df = pd.concat(result, ignore_index=True)
            print(result_df[columns_name].max())
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
