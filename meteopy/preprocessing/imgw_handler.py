from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from meteopy.utils.logging import get_logger

logger = get_logger(__name__)

class IMGWDataHandler:
    def __init__(self,delete : bool = True) -> None:
        self.output_directory = Path(__file__).resolve().parent.parent / "data" / "separated"
        self.input_directory = Path(__file__).resolve().parent.parent / "data" / "downloaded"
        self.delete = delete
        os.makedirs(self.output_directory, exist_ok=True)

        self.divide_downloaded()

    def divide_downloaded(self) -> None:
        for filename in os.listdir(self.input_directory):
            logger.info(f"dividing file {filename}")
            if filename.endswith(".csv"):
                input_path = os.path.join(self.input_directory, filename)

                data = pd.read_csv(input_path, encoding="ISO-8859-2")

                for station_id, group in data.groupby(data.columns[0]):
                    if filename.startswith("o"):
                        output_path = os.path.join(self.output_directory, f"o_station_{station_id}.csv")
                    elif filename.startswith("k"):
                        if "t" in filename:
                            output_path = os.path.join(self.output_directory, f"k_t_station_{station_id}.csv")
                        else:
                            output_path = os.path.join(self.output_directory, f"k_station_{station_id}.csv")
                    elif filename.startswith("s"):
                        if "t" in filename:
                            output_path = os.path.join(self.output_directory, f"s_t_station_{station_id}.csv")
                        else:
                            output_path = os.path.join(self.output_directory, f"s_station_{station_id}.csv")
                    if os.path.exists(output_path):
                        group.to_csv(output_path, mode="a", index=False, header=False)
                    else:
                        group.to_csv(output_path, mode="w", index=False, header=False)
                if self.delete:
                    os.remove(input_path)
