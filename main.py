"https://docs.google.com/forms/d/e/1FAIpQLScaXLbp4gz0Lozl094xxPo-TRkYQWH0BrBG7CAOk0IPEpov-A/viewform?usp=sf_link"
from pprint import pprint

import requests
from bs4 import BeautifulSoup


# =============== To scrape all the listings from the Zillow web address =========
URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.67022170019531%2C%22east%22%3A-122.19643629980469%2C%22south%22%3A37.69030420344032%2C%22north%22%3A37.86018111902779%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(URL, headers=header)
# print(response.raise_for_status)
data = response.text
soup = BeautifulSoup(data, "html.parser")

all_link_elements = soup.select(".property-card-link")

all_links = []
for link in all_link_elements:
    href = link["href"]
    # print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

print(all_links)
print(len(all_links))


# =============== Create a list of addresses for all the listings you scraped. e.g. =========

all_address_elements = soup.select(".property-card-link address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]
print(all_addresses)
print(len(all_addresses))


# <span data-test="property-card-price">$2,305+ 1 bd</span>
# <address data-test="property-card-addr">Woodchase Apartment Homes | 2795 San Leandro Blvd, San Leandro, CA</address>