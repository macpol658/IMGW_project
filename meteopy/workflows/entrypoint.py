from __future__ import annotations

import click

from meteopy.workflows.basic_summary import basic_summary
from meteopy.workflows.download import download
from meteopy.workflows.full_analysis import full_analysis


@click.group()
def cli() -> None:
    pass

cli.add_command(download)
cli.add_command(basic_summary)
cli.add_command(full_analysis)

if __name__ == "__main__":
    cli()
