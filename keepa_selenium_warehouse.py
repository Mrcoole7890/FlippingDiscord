
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
driver.get(os.getenv("keepaWarehouse"))

time.sleep(10)

def sendPercentageOffMessageToDiscord(webhookLinkName, average, currentPrice, img, perstOff, title, asin):
    # The API endpoint to communicate with
    url_post = os.getenv(webhookLinkName)
    print(webhookLinkName)
    new_data = {
        "embeds": [
            {
                "type": "rich",
                "title": title,
                "description": "_Average Price_: {}\n_Current Price_: {}\n_Percent Off_: {}\n_ASIN_: {}".format(average, currentPrice, perstOff, asin),
                "color": 65535,
                "url": "https://www.amazon.com/dp/" + asin,
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
    print(new_data)
    print(post_response)

for i in range(0, 105):
    """
    get the image
    average price //div[@id="p0"]//span[contains(text(),"Average")]
    new price
    percent off
    img
    //div[@id="p0"]//div[@class="title"]
    """

    currElement = driver.find_element(By.ID, "p{}".format(i))
    asin = currElement.find_element(By.XPATH, './/a').get_attribute("href").split("-")[1]
    img = currElement.find_element(By.XPATH, './/img').get_attribute("src")
    avgPrice = currElement.find_element(By.XPATH, './/span[contains(text(),"Average")]').text
    currPrice = currElement.find_element(By.XPATH, './/span[contains(text(),"Now")]').text
    percentOff = currElement.find_element(By.XPATH, './/span[contains(text(),"%")]').text
    title = currElement.find_element(By.XPATH, './/div[@class="title"]').text

    print(int(percentOff[0:2]))

    if (int(percentOff[0:2]) >= 90):
        sendPercentageOffMessageToDiscord("amazonWarehouse90Off", avgPrice, currPrice, img, percentOff, title, asin)

    elif (int(percentOff[0:2]) >= 80):
        sendPercentageOffMessageToDiscord("amazonWarehouse80Off", avgPrice, currPrice, img, percentOff, title, asin)

    else:
        sendPercentageOffMessageToDiscord("amazonWarehouse79below", avgPrice, currPrice, img, percentOff, title, asin)