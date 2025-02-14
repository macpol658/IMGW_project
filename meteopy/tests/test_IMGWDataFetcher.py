from __future__ import annotations

import io
import sys
import zipfile
from urllib.parse import urljoin

import requests

from meteopy.data_fetchers.imgw_fetcher import IMGWDataFetcher
from meteopy.utils.logging import get_logger

logger = get_logger(__name__)


def test_fetch(monkeypatch):

    instance = IMGWDataFetcher.__new__(IMGWDataFetcher)
    instance.base_url = "http://example.com/"
    instance.type = "dummy"
    instance.beginning = 2000
    instance.ending = 2020

    html_content = '<html><body><a href="2010_data.zip">Download</a></body></html>'

    def fake_get(url, **kwargs):
        class DummyResponse:
            def __init__(self, text):
                self.text = text
            def raise_for_status(self):
                pass
        return DummyResponse(html_content)

    monkeypatch.setattr(requests, "get", fake_get)

    links = instance.fetch(base_url="http://example.com/")
    expected = [urljoin("http://example.com/", "2010_data.zip")]
    assert links == expected


def test_download_file(monkeypatch, tmp_path):

    dummy_zip_io = io.BytesIO()
    with zipfile.ZipFile(dummy_zip_io, mode="w") as zip_file:
        zip_file.writestr("test.txt", "hello world")
    dummy_zip_bytes = dummy_zip_io.getvalue()

    def fake_urlretrieve(url, filename):
        with open(filename, "wb") as f:
            f.write(dummy_zip_bytes)

    module = sys.modules[IMGWDataFetcher.__module__]
    monkeypatch.setattr(module, "urlretrieve", fake_urlretrieve)

    instance = IMGWDataFetcher.__new__(IMGWDataFetcher)
    instance.data_dir = tmp_path / "downloaded"
    instance.data_dir.mkdir(exist_ok=True)
    instance.unzip = True

    fake_url = "http://example.com/fake.zip"
    instance.download_file(fake_url)

    zip_file_path = instance.data_dir / "fake.zip"
    assert not zip_file_path.exists()

    extracted_file_path = instance.data_dir / "test.txt"
    assert extracted_file_path.exists()
    content = extracted_file_path.read_text(encoding="utf-8")
    assert content == "hello world"


def test_download_all(monkeypatch, tmp_path):

    dummy_zip_io = io.BytesIO()
    with zipfile.ZipFile(dummy_zip_io, mode="w") as zip_file:
        zip_file.writestr("test.txt", "hello world")
    dummy_zip_bytes = dummy_zip_io.getvalue()

    def fake_urlretrieve(url, filename):
        with open(filename, "wb") as f:
            f.write(dummy_zip_bytes)

    module = sys.modules[IMGWDataFetcher.__module__]
    monkeypatch.setattr(module, "urlretrieve", fake_urlretrieve)

    instance = IMGWDataFetcher.__new__(IMGWDataFetcher)
    instance.data_dir = tmp_path / "downloaded"
    instance.data_dir.mkdir(exist_ok=True)
    instance.unzip = True

    instance.fetch = lambda base_url=None: [
        "http://example.com/file1.zip",
        "http://example.com/file2.zip"
    ]

    instance.download_all()

    zip_files = list(instance.data_dir.glob("*.zip"))
    assert len(zip_files) == 0

    extracted_file = instance.data_dir / "test.txt"
    assert extracted_file.exists()
    content = extracted_file.read_text(encoding="utf-8")
    assert content == "hello world"
