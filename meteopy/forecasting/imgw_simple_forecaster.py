from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from meteopy.utils.logging import get_logger

logger = get_logger(__name__)

class IMGWSimpleForecaster:
    def __init__(self, data_type: str, station_id: str, future_days: int) -> None:
        self.data_path = Path(__file__).resolve().parent.parent / "data" / "separated"
        self.station_id = station_id
        self.future_days = future_days
        self.data_type = data_type

        self.linear_regression_forecast()

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

        path = self.data_path / file_mapping[data_type]
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


    def linear_regression_forecast(self) -> None:
        df = self.load_data(self.station_id, self.data_type)
        if df is None or df.empty:
            logger.warning(f"Brak danych dla stacji {self.station_id}.")
            return

        df = df.dropna()
        df["Days"] = (df.index - df.index.min()).days
        X = df[["Days"]].values
        y = df[self.data_type].values

        split_index = int(len(df) * 0.8)
        X_train, X_test = X[:split_index], X[split_index:]
        y_train, y_test = y[:split_index], y[split_index:]

        model = LinearRegression()
        model.fit(X_train, y_train)

        all_X = np.array([i for i in range(len(df) + self.future_days)]).reshape(-1, 1)
        all_y_pred = model.predict(all_X)

        historical_pred = all_y_pred[:len(df)]
        future_pred = all_y_pred[len(df):]

        future_dates = pd.date_range(start=df.index.max(), periods=self.future_days + 1, freq="D")[1:]
        future_df = pd.DataFrame({self.data_type: future_pred}, index=future_dates)

        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df[self.data_type], label="Rzeczywiste dane", color="blue")
        plt.plot(df.index, historical_pred, label="Linia regresji", color="green", linestyle="dashed")
        plt.plot(future_df.index, future_df[self.data_type], label="Prognoza", color="red", linestyle="dashed")
        plt.xlabel("Data")
        plt.ylabel(self.data_type)
        plt.title(f"Prognoza dla stacji {self.station_id} ({self.data_type})")
        plt.legend()
        plt.grid()
        plt.show()
