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
requests with exponential backoff. When loading company data, any URL that lacks
an explicit scheme is automatically prefixed with `https://` so that pages can be
fetched correctly.

The scraping logic uses Python's standard library and `BeautifulSoup` with heuristic text searches. If key details are missing from the home page, the scraper looks for an "About" or "History" link and scrapes that page as well. Results are written to a new CSV file.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Prepare an input CSV describing each company. The scraper understands the
   extended format with columns like `Company Name`, `Ticker`, `URL`, and
   `Description`. Delimiters of either commas or tabs are detected
   automatically, so the file may use either style. See
   `sample_companies_extended.csv` for an example. Legacy files with a simple
   `url` column are also supported.

   The scraper fetches live HTML from the listed websites, so make sure the
   environment has network access. If run without internet connectivity, each
   request will log warnings and no data will be extracted.


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

## Sanity check

To verify that network access works and `fetch_page` returns HTML, run:

```bash
python sanity_check.py
```

This script fetches a sample page and prints the first few characters of HTML.
