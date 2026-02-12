**IMGW project** made as a part of a **Python course**.  
It contains elements such as:

- **web-scraping**
- **file handling**
- **data visualization**
- **basic statistics**
- **basic forecasting**

The project includes its own **CLI**, as well as **tests and logs**.

There were **13 variables** selected from the **IMGW dataset**.

---

## CLI Usage Examples

```bash
python -m meteopy.workflows.entrypoint download klimat 2000 2001
python -m meteopy.workflows.entrypoint download opad 2000 2001
python -m meteopy.workflows.entrypoint basic_summary TAVG 249180010 24918160 249200240
python -m meteopy.workflows.entrypoint full_analysis DESZ USL 354220195 354210185 -s 2001-01-03 -e 2001-12-20 -c -fd 30
```

---

## Help

To display a description of every command and its parameters, use:

```bash
python -m meteopy.workflows.entrypoint download --help
python -m meteopy.workflows.entrypoint basic_summary --help
python -m meteopy.workflows.entrypoint full_analysis --help
