from __future__ import annotations

import click

from meteopy.data_fetchers.imgw_fetcher import IMGWDataFetcher
from meteopy.preprocessing.imgw_handler import IMGWDataHandler


@click.command(name="download")
@click.argument("type",type=str)
@click.argument("starting_year",type=int)
@click.argument("ending_year",type=int)
@click.option("-nu","--no-unzip",is_flag=True,help="nie unzipowac pobranych plikow")
@click.option("-nh","--no-handler",is_flag=True,help="nie uzywac data handlera na pobranych plikach")
@click.option("-nd","--no-delete",is_flag=True,help="aby podczas uzycia handlera nie usuwac rozdzielonych plikow")
def download(type:str,starting_year:int,ending_year:int,no_unzip:bool,no_handler:bool,no_delete:bool) -> None:

    """Dostepne typy danych do pobrania: klimat, opad, synop \n
    przyklad uzycia: download klimat 2005 2010
    """
    unzip=not no_unzip
    handler=not no_handler
    delete=not no_delete
    IMGWDataFetcher(type,starting_year,ending_year,unzip)
    if handler:
        IMGWDataHandler(delete)

