import unittest
from src import scraper

class TestScraper(unittest.TestCase):
    def test_parse_html(self):
        html = """
        <html><head><title>Example</title><meta name=\"description\" content=\"Test company description\"></head><body></body></html>
        """
        title, desc = scraper.CompanyScraper.parse_html(html)
        self.assertEqual(title, "Example")
        self.assertEqual(desc, "Test company description")

if __name__ == "__main__":
    unittest.main()
