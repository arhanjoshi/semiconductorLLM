# semiconductorLLM

Tools for collecting publicly available data on semiconductor companies
operating in Arizona. The project is written in Python and uses
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to parse HTML.

## Project layout

- `src/` – scraping logic
- `data/` – example input files (CSV, spreadsheets)
- `tests/` – unit tests

## Getting started

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Place a CSV listing company names and their websites in `data/`.
   A sample file is provided at `data/example_companies.csv`.

3. Run the scraper:

   ```bash
   python src/scraper.py
   ```

   This prints basic information scraped from each website such as the page
   title and meta description. Stage 1 focuses on gathering this raw data.

## Version control

This repository uses [Git](https://git-scm.com/) for version control. Keep
commits small and descriptive. Ignore Python bytecode and virtual environment
directories using `.gitignore`.

## Next steps

- Expand the parser to extract details like company location or key dates.
- Use the data to power downstream applications (Stage 2).
- Consider additional libraries (e.g., [Scopus](https://www.elsevier.com/solutions/scopus))
  if research publications are relevant.
