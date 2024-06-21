import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin, urlparse

visited_urls = set()

# List of common User-Agent headers to randomize requests
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18362',
]

def get_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def crawl_website(url, max_depth=2):
    """
    Crawl the given URL to find additional links.
    """
    if max_depth == 0 or url in visited_urls:
        return []

    visited_urls.add(url)
    links = []

    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(url, href)
                if urlparse(full_url).scheme in ["http", "https"] and full_url not in visited_urls:
                    links.append(full_url)
                    print(f"Discovered link: {full_url}")
        else:
            print(f"Failed to access {url}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error crawling {url}: {e}")

    return links

def check_stripe(website):
    """
    Check if the given website uses Stripe payment gateway.
    """
    try:
        response = requests.get(website, headers=get_headers())
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if "stripe" in soup.text.lower():
                print(f"Stripe found on {website}")
                return True
        else:
            print(f"Failed to access {website}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error accessing {website}: {e}")
    return False

def find_stripe_keys(html_content):
    """
    Find potential Stripe API keys in the given HTML content.
    """
    keys = re.findall(r'sk_live_[a-zA-Z0-9]{24}', html_content)
    return keys

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
    
    while to_visit and len(visited_urls) < max_websites:
        url = to_visit.pop(0)
        if url in visited_urls:
            continue
        visited_urls.add(url)
        
        if check_stripe(url):
            stripe_websites.append(url)
            try:
                response = requests.get(url, headers=get_headers())
                if response.status_code == 200:
                    keys = find_stripe_keys(response.text)
                    if keys:
                        stripe_keys.extend(keys)
            except requests.RequestException as e:
                print(f"Error accessing {url} for keys: {e}")
        
        new_links = crawl_website(url, max_depth)
        to_visit.extend(new_links)

        time.sleep(5)  # Adding delay to avoid being blocked

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
