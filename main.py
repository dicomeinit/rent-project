"https://docs.google.com/forms/d/e/1FAIpQLScaXLbp4gz0Lozl094xxPo-TRkYQWH0BrBG7CAOk0IPEpov-A/viewform?usp=sf_link"
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# =============== To scrape all the listings from the Zillow web address =========
URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.67022170019531%2C%22east%22%3A-122.19643629980469%2C%22south%22%3A37.69030420344032%2C%22north%22%3A37.86018111902779%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScaXLbp4gz0Lozl094xxPo-TRkYQWH0BrBG7CAOk0IPEpov-A/viewform?usp=sf_link"

response = requests.get(URL, headers=HEADERS)
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

# =============== Create a list of prices for all the listings you scraped. e.g. =========

all_price_elements = soup.select(".property-card-data span")
all_prices = [price.get_text().split("+")[0] for price in all_price_elements if "$" in price.text]
print(all_prices)
print(len(all_prices))

# =============== Use Selenium to fill in the form you created =========

for n in range(len(all_links)):
    service = Service("/Users/diana/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get(FORM_URL)

    time.sleep(2)
    address = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
