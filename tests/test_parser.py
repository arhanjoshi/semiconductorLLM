import unittest
from scraper.semiconductor_scraper import extract_established_date, extract_arizona_info


class TestParsers(unittest.TestCase):
    def test_extract_established_date(self):
        text = "Acme Semiconductor was Founded in 1999 and is headquartered in Arizona."
        self.assertEqual(extract_established_date(text), "1999")

    def test_extract_arizona_info(self):
        text = "Acme Semiconductor operates a fab in Chandler, Arizona. The facility opened in 2010."
        self.assertIn("Arizona", extract_arizona_info(text))


if __name__ == "__main__":
    unittest.main()
