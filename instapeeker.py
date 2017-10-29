import requests
import time
from selenium import webdriver
from PIL import Image
from io import BytesIO

url = "https://www.instagram.com/kuroega/"
driver = webdriver.Firefox(executable_path=r'/Users/rainer/Documents/workspace/python/ImageScraper/geckodriver')
driver.get(url)

driver.execute_script("window.scrollTo(0,2000);")
driver.execute_script("document.elementFromPoint(200, 200).click();")
time.sleep(2)
driver.execute_script("document.elementFromPoint(20, 20).click();")
for y in range(12):
    y = 2000 + 1000 * y
    driver.execute_script("window.scrollTo(0," + str(y) + ");")
    time.sleep(1.5)

res = []
exploded = False
for i in range(1, 50):
    if exploded:
        break
    for j in range(1, 4):
        try:
            res += driver.find_element_by_xpath("//div[@class='_cmdpi']/div[" +str(i)+ "]/div[" + str(j) + "]/a/div/div/img").get_attribute("src"),
        except:
            print("Ablum Exploded!")
            exploded = True
            break
# print(res)

n = 0
for image_url in res:
    image_object = requests.get(image_url)
    image = Image.open(BytesIO(image_object.content))
    image.save("/Users/rainer/Documents/workspace/python/ImageScraper/ins/image" + str(n) + "." + image.format, image.format)
    n += 1

print("Saved " + str(n) + " pieces of art!")
