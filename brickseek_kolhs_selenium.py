
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
import math

load_dotenv()



options = Options()
options.add_experimental_option('detach', True)

driver = webdriver.Chrome()
# get google.co.in
driver.get(os.getenv("brickseekKolhs"))

time.sleep(5)

def sendPercentageOffMessageToDiscord(webhookLinkName, currentPrice, img, perstOff, title, id):
    # The API endpoint to communicate with
    url_post = os.getenv(webhookLinkName)
    new_data = {
        "embeds": [
            {
                "type": "rich",
                "title": title,
                "description": "_Current Price_: {}\n_Percent Off_: %{}".format(currentPrice, perstOff),
                "color": 65535,
                "url": "https://www.kohls.com/product/prd-{}/{}".format(id, title.replace(" ", "-")),
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

test = driver.find_elements(By.XPATH, '//li[@class="flex flex-row justify-between sm:flex-col a-bg-color sm:rounded border-b-[1px] a-border-color-separator sm:border-b-0 relative undefined min-w-[278px] md:max-w-[278px]"]')
for ele in test:
    img = ele.find_element(By.XPATH, './/img').get_attribute("src")
    id = img.split("/")[-1].split("?")[0].split("_")[0]
    title = ele.find_element(By.XPATH, './/a[@class="block font-muted a-text-color-title line-clamp-2 mt-1 cursor-pointer sm:min-h-[42px]"]').text
    currentPrice = ele.find_element(By.XPATH, './/span[@class="font-large a-text-color-brand"]').text.split("$")[1].replace(",", "")
    #muted line-through
    oldPrice = ele.find_element(By.XPATH, './/span[@class="muted line-through"]').text.split("$")[1].replace(",", "")
    amountOff = ele.find_element(By.XPATH, './/div[@class="inline-block a-bg-color-brand text-white rounded font-footnote font-medium py-[3px] px-3"]').text.split("$")[1].replace(",", "")
    percentOff = math.floor(float(amountOff) / float(oldPrice) * 100)
    sendPercentageOffMessageToDiscord("kolhsDiscord",currentPrice,img,percentOff,title, id)
