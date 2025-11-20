import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.scrapethissite.com/pages/forms/"

def parse_and_extract_rows(soup: BeautifulSoup):
    """
    Extract table rows from the parsed HTML.

    Args:
        soup: The parsed HTML.

    Returns:
        An iterator of dictionaries with the data from the current page.
    """
    header = soup.find('tr')
    headers = [th.text.strip() for th in header.find_all('th')]
    teams = soup.find_all('tr', 'team')

    for team in teams:
        row_dict = {}
        for header, col in zip(headers, team.find_all('td')):
            row_dict[header] = col.text.strip()
        yield row_dict


def scrape_all_pages():
    """
    Scrape all pages by following the “next page” (»)
    button until it is no longer available.
    """
    page = 1
    all_rows = []

    while True:
        # Fetch the page
        url = f"{BASE_URL}?page_num={page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract rows from this page
        for row in parse_and_extract_rows(soup):
            all_rows.append(row)

        # Find the "next page" button
        next_button = soup.select_one("li.next > a")

        # If there is no next button → end of pagination
        if not next_button:
            break

        # If the button is disabled → stop
        parent_li = next_button.find_parent("li")
        if "disabled" in parent_li.get("class", []):
            break

        # Otherwise → go to next page
        page += 1

    return all_rows


if __name__ == "__main__":
    results = scrape_all_pages()
    print(f"Total rows scraped: {len(results)}")
    for row in results[:5]:
        print(row)
import pandas as pd

if __name__ == "__main__":
    results = scrape_all_pages()
    print(f"Total rows scraped: {len(results)}")

    df = pd.DataFrame(results)
    df.to_csv("hockey_teams.csv", index=False)
    print("Saved to hockey_teams.csv")
