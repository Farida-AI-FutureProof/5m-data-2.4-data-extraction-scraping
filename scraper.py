import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.scrapethissite.com/pages/forms/"

def parse_and_extract_rows(soup: BeautifulSoup):
    """
    Extract table rows from the parsed HTML.
    """
    header = soup.find('tr')
    headers = [th.text.strip() for th in header.find_all('th')]
    teams = soup.find_all('tr', 'team')

    for team in teams:
        row_dict = {header: col.text.strip()
                    for header, col in zip(headers, team.find_all('td'))}
        yield row_dict


def scrape_all_pages():
    """
    Scrape all pages by following the Next button until no more pages exist.
    Uses aria-label="Next" as the primary selector, with a fallback to li.next > a.
    """
    page = 1
    all_rows = []

    while True:
        url = f"{BASE_URL}?page_num={page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract rows
        for row in parse_and_extract_rows(soup):
            all_rows.append(row)

        # ----- NEXT PAGE LOGIC -----
        # Primary selector (recommended by instructor)
        next_button = soup.find("a", {"aria-label": "Next"})

        # Fallback selector (CSS based)
        if not next_button:
            next_button = soup.select_one("li.next > a")

        # If still no next button → end of pagination
        if not next_button:
            break

        # If disabled (no more pages)
        parent_li = next_button.find_parent("li")
        if parent_li and "disabled" in parent_li.get("class", []):
            break

        # Otherwise go to next page
        page += 1

    return all_rows



import pandas as pd

if __name__ == "__main__":
    results = scrape_all_pages()
    print(f"Total rows scraped: {len(results)}")

    df = pd.DataFrame(results)
    df.to_csv("hockey_teams.csv", index=False)
    print("Saved to hockey_teams.csv")

