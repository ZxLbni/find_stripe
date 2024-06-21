import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse

visited_urls = set()

def crawl_website(url, max_depth=2):
    """
    Crawl the given URL to find additional links.
    """
    if max_depth == 0 or url in visited_urls:
        return []
    
    visited_urls.add(url)
    links = []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(url, href)
                if urlparse(full_url).scheme in ["http", "https"]:
                    links.append(full_url)
    except requests.RequestException as e:
        print(f"Error crawling {url}: {e}")

    return links

def check_stripe(website):
    """
    Check if the given website uses Stripe payment gateway.
    """
    try:
        response = requests.get(website)
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

def find_stripe_keys(website):
    """
    Find potential Stripe API keys in the given website's content.
    """
    keys = []
    try:
        response = requests.get(website)
        if response.status_code == 200:
            matches = re.findall(r'sk_live_[a-zA-Z0-9]{24}', response.text)
            if matches:
                print(f"Found Stripe keys on {website}: {matches}")
                keys.extend(matches)
        else:
            print(f"Failed to access {website} for keys: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error accessing {website} for keys: {e}")
    return keys

def main():
    seed_urls = [
        "https://example.com",  # Replace with initial seed URLs
    ]
    max_depth = 2
    stripe_websites = []
    stripe_keys = []

    to_visit = seed_urls.copy()
    
    while to_visit:
        url = to_visit.pop(0)
        if check_stripe(url):
            stripe_websites.append(url)
            keys = find_stripe_keys(url)
            if keys:
                stripe_keys.extend(keys)
        
        new_links = crawl_website(url, max_depth)
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
