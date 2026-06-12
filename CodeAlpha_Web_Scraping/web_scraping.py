from bs4 import BeautifulSoup
import json
import pandas as pd
from playwright.sync_api import sync_playwright

url = "https://www.imdb.com/chart/top/"

movies = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        locale="en-US"
    )

    page.set_extra_http_headers({
        "Accept-Language": "en-US,en;q=0.9"
    })

    page.goto(url, wait_until="load", timeout=120000)

    page.wait_for_timeout(5000)

    html = page.content()

    browser.close()

soup = BeautifulSoup(html, "html.parser")


def parse_next_data(soup):
    script = soup.select_one("script#__NEXT_DATA__")
    if not script or not script.string:
        return []

    try:
        payload = json.loads(script.string)
    except json.JSONDecodeError:
        return []

    chart_titles = (
        payload
        .get("props", {})
        .get("pageProps", {})
        .get("pageData", {})
        .get("chartTitles", {})
        .get("edges", [])
    )

    movies = []
    for edge in chart_titles:
        node = edge.get("node", {})
        title = node.get("titleText", {}).get("text", "")
        year = node.get("releaseYear", {}).get("year", "")
        rating = node.get("ratingsSummary", {}).get("aggregateRating", "")

        if title:
            movies.append({
                "Movie Title": title,
                "Release Year": year,
                "IMDb Rating": rating,
            })

    return movies


def parse_legacy_table(soup):
    rows = soup.select("tbody.lister-list tr")
    movies = []

    for row in rows:
        title_tag = row.select_one("td.titleColumn a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        year_tag = row.select_one("td.titleColumn span.secondaryInfo")
        year = year_tag.get_text(strip=True).strip("()") if year_tag else ""
        rating_tag = row.select_one("td.ratingColumn.imdbRating strong")
        rating = rating_tag.get_text(strip=True) if rating_tag else ""

        movies.append({
            "Movie Title": title,
            "Release Year": year,
            "IMDb Rating": rating,
        })

    return movies


movies = parse_next_data(soup)
if not movies:
    movies = parse_legacy_table(soup)

if not movies:
    raise SystemExit(
        "No movies found. IMDb may have changed its structure or the page did not render correctly."
    )

print("\nFirst 5 Movies:")
print(movies[:5])

df = pd.DataFrame(movies)

print("\nDataFrame Preview:")
print(df.head())

df.to_csv("movies_dataset.csv", index=False, encoding="utf-8")

print(f"\nDataset saved successfully! ({len(df)} movies)")