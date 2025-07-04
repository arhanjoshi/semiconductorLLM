from scraper.semiconductor_scraper import fetch_page

URL = "https://www.tsmc.com"  # try different sites if needed

html = fetch_page(URL)
if html is None:
    print(f"[FAIL] fetch_page returned None for {URL}")
else:
    print(f"[OK] fetched {len(html)} bytes from {URL}\n")
    print(html[:500])  # peek at the first 500 chars
