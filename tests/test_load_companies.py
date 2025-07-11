import unittest
import tempfile
import csv
from scraper.semiconductor_scraper import SemiconductorScraper


class TestLoadCompanies(unittest.TestCase):
    def test_load_extended_csv(self):
        rows = [
            {
                "Company Name": "Test Corp",
                "Ticker": "TST",
                "URL": "http://example.com",
            }
        ]
        with tempfile.NamedTemporaryFile("w", newline="", delete=False) as tmp:
            writer = csv.DictWriter(tmp, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
            tmp_name = tmp.name

        scraper = SemiconductorScraper(tmp_name)
        scraper.load_companies()
        self.assertEqual(len(scraper.companies), 1)
        company = scraper.companies[0]
        self.assertEqual(company.company_name, "Test Corp")
        self.assertEqual(company.ticker, "TST")
        self.assertEqual(company.url, "http://example.com")

    def test_adds_scheme_to_url(self):
        rows = [
            {
                "Company Name": "No Scheme Inc",
                "URL": "example.org",
            }
        ]
        with tempfile.NamedTemporaryFile("w", newline="", delete=False) as tmp:
            writer = csv.DictWriter(tmp, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
            tmp_name = tmp.name

        scraper = SemiconductorScraper(tmp_name)
        scraper.load_companies()
        self.assertEqual(len(scraper.companies), 1)
        company = scraper.companies[0]
        self.assertEqual(company.url, "https://example.org")

    def test_tab_delimited(self):
        rows = [
            {
                "Company Name": "Tabbed Co",
                "URL": "tabbed.com",
            }
        ]
        with tempfile.NamedTemporaryFile("w", newline="", delete=False) as tmp:
            writer = csv.DictWriter(tmp, fieldnames=rows[0].keys(), delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
            tmp_name = tmp.name

        scraper = SemiconductorScraper(tmp_name)
        scraper.load_companies()
        self.assertEqual(len(scraper.companies), 1)
        self.assertEqual(scraper.companies[0].url, "https://tabbed.com")


if __name__ == "__main__":
    unittest.main()
