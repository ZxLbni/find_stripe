import requests
from bs4 import BeautifulSoup
import re
import time

def search_websites(query, max_results=10):
    """
    Search the web using a search engine and return a list of websites.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    search_url = f"https://www.google.com/search?q={query}&num={max_results}"
    websites = []

    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if "url?q=" in href and not "webcache" in href:
                    url = href.split("?q=")[1].split("&sa=U")[0]
                    if url.startswith('http'):
                        print(f"Found website: {url}")
                        websites.append(url)
        else:
            print(f"Failed to get search results: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error performing search: {e}")
    return websites[:max_results]

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
    query = "site:example.com"  # Replace with your search query
    max_websites = 10  # Limit the number of websites to check
    websites = search_websites(query, max_websites)
    stripe_websites = []
    stripe_keys = []

    for website in websites:
        if check_stripe(website):
            stripe_websites.append(website)
            keys = find_stripe_keys(website)
            if keys:
                stripe_keys.extend(keys)
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
