from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

from pprint import pprint
from time import sleep



HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept-Language": "en-US,en;q=0.5",
}

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSflYhaSiYjhmdGIKWGnBbep4u1f7CVdJ--7nr02rgqJIsihzg/viewform?usp=sf_link"
FORM_RESPONSES = "https://docs.google.com/forms/d/1OGVkrV8JT7MXRnhLR5C0zlTOT85MHgW8Br7m8mqcF4g/edit#responses"
ZILLOW_URL = "https://www.zillow.com/park-slope-brooklyn-new-york-ny/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Park%20Slope%2C%20New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.03159495275878%2C%22east%22%3A-73.9311730472412%2C%22south%22%3A40.645113432062146%2C%22north%22%3A40.69667232463091%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A197044%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A601591%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D"
    # Burlington, VT "https://www.zillow.com/burlington-vt/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Burlington%2C%20VT%22%2C%22mapBounds%22%3A%7B%22west%22%3A-73.44844181103515%2C%22east%22%3A-73.04675418896484%2C%22south%22%3A44.39161642972843%2C%22north%22%3A44.5855951413992%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A37662%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A602982%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
    # Boulder, CO "https://www.zillow.com/boulder-co/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Boulder%2C%20CO%22%2C%22mapBounds%22%3A%7B%22west%22%3A-105.71586162207032%2C%22east%22%3A-104.9124863779297%2C%22south%22%3A39.80992565922314%2C%22north%22%3A40.22640537302215%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A30543%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A482386%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A2400%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
    # Sand Franciso "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.91226424169922%2C%22east%22%3A-122.1088889975586%2C%22south%22%3A37.503424909695106%2C%22north%22%3A37.933600960252704%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

chrome_driver_path = "YOUR PATH TO CHROMEDRIVER.EXE"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
action = ActionChains(driver)

driver.get(ZILLOW_URL)
driver.maximize_window()
sleep(5)
# Manually scroll to load all the listings on the page.
print("Manually scroll down to load all listings")
sleep(20)


####  Various attempts to scroll Zillow's listing sidebar, to load up all the pages, none seem to work. Use manual scroll.
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# target = driver.find_element(By.XPATH, '//*[@id="schools-disclaimer"]/p[1]')
# target = driver.find_element(By.XPATH, '//*[@id="grid-search-results"]/ul')
# target.send_keys(Keys.PAGE_DOWN)
# driver.execute_script("arguments[0].scrollIntoView(true);", target)
# target.send_keys(Keys.PAGE_DOWN)
# driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located(By.XPATH, "//div[@class='search-pagination']")))
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # driver.execute_script("arguements[0].scrollIntoView(true);", last_height)
#     sleep(2)
#     new_height = driver.execute_script("return document.body.scrollHeight")
#
#     if new_height == last_height:
#         break
#     last_height = new_height
#     driver.implicitly_wait(2)
#
# print("scrolled")

# Bring the source html from the webpage, to manually read it into a file. This helps with getting all listings.
html_source = driver.page_source
sleep(5)

with open('file.html', mode="w", encoding="utf-8") as fp:
    fp.write(html_source)

with open("file.html", mode="r", encoding="utf-8") as fp:
    content = fp.read()

soup = BeautifulSoup(content, "html.parser")

# Get rent prices as str
rent = soup.find_all("span", {'data-test':"property-card-price"})
prices = [price.text for price in rent]

# Get addresses
address = soup.find_all("address", {'data-test': "property-card-addr"})
address_list = [addy.text for addy in address]

# Get property links
property_link = soup.find_all("a", {"data-test": "property-card-link"})
raw_links = [link["href"] for link in property_link]
raw_links = list(dict.fromkeys(raw_links))
link_list = []

# Complete broken property links
for index in range(len(raw_links)):
    if not (raw_links[index]).startswith("http"):
        link_list.append('https://www.zillow.com' + raw_links[index])
    else:
        link_list.append(raw_links[index])

# pprint(prices)
# pprint(address_list)
# pprint(raw_links)
# pprint(link_list)


# Now, inputting the data into the google form with Selenium
driver.get(FORM_URL)
driver.maximize_window()


for index in range(len(link_list)):
    try:
        address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

        address_input.send_keys(address_list[index])
        price_input.send_keys(prices[index])
        link_input.send_keys(link_list[index])
        print(f"{address_list[index]}  {prices[index]}  {link_list[index]}")
        submit.click()
        sleep(5)
        another = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        another.click()
        sleep(5)
    except NoSuchElementException:
        pass

driver.quit()
