# Assignment

## Brief

Write the Python codes for the following questions.

## Instructions

Paste the answer as Python in the answer code section below each question.

### Question 1

Question: The scraping of `https://www.scrapethissite.com/pages/forms/` in the last section assumes a hardcoded (fixed) no of pages. Can you improve the code by removing the hardcoded no of pages and instead use the `»` button to determine if there are more pages to scrape? Hint: Use a `while` loop.

```python
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
```

Answer:

```python
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
        # Build and fetch the page URL
        url = f"{BASE_URL}?page_num={page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract rows from this page
        for row in parse_and_extract_rows(soup):
            all_rows.append(row)

        # Detect presence of next-page button
        next_button = soup.select_one("li.next > a")

        # Stop when next button is missing or disabled
        if not next_button:
            break

        parent_li = next_button.find_parent("li")
        if "disabled" in parent_li.get("class", []):
            break

        # Move to next page
        page += 1

    return all_rows

```

## Submission

- Submit the URL of the GitHub Repository that contains your work to NTU black board.
- Should you reference the work of your classmate(s) or online resources, give them credit by adding either the name of your classmate or URL.
---

### Credits

This solution was developed by Farida Charania with coding assistance and guidance from ChatGPT (OpenAI). All implementation, testing, debugging, and final submission formatting were done by Farida Charania.

