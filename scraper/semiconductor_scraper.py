import csv
import re
from dataclasses import dataclass, asdict
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


def fetch_page(url: str) -> Optional[str]:
    """Fetch a page and return HTML content."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def extract_established_date(text: str) -> Optional[str]:
    """Attempt to extract the established date from text."""
    # Look for patterns like 'Founded in 1998' or 'Established: 2001'
    match = re.search(r"(Founded|Established)[^\d]*(\d{4})", text, re.IGNORECASE)
    if match:
        return match.group(2)
    year_match = re.search(r"\b(19|20)\d{2}\b", text)
    if year_match:
        return year_match.group(0)
    return None


def extract_arizona_info(text: str) -> Optional[str]:
    """Look for sentences mentioning Arizona."""
    sentences = re.split(r"(?<=[.!?]) +", text)
    arizona_sentences = [s for s in sentences if "arizona" in s.lower() or "az" in s.lower()]
    if arizona_sentences:
        return " ".join(arizona_sentences)
    return None


def extract_description(soup: BeautifulSoup) -> Optional[str]:
    """Get meta description or first paragraph."""
    meta = soup.find("meta", {"name": "description"})
    if meta and meta.get("content"):
        return meta["content"].strip()
    p = soup.find("p")
    if p:
        return p.get_text(strip=True)
    return None


@dataclass
class CompanyInfo:
    url: str
    name: Optional[str] = None
    established: Optional[str] = None
    arizona_info: Optional[str] = None
    description: Optional[str] = None
    classification: Optional[str] = None


class SemiconductorScraper:
    def __init__(self, input_csv: str):
        self.input_csv = input_csv
        self.companies: List[CompanyInfo] = []

    def load_companies(self):
        """Load companies from a CSV file."""
        with open(self.input_csv, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.companies.append(
                    CompanyInfo(
                        url=row.get("url", "").strip(),
                        name=row.get("name"),
                        classification=row.get("classification"),
                    )
                )

    def scrape(self):
        """Scrape all company websites."""
        for company in self.companies:
            html = fetch_page(company.url)
            if not html:
                continue
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(" ", strip=True)
            if not company.name:
                company.name = soup.title.string.strip() if soup.title else None
            company.established = extract_established_date(text)
            company.arizona_info = extract_arizona_info(text)
            company.description = extract_description(soup)

    def to_csv(self, output_csv: str):
        """Write scraped data to CSV."""
        fieldnames = [
            "url",
            "name",
            "established",
            "arizona_info",
            "description",
            "classification",
        ]
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company in self.companies:
                writer.writerow(asdict(company))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape semiconductor company data.")
    parser.add_argument("input_csv", help="CSV file with company URLs")
    parser.add_argument("output_csv", help="Output CSV file")
    args = parser.parse_args()

    scraper = SemiconductorScraper(args.input_csv)
    scraper.load_companies()
    scraper.scrape()
    scraper.to_csv(args.output_csv)
