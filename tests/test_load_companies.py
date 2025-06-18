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


if __name__ == "__main__":
    unittest.main()
