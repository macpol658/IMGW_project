from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from meteopy.utils.logging import get_logger

logger = get_logger(__name__)

class IMGWStatistics:
    def __init__(self, data_type: str, station_ids: list) -> None:
        self.data_path = Path(__file__).resolve().parent.parent / "data" / "separated"
        self.data_type = data_type
        self.station_IDs = station_ids
        self.output_path = Path(__file__).resolve().parent.parent / "data" / "statistics"
        self.output_path.mkdir(parents=True, exist_ok=True)

    def load_data(self, stationID: str, data_type: str) -> pd.DataFrame:
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

        column_mapping = {
            "SMDB": 5, "PKSN": 8, "HSS": 10, "TMAX": 5, "TMIN": 7, "TAVG": 9,
            "WLGS": 7, "FWS": 7, "NOS": 9, "USL": 20, "DESZ": 22, "MGLA": 30, "SADZ": 24
        }

        if data_type not in file_mapping:
            logger.warning(f"Nieznany typ danych: {data_type}")
            return None

        path = os.path.join(self.data_path, file_mapping[data_type])
        try:
            df = pd.read_csv(path, sep=",", encoding="ISO-8859-2")
            df = df.iloc[:, [2, 3, 4, column_mapping[data_type]]]
            df.columns = ["Year", "Month", "Day", data_type]
            df = self.date_processing(df)
            df[data_type] = pd.to_numeric(df[data_type], errors="coerce")
            return df
        except FileNotFoundError:
            logger.error(f"Nie znaleziono pliku: {path}")
            return None

    def date_processing(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
        df = df.drop(columns=["Year", "Month", "Day"])
        df = df.set_index("Date")
        return df

    def describe_stations(self) -> None:
        output_file = self.output_path / "basic_stats.csv"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Stacja,Typ danych,Statystyka,Wartosc\n")

            for station in self.station_IDs:
                df = self.load_data(station, self.data_type)
                if df is not None:
                    stats = df.describe().round(2)
                    for stat in stats.index:
                        f.write(f"{station},{self.data_type},{stat},{stats.loc[stat].values[0]}\n")
                logger.info(f"Statystyki {self.data_type} dla stacji {station} zapisano do {output_file}")



    def correlate_datas(self, data_type_1: str, data_type_2: str) -> None:
        output_file = self.output_path / "correlations.csv"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Stacja,Typ danych 1,Typ danych 2,Korelacja\n")

            for station in self.station_IDs:
                df1 = self.load_data(station, data_type_1)
                df2 = self.load_data(station, data_type_2)

                if df1 is not None and df2 is not None:
                    merged_df = df1.merge(df2, on="Date", how="inner")
                    corr_matrix = merged_df[[data_type_1, data_type_2]].corr(method="pearson").round(2)
                    corr_value = corr_matrix.loc[data_type_1, data_type_2]
                    f.write(f"{station},{data_type_1},{data_type_2},{corr_value}\n")

            logger.info(f"Korelacja {data_type_1} do {data_type_2} dla {station} zapisano do {output_file}")





