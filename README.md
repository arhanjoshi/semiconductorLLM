# semiconductorLLM

This project provides a simple scraper for collecting information about semiconductor companies. The scraper reads a CSV file containing company websites and optional metadata, fetches each site, and attempts to extract:

- Company name
- Established date
- Sentences mentioning Arizona
- Company description
- Classification in the semiconductor supply chain

The scraping logic uses `requests` and `BeautifulSoup` with heuristic text searches. Results are written to a new CSV file.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Prepare an input CSV with at least a `url` column. See `sample_companies.csv` for an example.

3. Run the scraper:

```bash
python -m scraper.semiconductor_scraper sample_companies.csv output.csv
```

The output CSV will contain the extracted fields for each company.

## Tests

Basic parser tests can be run with:

```bash
python -m unittest discover tests
```
