import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin, urlparse

def get_headers():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18362',
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def fetch_page_content(url):
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to access {url}: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def extract_links(url, html_content):
    links = set()
    soup = BeautifulSoup(html_content, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        if urlparse(full_url).scheme in ["http", "https"]:
            links.add(full_url)
    return links

def check_stripe_integration(html_content):
    return "stripe" in html_content.lower()

def find_stripe_keys(html_content):
    return re.findall(r'sk_live_[a-zA-Z0-9]{24}', html_content)

def crawl_website(url, max_depth, visited_urls):
    if max_depth == 0 or url in visited_urls:
        return []

    visited_urls.add(url)
    html_content = fetch_page_content(url)
    if html_content is None:
        return []

    new_links = extract_links(url, html_content)
    if check_stripe_integration(html_content):
        return [(url, html_content, new_links)]

    return [(None, None, new_links)]

def main():
    seed_urls = [
        "https://www.shopify.com",
        "https://www.patreon.com",
        "https://www.kickstarter.com",
        "https://www.gofundme.com",
        "https://www.squarespace.com",
        "https://www.bigcommerce.com",
        "https://www.woocommerce.com",
        "https://www.wix.com",
        "https://www.weebly.com",
        "https://www.etsy.com",
    ]
    max_depth = 1
    max_websites = 50
    stripe_websites = []
    stripe_keys = []

    to_visit = seed_urls.copy()
    visited_urls = set()
    
    while to_visit and len(visited_urls) < max_websites:
        url = to_visit.pop(0)
        if url in visited_urls:
            continue

        results = crawl_website(url, max_depth, visited_urls)
        for result_url, html_content, new_links in results:
            if result_url and html_content:
                stripe_websites.append(result_url)
                keys = find_stripe_keys(html_content)
                if keys:
                    stripe_keys.extend(keys)
            
            to_visit.extend(new_links)

        time.sleep(2)  # Adding delay to avoid being blocked

    if stripe_websites:
        print(f"Writing {len(stripe_websites)} Stripe websites to file.")
        with open("stripe_websites.txt", "w") as file:
            for site in stripe_websites:
                file.write(f"{site}\n")
    else:
        print("No Stripe websites found.")

    if stripe_keys:
        print(f"Writing {len(stripe_keys)} Stripe keys to file.")
        with open("stripe_keys.txt", "w") as file:
            for key in stripe_keys:
                file.write(f"{key}\n")
    else:
        print("No Stripe keys found.")

if __name__ == "__main__":
    main()
