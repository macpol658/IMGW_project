from __future__ import annotations

import os

import pytest

from meteopy.preprocessing.imgw_handler import IMGWDataHandler


@pytest.fixture
def handler_with_temp_dirs(tmp_path):

    input_dir = tmp_path / "downloaded"
    output_dir = tmp_path / "separated"
    input_dir.mkdir()
    output_dir.mkdir()

    handler = IMGWDataHandler.__new__(IMGWDataHandler)
    handler.input_directory = input_dir
    handler.output_directory = output_dir
    os.makedirs(handler.output_directory, exist_ok=True)
    return handler

def test_divide_downloaded_o_file(handler_with_temp_dirs):

    handler = handler_with_temp_dirs
    o_file = handler.input_directory / "o_test.csv"
    o_file.write_text("Station,Value\n101,1\n102,2\n101,3\n", encoding="ISO-8859-2")

    handler.divide_downloaded()

    assert not o_file.exists()

    out_file_101 = handler.output_directory / "o_station_101.csv"
    out_file_102 = handler.output_directory / "o_station_102.csv"
    assert out_file_101.exists()
    assert out_file_102.exists()

    content_101 = out_file_101.read_text(encoding="ISO-8859-2").strip().splitlines()
    content_102 = out_file_102.read_text(encoding="ISO-8859-2").strip().splitlines()

    assert content_101 == ["101,1", "101,3"]
    assert content_102 == ["102,2"]

def test_divide_downloaded_k_file(handler_with_temp_dirs):

    handler = handler_with_temp_dirs
    k_file = handler.input_directory / "kfile.csv"
    k_file.write_text("Station,Value\n201,10\n202,20\n201,30\n", encoding="ISO-8859-2")

    handler.divide_downloaded()

    assert not k_file.exists()

    out_file_201 = handler.output_directory / "k_station_201.csv"
    out_file_202 = handler.output_directory / "k_station_202.csv"
    assert out_file_201.exists()
    assert out_file_202.exists()

    content_201 = out_file_201.read_text(encoding="ISO-8859-2").strip().splitlines()
    content_202 = out_file_202.read_text(encoding="ISO-8859-2").strip().splitlines()
    assert content_201 == ["201,10", "201,30"]
    assert content_202 == ["202,20"]

def test_divide_downloaded_k_t_file(handler_with_temp_dirs):

    handler = handler_with_temp_dirs
    k_t_file = handler.input_directory / "k_t_test.csv"
    k_t_file.write_text("Station,Value\n301,100\n302,200\n301,300\n", encoding="ISO-8859-2")

    handler.divide_downloaded()

    assert not k_t_file.exists()

    out_file_301 = handler.output_directory / "k_t_station_301.csv"
    out_file_302 = handler.output_directory / "k_t_station_302.csv"
    assert out_file_301.exists()
    assert out_file_302.exists()

    content_301 = out_file_301.read_text(encoding="ISO-8859-2").strip().splitlines()
    content_302 = out_file_302.read_text(encoding="ISO-8859-2").strip().splitlines()
    assert content_301 == ["301,100", "301,300"]
    assert content_302 == ["302,200"]

def test_divide_downloaded_s_file(handler_with_temp_dirs):

    handler = handler_with_temp_dirs
    s_file = handler.input_directory / "sfile.csv"
    s_file.write_text("Station,Value\n401,50\n402,60\n401,70\n", encoding="ISO-8859-2")

    handler.divide_downloaded()

    assert not s_file.exists()

    out_file_401 = handler.output_directory / "s_station_401.csv"
    out_file_402 = handler.output_directory / "s_station_402.csv"
    assert out_file_401.exists()
    assert out_file_402.exists()

    content_401 = out_file_401.read_text(encoding="ISO-8859-2").strip().splitlines()
    content_402 = out_file_402.read_text(encoding="ISO-8859-2").strip().splitlines()
    assert content_401 == ["401,50", "401,70"]
    assert content_402 == ["402,60"]

def test_divide_downloaded_s_t_file(handler_with_temp_dirs):

    handler = handler_with_temp_dirs
    s_t_file = handler.input_directory / "s_t_test.csv"
    s_t_file.write_text("Station,Value\n501,500\n502,600\n501,700\n", encoding="ISO-8859-2")

    handler.divide_downloaded()

    assert not s_t_file.exists()

    out_file_501 = handler.output_directory / "s_t_station_501.csv"
    out_file_502 = handler.output_directory / "s_t_station_502.csv"
    assert out_file_501.exists()
    assert out_file_502.exists()

    content_501 = out_file_501.read_text(encoding="ISO-8859-2").strip().splitlines()
    content_502 = out_file_502.read_text(encoding="ISO-8859-2").strip().splitlines()
    assert content_501 == ["501,500", "501,700"]
    assert content_502 == ["502,600"]

