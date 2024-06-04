import asyncio
import os
import zipfile

import aiohttp

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


def check_directory(dir_name):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    os.chdir(dir_name)


async def download_file(session, url):
    filename = os.path.basename(url)
    async with session.get(url, ssl=False) as response:
        if response.status == 200:
            with open(filename, "wb") as file:
                file.write(await response.read())
        else:
            print(f"Download failed: {filename}")


async def downloads_files(urls):
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = [download_file(session, url) for url in urls]
        await asyncio.gather(*tasks)


async def unzip():
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            with zipfile.ZipFile(file, "r") as zip_file:
                zip_file.extractall()
                os.remove(file)


async def main():
    check_directory("downloads")
    await downloads_files(download_uris)
    await unzip()


if __name__ == "__main__":
    asyncio.run(main())
