from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from meteopy.utils.logging import get_logger

logger = get_logger(__name__)

class IMGWDataVisualizer:
    def __init__(self, start_date: str, end_date: str, data_type: str, station_ids: list) -> None:
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.data_path = Path(__file__).resolve().parent.parent / "data" / "separated"
        self.data_type = data_type
        self.station_IDs = station_ids

        self.timeseries_plot()

    def timeseries_plot(self) -> None:
        plt.figure(figsize=(10, 5))

        for stationID in self.station_IDs:
            df = self.load_data(stationID)
            if df is not None:
                plt.plot(df.index, df[self.data_type], label=f"Stacja {stationID}")

        plt.xlabel("Data")
        plt.ylabel(self.get_ylabel())
        plt.title(self.get_title())
        plt.legend()
        plt.grid(True)
        plt.show()

    def load_data(self, stationID: str) -> pd.DataFrame:
        file_mapping = {
            "SMDB": f"o_station_{stationID}.csv",
            "PKSN": f"o_station_{stationID}.csv",
            "HSS": f"o_station_{stationID}.csv",
            "TMAX": f"k_station_{stationID}.csv",
            "TMIN": f"k_station_{stationID}.csv",
            "TAVG": f"k_station_{stationID}.csv",
            "WLGS": f"k_t_station_{stationID}.csv",
            "FWS": f"k_t_station_{stationID}.csv",
            "NOS": f"k_t_station_{stationID}.csv",
            "USL": f"s_station_{stationID}.csv",
            "DESZ": f"s_station_{stationID}.csv",
            "MGLA": f"s_station_{stationID}.csv",
            "SADZ": f"s_station_{stationID}.csv"
        }

        if self.data_type not in file_mapping:
            logger.warning(f"Nieznany typ danych: {self.data_type}")
            return None

        path = os.path.join(self.data_path, file_mapping[self.data_type])
        try:
            df = pd.read_csv(path, sep=",", encoding="ISO-8859-2")
            column_mapping = {
                "SMDB": 5, "PKSN": 8, "HSS": 10, "TMAX": 5, "TMIN": 7, "TAVG": 9,
                "WLGS": 7, "FWS": 7, "NOS": 9, "USL": 20, "DESZ": 22, "MGLA": 30, "SADZ": 24
            }
            df = df.iloc[:, [2, 3, 4, column_mapping[self.data_type]]]
            df.columns = ["Year", "Month", "Day", self.data_type]
            df = self.date_processing(df)
            df[self.data_type] = pd.to_numeric(df[self.data_type])
            return df
        except FileNotFoundError:
            logger.warning(f"Nie znaleziono pliku: {path}")
            return None

    def date_processing(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
        df = df.drop(columns=["Year", "Month", "Day"])
        df = df[(df["Date"] >= self.start_date) & (df["Date"] <= self.end_date)].reset_index(drop=True)
        df = df.set_index("Date")
        return df

    def get_ylabel(self) -> str:
        units = {
            "SMDB": "[mm]", "PKSN": "[cm]", "HSS": "[cm]", "TMAX": "[°C]", "TMIN": "[°C]", "TAVG": "[°C]",
            "WLGS": "[%]", "FWS": "[m/s]", "NOS": "[oktanty]", "USL": "[godziny]", "DESZ": "[godziny]",
            "MGLA": "[godziny]", "SADZ": "[godziny]"
        }
        return f"{self.data_type} {units.get(self.data_type, '')}"

    def get_title(self) -> str:
        titles = {
            "SMDB": "Suma dobowa opadów",
            "PKSN": "Wysokość pokrywy śnieżnej",
            "HSS": "Wysokość świeżospadłego śniegu",
            "TMAX": "Maksymalna temperatura dobowa",
            "TMIN": "Minimalna temperatura dobowa",
            "TAVG": "Średnia temperatura dobowa",
            "WLGS": "Średnia dobowa wilgotność względna",
            "FWS": "Średnia prędkość wiatru",
            "NOS": "Średnie zachmurzenie",
            "USL": "Średnie dobowe usłonecznienie",
            "DESZ": "Średni czas trwania deszczu",
            "MGLA": "Średni czas trwania mgły",
            "SADZ": "Średni czas trwania sadzi"
        }
        return f"{titles.get(self.data_type, self.data_type)} w wybranym okresie"


