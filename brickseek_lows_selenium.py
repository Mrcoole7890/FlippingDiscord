
# Python program to demonstrate
# selenium
 
# import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()



options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome()
# get google.co.in
driver.get(os.getenv("brickseekLows"))

time.sleep(5)

def sendPercentageOffMessageToDiscord(webhookLinkName, msrp, currentPrice, img, perstOff, title):
    # The API endpoint to communicate with
    url_post = os.getenv(webhookLinkName)
    new_data = {
        "embeds": [
            {
                "type": "rich",
                "title": title,
                "description": "_MSRP_: {}\n_Current Price_: {}\n_Percent Off_: {}".format(msrp, currentPrice, perstOff),
                "color": 65535,
                "thumbnail": {
                    "url": img,
                    "height": 0,
                    "width": 0
                }
            }
        ]
    }
    # A POST request to tthe API
    post_response = requests.post(url_post, json=new_data)

test = driver.find_elements(By.XPATH, '//div[@class="item-list__tile"]')

for ele in test:
    img = ele.find_element(By.XPATH, './/img').get_attribute("src")
    title = ele.find_element(By.XPATH, './/span[@class="item-list__title"]/span').text
    #item-list__discount-meter-bar-fill-text
    percentOff = ele.find_element(By.XPATH, './/div[@class="item-list__discount-meter-bar-fill-text"]').text
    percentOff = percentOff.split("%")[0]
    #price-formatted price-formatted--style-display
    currentPrice = ele.find_element(By.XPATH, './/span[@class="price-formatted price-formatted--style-display"]').text
    currentPriceSeged = currentPrice.split("\n")
    currentPrice = currentPriceSeged[0] + "." + currentPriceSeged[2]
    msrp = ele.find_element(By.XPATH, './/div[@class="item-list__price-column"]//span[@class="price-formatted price-formatted--style-display"]').text
    msrpSeged = msrp.split("\n")
    msrp = msrpSeged[0] + "." + msrpSeged[2]
    sendPercentageOffMessageToDiscord("lowesDiscord",msrp,currentPrice,img,percentOff,title)
