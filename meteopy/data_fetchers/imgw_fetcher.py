from __future__ import annotations

import os
import zipfile
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup

from meteopy.utils.logging import get_logger

logger = get_logger(__name__)

class IMGWDataFetcher:
    def __init__(self, type: str, beginning: int, ending: int, unzip: bool = True) -> None:
        self.base_url = "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/"
        self.type = type
        self.beginning = beginning
        self.ending = ending
        self.unzip = unzip
        self.data_dir = Path(__file__).resolve().parent.parent / "data" / "downloaded"

        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.download_all()

    def fetch(self, base_url: str = None) -> list:
        found = []

        if base_url is None:
            base_url = self.base_url + self.type + "/"

        try:
            response = requests.get(base_url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f"Error downloading {base_url}: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        for link in links:
            href = link.get("href")
            if href is not None:
                try:
                    if "_" in href and "/" in href:
                        start, end = map(int, href[:-1].split("_")[:2])
                        if start <= self.beginning <= self.ending or start <= self.ending <= end:
                            full_url = urljoin(base_url, href)
                            found.extend(self.fetch(full_url))
                    else:
                        year = int(href[:4])
                        if self.beginning <= year <= self.ending:
                            full_url = urljoin(base_url, href)
                            if full_url[-1] == "/":
                                found.extend(self.fetch(full_url))
                            else:
                                found.append(full_url)
                except ValueError:
                    continue

        return found

    def download_file(self, url: str) -> None:
        filename = self.data_dir / url.split("/")[-1]
        self.data_dir.mkdir(parents=True, exist_ok=True)
        urlretrieve(url, filename)

        if self.unzip:
            with zipfile.ZipFile(str(filename), "r") as zip_ref:
                extracted_files = zip_ref.namelist()
                for file in extracted_files:
                    extracted_file_path = self.data_dir / file
                    if extracted_file_path.exists():
                        logger.info(f"File {extracted_file_path} already exists")
                    else:
                        logger.info(f"Unpacking {file}...")
                        zip_ref.extract(file, str(self.data_dir))
            os.remove(filename)

    def download_all(self) -> None:
        links = self.fetch()
        if links:
            for link in links:
                self.download_file(link)
            logger.info("All files downloaded")
        else:
            logger.info("No files found to download.")






