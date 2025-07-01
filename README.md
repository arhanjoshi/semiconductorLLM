# semiconductorLLM

This project provides a simple scraper for collecting information about semiconductor companies. The scraper reads a CSV file containing company websites and optional metadata, fetches each site, and attempts to extract:

- Company name
- Established date
- Sentences mentioning Arizona
- Company description
- Classification in the semiconductor supply chain

The helper `classify_supply_chain` assigns roles such as Foundry, IDM, or
Equipment based on keywords it finds in the page text.

The scraper shows progress with a `tqdm` progress bar and retries failed HTTP
requests with exponential backoff.

The scraping logic uses Python's standard library and `BeautifulSoup` with heuristic text searches. If key details are missing from the home page, the scraper looks for an "About" or "History" link and scrapes that page as well. Results are written to a new CSV file.

The scraping logic uses `requests` and `BeautifulSoup` with heuristic text searches. Results are written to a new CSV file.


## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Prepare an input CSV describing each company. The scraper understands the
   extended format with columns like `Company Name`, `Ticker`, `URL`, and
   `Description`. See `sample_companies_extended.csv` for an example. Legacy
   files with a simple `url` column are also supported.

3. Run the scraper from the project root. For example, to scrape the
   provided `D&BSemiList_ArhanJoshi_Edited.csv` file:

```bash
python scraper/semiconductor_scraper.py "D&BSemiList_ArhanJoshi_Edited.csv" output_full.csv
3. Run the scraper:

```bash
python -m scraper.semiconductor_scraper sample_companies_extended.csv output.csv
```

The output CSV will contain the extracted fields for each company.

## Tests

Basic parser tests can be run with:

```bash
python -m unittest discover tests
```
