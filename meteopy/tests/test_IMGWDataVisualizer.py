from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from meteopy.eda.imgw_eda_visualizer import IMGWDataVisualizer


def test_load_data(monkeypatch, tmp_path):

    monkeypatch.setattr(IMGWDataVisualizer, "timeseries_plot", lambda self: None)

    vis = IMGWDataVisualizer(
        start_date="2020-01-01",
        end_date="2020-12-31",
        data_type="TMAX",
        station_ids=["test"]
    )
    sep_dir = tmp_path / "separated"
    sep_dir.mkdir()
    vis.data_path = sep_dir

    csv_content = (
        "col0,col1,Year,Month,Day,TMAX,extra\n"
        "a,b,2020,1,15,25,x\n"
        "a,b,2020,1,16,26,x\n"
    )
    csv_file = sep_dir / "k_station_test.csv"
    csv_file.write_text(csv_content, encoding="ISO-8859-2")

    df = vis.load_data("test")
    assert df is not None
    assert isinstance(df.index, pd.DatetimeIndex)
    assert pd.api.types.is_numeric_dtype(df["TMAX"])
    assert len(df) == 2
    assert df["TMAX"].iloc[0] == 25
    assert df["TMAX"].iloc[1] == 26


def test_get_ylabel_and_title(monkeypatch):

    monkeypatch.setattr(IMGWDataVisualizer, "timeseries_plot", lambda self: None)

    vis = IMGWDataVisualizer(
        start_date="2020-01-01",
        end_date="2020-01-31",
        data_type="TMAX",
        station_ids=[]
    )
    ylabel = vis.get_ylabel()
    title = vis.get_title()

    assert ylabel == "TMAX [°C]"
    assert title == "Maksymalna temperatura dobowa w wybranym okresie"

def test_timeseries_plot(monkeypatch):

    dummy_df = pd.DataFrame({
        "TMAX": [25, 26]
    }, index=pd.to_datetime(["2020-01-15", "2020-01-16"]))

    def fake_load_data(self, station_id):
        return dummy_df

    monkeypatch.setattr(IMGWDataVisualizer, "load_data", fake_load_data)

    plot_calls = []

    def fake_plot(x, y, label, *args, **kwargs):
        plot_calls.append(label)

    monkeypatch.setattr(plt, "plot", fake_plot)
    monkeypatch.setattr(plt, "show", lambda: None)

    vis = IMGWDataVisualizer(
        start_date="2020-01-01",
        end_date="2020-12-31",
        data_type="TMAX",
        station_ids=["1", "2"]
    )

    assert "Stacja 1" in plot_calls
    assert "Stacja 2" in plot_calls
    assert len(plot_calls) == 2


def test_timeseries_plot_with_missing_data(monkeypatch):

    dummy_df = pd.DataFrame({
        "TMAX": [25, 26]
    }, index=pd.to_datetime(["2020-01-15", "2020-01-16"]))

    def fake_load_data(self, station_id):
        return dummy_df if station_id == "1" else None

    monkeypatch.setattr(IMGWDataVisualizer, "load_data", fake_load_data)

    plot_calls = []

    def fake_plot(x, y, label, *args, **kwargs):
        plot_calls.append(label)

    monkeypatch.setattr(plt, "plot", fake_plot)
    monkeypatch.setattr(plt, "show", lambda: None)

    vis = IMGWDataVisualizer(
        start_date="2020-01-01",
        end_date="2020-12-31",
        data_type="TMAX",
        station_ids=["1", "2"]
    )

    assert "Stacja 1" in plot_calls
    assert "Stacja 2" not in plot_calls
    assert len(plot_calls) == 1
