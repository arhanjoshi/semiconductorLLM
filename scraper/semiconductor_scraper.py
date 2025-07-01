import csv
import re
from dataclasses import dataclass
from typing import List, Optional

import time
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover - allow running without tqdm
    def tqdm(iterable, **kwargs):
        return iterable

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - handle missing dependency in tests
    class BeautifulSoup:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError("BeautifulSoup (bs4) is required for HTML parsing")


def fetch_page(url: str, headers: Optional[dict] = None, retries: int = 3) -> Optional[str]:
    """Fetch a page and return HTML content using standard library with retries."""
    delay = 1.0
    for attempt in range(retries):
        try:
            req = Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=10) as resp:
                return resp.read().decode("utf-8", errors="ignore")
        except (HTTPError, URLError, ValueError):
            if attempt == retries - 1:
                return None
            time.sleep(delay)
            delay *= 2
    return None


def extract_established_date(text: str) -> Optional[str]:
    """Attempt to extract the established date from text."""
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


def find_about_or_history_link(soup: BeautifulSoup, company_name: str) -> Optional[str]:
    """Search for an 'About' or 'History' link on the page."""
    link_keywords = ["about", "history"]
    texts = [company_name.lower()] if company_name else []
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        text = a.get_text(" ", strip=True).lower()
        for kw in link_keywords:
            if kw in href or kw in text:
                if kw == "about" and texts and not any(t in text for t in texts):
                    continue
                return a["href"]
    return None


INFO_KEYWORDS = [
    "about", "about-us", "aboutus", "company", "profile", "overview", "corporate",
    "company-info", "company-profile", "company-overview", "who-we-are", "our-story",
    "story", "journey", "legacy", "history", "our-history", "milestones", "timeline",
    "mission", "vision", "values", "fact-sheet", "facts", "at-a-glance",
    "leadership", "management-team", "executives", "investor-relations",
    "ir/company-profile", "sustainability", "csr", "esg"
]

def find_info_page(base_url: str, soup: BeautifulSoup) -> Optional[str]:
    """Return the best candidate 'info' page URL."""
    candidates = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        href_lc = href.lower()
        text_lc = a.get_text(" ", strip=True).lower()
        if any(kw in href_lc for kw in INFO_KEYWORDS):
            score = 0
        elif any(kw in text_lc for kw in INFO_KEYWORDS):
            score = 1
        else:
            continue
        depth = href_lc.count("/")
        candidates.append((score, depth, href))
    if not candidates:
        return None
    candidates.sort(key=lambda t: (t[0], t[1]))
    return urljoin(base_url, candidates[0][2])

def classify_supply_chain(text: str) -> Optional[str]:
    """Identify the company's role in the semiconductor supply chain."""
    mapping = {
        "Foundry": ["foundry", "fab"],
        "IDM": ["integrated device manufacturer", "idm"],
        "EDA": ["electronic design automation", "eda", "cadence", "synopsys"],
        "Equipment": ["lithography", "etch", "deposition", "equipment", "tool"],
        "Materials": ["silicon", "chemicals", "gases", "materials"],
        "Assembly/Test": ["assembly", "test", "packaging"],
        "IP": ["ip cores", "intellectual property"],
    }
    lower = text.lower()
    for role, keywords in mapping.items():
        if any(k in lower for k in keywords):
            return role
    return None

@dataclass
class CompanyInfo:
    company_name: Optional[str] = None
    ticker: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[str] = None
    sales: Optional[str] = None
    sic: Optional[str] = None
    url: str = ""
    phone_number: Optional[str] = None
    description: Optional[str] = None
    established: Optional[str] = None
    arizona_info: Optional[str] = None
    website_description: Optional[str] = None
    classification: Optional[str] = None

class SemiconductorScraper:
    def __init__(self, input_csv: str):
        self.input_csv = input_csv
        self.companies: List[CompanyInfo] = []

    def load_companies(self):
        with open(self.input_csv, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = (row.get("URL") or row.get("Url") or row.get("url") or "").strip()
                if not url:
                    continue
                self.companies.append(
                    CompanyInfo(
                        company_name=row.get("Company Name") or row.get("name"),
                        ticker=row.get("Ticker"),
                        location=row.get("Location"),
                        location_type=row.get("Location Type"),
                        sales=row.get("Sales"),
                        sic=row.get("SIC"),
                        url=url,
                        phone_number=row.get("Phone Number"),
                        description=row.get("Description"),
                    )
                )

    def scrape(self):
        for company in tqdm(self.companies, desc="Scraping companies"):
            html = fetch_page(company.url)
            if not html:
                continue
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(" ", strip=True)

            info_url = find_info_page(company.url, soup)
            if info_url:
                info_html = fetch_page(info_url)
                if info_html:
                    soup = BeautifulSoup(info_html, "html.parser")
                    text = soup.get_text(" ", strip=True)

            if not company.company_name:
                company.company_name = soup.title.string.strip() if soup.title else None
            company.established = extract_established_date(text)
            company.arizona_info = extract_arizona_info(text)
            company.website_description = extract_description(soup)
            company.classification = classify_supply_chain(text)

            if not all([company.established, company.arizona_info, company.website_description]):
                link = find_about_or_history_link(soup, company.company_name or "")
                if link:
                    link = urljoin(company.url, link)
                    about_html = fetch_page(link)
                    if about_html:
                        about_soup = BeautifulSoup(about_html, "html.parser")
                        about_text = about_soup.get_text(" ", strip=True)
                        if not company.established:
                            company.established = extract_established_date(about_text)
                        if not company.arizona_info:
                            company.arizona_info = extract_arizona_info(about_text)
                        if not company.website_description:
                            company.website_description = extract_description(about_soup)
                        if not company.classification:
                            company.classification = classify_supply_chain(about_text)

    def to_csv(self, output_csv: str):
        fieldnames = [
            "Company Name", "Ticker", "Location", "Location Type", "Sales", "SIC", "URL",
            "Phone Number", "Description", "Established", "Arizona Info", "Website Description",
            "Classification",
        ]
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company in self.companies:
                writer.writerow({
                    "Company Name": company.company_name,
                    "Ticker": company.ticker,
                    "Location": company.location,
                    "Location Type": company.location_type,
                    "Sales": company.sales,
                    "SIC": company.sic,
                    "URL": company.url,
                    "Phone Number": company.phone_number,
                    "Description": company.description,
                    "Established": company.established,
                    "Arizona Info": company.arizona_info,
                    "Website Description": company.website_description,
                    "Classification": company.classification,
                })

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
