import requests
from bs4 import BeautifulSoup
import pandas as pd
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CompanyInfo:
    name: str
    website: str
    title: Optional[str] = None
    description: Optional[str] = None


class CompanyScraper:
    """Simple scraper to extract company information from a list of URLs."""

    def __init__(self, csv_path: str):
        self.companies_df = pd.read_csv(csv_path)

    def fetch_html(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

    @staticmethod
    def parse_html(html: str) -> CompanyInfo:
        """Parse raw HTML and return title and description."""
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title else None
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'].strip() if description_tag else None
        return title, description

    def scrape(self) -> List[CompanyInfo]:
        results: List[CompanyInfo] = []
        for _, row in self.companies_df.iterrows():
            name = row.get('name')
            website = row.get('website')
            html = self.fetch_html(website)
            if html:
                title, description = self.parse_html(html)
                results.append(CompanyInfo(name=name, website=website,
                                           title=title, description=description))
            else:
                results.append(CompanyInfo(name=name, website=website))
        return results


if __name__ == "__main__":
    scraper = CompanyScraper("data/example_companies.csv")
    results = scraper.scrape()
    for company in results:
        print(company)
