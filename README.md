IMGW project made as a part of pyton course. It contains elements such as web-scrapping, file handling, data vizualization, basic statistics and basic forecasting.
The project has its own CLI as well as tests and logs.
There were 13 variables to operate on chosen from the IMGW dataset.

An example of using the CLI:
python -m meteopy.workflows.entrypoint download klimat (type of data) 2000 2001 (date range)
python -m meteopy.workflows.entrypoint download opad (type of data) 2000 2001 (date range)
python -m meteopy.workflows.entrypoint basic_summary TAVG (variable) 249180010 24918160 249200240 (station_ids)
python -m meteopy.workflows.entrypoint full_analysis DESZ USL (variables) 354220195 354210185 (station_ids) -s 2001-01-03 (start date) -e 2001-12-20 (end_date) 
-c (to show correlation) -fd 30 (number of forecast days)

The description of every command and its parameters can be shown by typing:
python -m meteopy.workflows.entrypoint download/basic_summary/full_analysis --help
