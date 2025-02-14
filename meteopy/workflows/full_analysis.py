from __future__ import annotations

import click

from meteopy.eda.imgw_eda_visualizer import IMGWDataVisualizer
from meteopy.forecasting.imgw_simple_forecaster import IMGWSimpleForecaster
from meteopy.statistics.imgw_statistics import IMGWStatistics


@click.command(name="full_analysis")
@click.argument("arguments",nargs=-1)
@click.option("-s","--start-day",type=str,help="Dzien poczatkowy dla wykresu w formacie YYYY-MM-DD")
@click.option("-e","--end-day",type=str,help="Dzien koncowy dla wykresu w formacie YYYY-MM-DD")
@click.option("-c","--correlation",is_flag=True,help="Obliczyć korelację pomiędzy dwoma statystykami "
"(jeżeli podanych jest więcej korelacja zostanie obliczona dla pierwszych dwoch)")
@click.option("-fd","--future-days",default=15,type=int,help="Liczba dni, dla ktorych zostanie wykonana prognoza")
def full_analysis(arguments,start_day:str,end_day:str,correlation:bool,future_days:int) -> None:

    """Dostepne typy danych: SMDB (suma dobowa opadow), PKSN (wysokosc pokrywy snieznej), HSS (wysokosc swiezospadlego sniegu),
    TMAX (maksymalna temperatura dobowa), TMIN (minimalna -||-), TAVG (srenida -||-), WLGS (srednia dobowa wilgotnosc wzgledna),
     FWS (srednia predkosc wiatru), NOS (srednie zachmurzenie),USL (srednie dobowe uslonecznienie),
     DESZ (sredni czas trwania deszczu), MGLA (sredni czas trwania mgly), SADZ(sredni czas trwania szadzi) \n
    przyklad uzycia: full_analysis WLGS NOS MGLA TMIN station_id1 station_id2 station_id3 -s 1999-10-11 -e 2001-09-08 -c -fd 30
    """
    data_type = [arg for arg in arguments if arg.isalpha()]
    station_id = [arg for arg in arguments if arg.isdigit()]

    for dtype in data_type:
        stats=IMGWStatistics(dtype,station_id)
        stats.describe_stations()
    if correlation and len(data_type) >= 2:
            stats=IMGWStatistics("",station_id)
            stats.correlate_datas(data_type[0],data_type[1])
    if start_day and end_day:
        for data in data_type:
            IMGWDataVisualizer(start_day,end_day,data,station_id)
    for data in data_type:
        for station in station_id:
            IMGWSimpleForecaster(data,station,future_days)
