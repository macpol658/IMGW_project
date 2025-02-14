from __future__ import annotations

import click

from meteopy.statistics.imgw_statistics import IMGWStatistics


@click.command(name="basic_summary")
@click.argument("data_type",type=str)
@click.argument("station_ids",nargs=-1)
def basic_summary(data_type:str,station_ids:tuple) -> None:

    """Dostepne typy danych: SMDB (suma dobowa opadow), PKSN (wysokosc pokrywy snieznej), HSS (wysokosc swiezospadlego sniegu),
    TMAX (maksymalna temperatura dobowa), TMIN (minimalna -||-), TAVG (srenida -||-), WLGS (srednia dobowa wilgotnosc wzgledna),
     FWS (srednia predkosc wiatru), NOS (srednie zachmurzenie),USL (srednie dobowe uslonecznienie),
     DESZ (sredni czas trwania deszczu), MGLA (sredni czas trwania mgly), SADZ(sredni czas trwania szadzi)\n
    przyklad uzycia: basic_summary SMDB station_id1 station_id2 station_id3
    """
    station_ids=list(station_ids)
    stats=IMGWStatistics(data_type,station_ids)
    stats.describe_stations()
