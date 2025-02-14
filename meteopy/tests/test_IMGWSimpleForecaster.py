from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from meteopy.forecasting.imgw_simple_forecaster import IMGWSimpleForecaster


def create_dummy_csv(csv_path: Path, n: int = 10, start_day: int = 1, start_value: int = 10, increment: int = 1):

    lines = ["col0,col1,Year,Month,Day,TMAX"]
    for i in range(n):
        day = start_day + i
        value = start_value + i * increment
        lines.append(f"a,b,2020,1,{day},{value}")
    csv_content = "\n".join(lines)
    csv_path.write_text(csv_content, encoding="ISO-8859-2")

def test_linear_regression_forecast(monkeypatch, tmp_path):

    sep_dir = tmp_path / "separated"
    sep_dir.mkdir()

    csv_file = sep_dir / "k_station_test.csv"
    create_dummy_csv(csv_file, n=10, start_day=1, start_value=10, increment=1)

    show_called = False
    def fake_show():
        nonlocal show_called
        show_called = True
    monkeypatch.setattr(plt, "show", fake_show)

    plot_calls = []
    def fake_plot(x, y, label=None, *args, **kwargs):
        plot_calls.append(label)
    monkeypatch.setattr(plt, "plot", fake_plot)

    forecaster = IMGWSimpleForecaster.__new__(IMGWSimpleForecaster)
    forecaster.data_type = "TMAX"
    forecaster.station_id = "test"
    forecaster.future_days = 5
    forecaster.data_path = sep_dir

    forecaster.linear_regression_forecast()

    assert "Rzeczywiste dane" in plot_calls, f"Plot calls: {plot_calls}"
    assert "Linia regresji" in plot_calls, f"Plot calls: {plot_calls}"
    assert "Prognoza" in plot_calls, f"Plot calls: {plot_calls}"
    assert len(plot_calls) == 3

    assert show_called

def test_linear_regression_forecast_no_data(monkeypatch, tmp_path, caplog):

    sep_dir = tmp_path / "separated"
    sep_dir.mkdir()

    monkeypatch.setattr(plt, "show", lambda: None)

    IMGWSimpleForecaster(data_type="TMAX", station_id="nonexistent", future_days=5)

    assert "Nie znaleziono pliku" in caplog.text

def test_load_data_and_date_processing(monkeypatch, tmp_path):

    sep_dir = tmp_path / "separated"
    sep_dir.mkdir()

    csv_file = sep_dir / "k_station_test.csv"
    create_dummy_csv(csv_file, n=5, start_day=10, start_value=15, increment=2)

    forecaster = IMGWSimpleForecaster.__new__(IMGWSimpleForecaster)
    forecaster.data_path = sep_dir
    forecaster.data_type = "TMAX"

    df = forecaster.load_data("test", "TMAX")
    assert df is not None
    assert isinstance(df.index, pd.DatetimeIndex)
    assert "TMAX" in df.columns
    assert pd.api.types.is_numeric_dtype(df["TMAX"])
    assert len(df) == 5
