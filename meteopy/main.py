from __future__ import annotations

from consts.dirs import Dirs
from meteopy.data_fetchers.imgw_fetcher import IMGWDataFetcher
from meteopy.eda.imgw_eda_visualizer import IMGWDataVisualizer
from meteopy.forecasting.imgw_simple_forecaster import IMGWSimpleForecaster
from meteopy.preprocessing.imgw_handler import IMGWDataHandler
from meteopy.statistics.imgw_statistics import IMGWStatistics


def main():

    directories = Dirs()
    directories.create_dirs()
    #IMGWDataFetcher("klimat", 2000, 2000)
    #IMGWDataFetcher("opad", 2000, 2000)
    #IMGWDataFetcher("synop", 2001, 2001)
    #IMGWDataHandler()
    #IMGWDataVisualizer("2000-02-03", "2000-12-13", "FWS", ["249210070","249220150","249200320","249200470"])
    #IMGWDataVisualizer("2000-02-03", "2000-12-13", "NOS", ["249210070", "249220150", "249200320", "249200470"])
    #stats = IMGWStatistics("TAVG", ["249180010", "249180020","249200240","249200320"])
    #stats.describe_stations()
    #stats = IMGWStatistics("", ["354220195"])
    #stats.correlate_datas("DESZ", "USL")
    #IMGWSimpleForecaster("SMDB", "251160040", 60)
    #IMGWSimpleForecaster("WLGS", "250170390", 60)

if __name__ == "__main__":
    main()
