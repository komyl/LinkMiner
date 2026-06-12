from bs4 import BeautifulSoup
import requests
import validators
import time
from urllib.parse import urljoin

start_url = input("Please enter the URL to start scraping: ")

if not validators.url(start_url):
    print("Invalid URL. Please enter a valid URL.")
    exit()

try:
    r = requests.get(start_url, timeout=10)
    r.raise_for_status()
except requests.HTTPError as e:
    print(f"HTTP error occurred for {start_url}: {e.response.status_code} - {e.response.reason}")
    exit()
except requests.ConnectionError:
    print(f"Connection error occurred for {start_url}.")
    exit()
except requests.Timeout:
    print(f"Timeout occurred for {start_url}.")
    exit()
except requests.RequestException as e:
    print(f"Error in request to {start_url}: {e}")
    exit()

soup = BeautifulSoup(r.text, 'lxml')
links = set()

for link in soup.findAll('a', href=True):
    href = link.get('href')
    full_url = urljoin(start_url, href)
    if validators.url(full_url):
        links.add(full_url)

processed_links = set()
new_links = list(links)

for i, u in enumerate(new_links):
    if i >= 1000:
        break

    if u in processed_links:
        continue

    processed_links.add(u)

    try:
        r = requests.get(u, timeout=10)
        r.raise_for_status()
        print(f"Processing: {u}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred for {u}: {e.response.status_code} - {e.response.reason}")
        continue
    except requests.ConnectionError:
        print(f"Connection error occurred for {u}.")
        continue
    except requests.Timeout:
        print(f"Timeout occurred for {u}.")
        continue
    except requests.RequestException as e:
        print(f"Error in request to {u}: {e}")
        continue

    soup = BeautifulSoup(r.text, 'lxml')
    for link in soup.findAll('a', href=True):
        href = link.get('href')
        full_url = urljoin(u, href)
        if validators.url(full_url) and full_url not in links:
            new_links.append(full_url)

    time.sleep(1)

print("Link processing completed.")