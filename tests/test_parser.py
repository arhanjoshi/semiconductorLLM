import unittest
from scraper.semiconductor_scraper import (
    extract_established_date,
    extract_arizona_info,
    find_info_page,
    classify_supply_chain,
)

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - BeautifulSoup may not be available
    BeautifulSoup = None



class TestParsers(unittest.TestCase):
    def test_extract_established_date(self):
        text = "Acme Semiconductor was Founded in 1999 and is headquartered in Arizona."
        self.assertEqual(extract_established_date(text), "1999")

    def test_extract_arizona_info(self):
        text = "Acme Semiconductor operates a fab in Chandler, Arizona. The facility opened in 2010."
        self.assertIn("Arizona", extract_arizona_info(text))

    @unittest.skipIf(BeautifulSoup is None, "BeautifulSoup not installed")
    def test_find_info_page(self):
        html = "<html><body><a href='/about-us'>About Us</a><a href='/other'>Other</a></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        self.assertEqual(
            find_info_page("https://example.com", soup),
            "https://example.com/about-us",
        )

    def test_classify_supply_chain(self):
        text = "Our company operates a leading foundry providing advanced fabs."
        self.assertEqual(classify_supply_chain(text), "Foundry")


if __name__ == "__main__":
    unittest.main()
