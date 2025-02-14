from __future__ import annotations

import pandas as pd
import pytest

from meteopy.statistics.imgw_statistics import IMGWStatistics


@pytest.fixture
def test_env(tmp_path):

    data_separated = tmp_path / "data" / "separated"
    data_separated.mkdir(parents=True, exist_ok=True)
    output_dir = tmp_path / "data" / "statistics"
    output_dir.mkdir(parents=True, exist_ok=True)


    smdb_file = data_separated / "o_station_test.csv"
    smdb_file.write_text(
        "A,B,Year,Month,Day,SMDB\n"
        "x,y,2020,1,1,100\n"
        "x,y,2020,1,2,101\n"
    )

    k_file = data_separated / "k_station_test.csv"
    k_file.write_text(
        "col0,col1,Year,Month,Day,TMAX,TMP,TMIN,extra\n"
        "a,b,2020,1,1,30,xxx,10,ignore\n"
        "a,b,2020,1,2,31,xxx,11,ignore\n"
        "a,b,2020,1,3,32,xxx,12,ignore\n"
    )

    stats = IMGWStatistics(data_type="SMDB", station_ids=["test"])

    stats.data_path = data_separated
    stats.output_path = output_dir

    stats.date_processing = lambda df: df.assign(Date=pd.to_datetime(df[["Year", "Month", "Day"]]))
    return stats, tmp_path


def test_load_data_smdb(test_env):
    stats, _ = test_env
    df = stats.load_data("test", "SMDB")
    assert df is not None
    assert set(df.columns) >= {"Year", "Month", "Day", "SMDB", "Date"}
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])
    assert pd.api.types.is_numeric_dtype(df["SMDB"])
    assert len(df) == 2


def test_load_data_tmax(test_env):
    stats, _ = test_env
    df = stats.load_data("test", "TMAX")
    assert df is not None
    assert set(df.columns) >= {"Year", "Month", "Day", "TMAX", "Date"}
    assert pd.api.types.is_numeric_dtype(df["TMAX"])
    assert len(df) == 3


def test_correlate_stations(test_env):
    stats, _ = test_env
    stats.correlate_stations("TMAX", "TMIN")
    corr_file = stats.output_path / "correlations.csv"
    assert corr_file.exists()
    content = corr_file.read_text(encoding="utf-8")
    lines = content.strip().splitlines()
    assert len(lines) == 2
    header = lines[0]
    assert header == "Stacja,Typ danych 1,Typ danych 2,Korelacja"
    data_line = lines[1]
    parts = data_line.split(",")
    assert parts[0] == "test"
    corr_val = float(parts[3])
    assert abs(corr_val - 1.0) < 1e-6


def test_describe_stations(test_env):
    stats, _ = test_env
    stats.describe_stations()
    basic_file = stats.output_path / "basic_stats.csv"
    assert basic_file.exists()
    content = basic_file.read_text(encoding="utf-8")
    lines = content.strip().splitlines()
    assert len(lines) == 1 + 8
    assert lines[0] == "Stacja,Typ danych,Statystyka,Wartosc"
    for line in lines[1:]:
        assert line.startswith("test,SMDB")


def test_date_processing():
    df = pd.DataFrame({
        "Year": [2020, 2020],
        "Month": [1, 2],
        "Day": [15, 16],
        "Value": [10, 20]
    })
    stats = IMGWStatistics(data_type="Value", station_ids=["dummy"])
    df_processed = stats.date_processing(df.copy())
    assert "Value" in df_processed.columns
    assert "Date" not in df_processed.columns
    assert isinstance(df_processed.index, pd.DatetimeIndex)
    assert df_processed.index[0] == pd.Timestamp("2020-01-15")
