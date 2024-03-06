from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time


GOOGLE_FORM_URL = "Your Google Form link"
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

# ----------Part 1: Scrape zillow for all addresses, prices and links using BeautifulSoup----------
headers = {
    "User-Agent": "Example/4.0...",
    "Accept-Language": "example-US...",
}

response = requests.get(url=ZILLOW_URL, headers=headers)
soup = BeautifulSoup(markup=response.text , features="html.parser")

# Get all property links and put in a list.
all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
all_links = [link["href"] for link in all_link_elements]
print(f"There are {len(all_links)} links for all properties.")
# print(all_links)

# Get all property prices, format them correctly by removing all extra text, and put in a list.
all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [price.text.replace("/mo", "").split("+")[0] for price in all_price_elements]
print(f"There are {len(all_prices)} prices for all properties.")
# print(all_prices)

# Get all property addresses, clean up and remove extra text/whitespace, and put in a list.
all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.text.strip().replace("|", "") for address in all_address_elements]
print(f"There are {len(all_addresses)} addresses for all properties.")


# ---------------Part 2: Use Selenium webdriver to fill out all Google Forms.---------------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_links)):
    driver.get(url=GOOGLE_FORM_URL)
    time.sleep(2) 

    address_entry = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/'
                                        'div/div[2]/div/div[1]/div/div[1]/input')
    price_entry = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/'
                                      'div[2]/div/div[1]/div/div[1]/input')
    link_entry = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/'
                                     'div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_entry.send_keys(all_addresses[n])
    price_entry.send_keys(all_prices[n])
    link_entry.send_keys(all_links[n])
    submit_button.click()