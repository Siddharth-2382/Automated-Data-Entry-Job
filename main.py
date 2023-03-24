from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22" \
      "%3A%7B%22west%22%3A-122.67022170019531%2C%22east%22%3A-122.19643629980469%2C%22south%22%3A37.62235296460687%2C" \
      "%22north%22%3A37.92791421764088%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B" \
      "%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22" \
      "%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B" \
      "%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C" \
      "%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22" \
      "%3Atrue%7D "
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.127 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate"
}

# get link, address and price of properties by web-scrapping using beautifulsoup
response = requests.get(URL, headers=HEADER)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

all_link_elements = soup.select(".list-card-info a")
all_link = []
for link_element in all_link_elements:
    href = link_element['href']
    if "http" not in href:
        all_link.append(f"https://www.zillow.com{href}")
    else:
        all_link.append(href)
print(all_link)

all_address_element = soup.find_all(name="address", class_="list-card-addr")
all_address = [address.get_text().split("|")[-1].strip() for address in all_address_element]
print(all_address)

all_price_element = soup.find_all(name="div", class_="list-card-price")
all_price = [price.get_text().split("+")[0].split("/mo")[0].strip() for price in all_price_element]
print(all_price)

# Enter data using selenium webdriver
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')
brave_browser_path = os.getenv('BRAVE_BROWSER_PATH')
GOOGLE_FORM_LINK = os.getenv('GOOGLE_FORM_LINK')

OPTION = webdriver.ChromeOptions()
OPTION.binary_location = brave_browser_path

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=OPTION)
driver.maximize_window()

# loop through all address, price and link of properties and add them to spreadsheet using google form
for n in range(len(all_address)):
    driver.get(url=GOOGLE_FORM_LINK)
    time.sleep(3)
    address_input = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/'
                                                           'div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div'
                                                         '/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div'
                                                        '/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address_input.send_keys(all_address[n])
    price_input.send_keys(all_price[n])
    link_input.send_keys(all_link[n])
    submit_button.click()
