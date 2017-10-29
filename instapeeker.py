import sys
import pathlib
import requests
import time
from selenium import webdriver
from PIL import Image
from io import BytesIO

# url of Instagram user page
url = "https://www.instagram.com/" + sys.argv[1] if len(sys.argv) > 1 else "https://www.instagram.com/savagesband"
# name of output foler
output_folder = "./instagram@" + sys.argv[2] + "/" if len(sys.argv) > 1 else "./images/"

# initialize a selenium web driver
driver = webdriver.Firefox(executable_path=r'/Users/rainer/Documents/workspace/python/instapeek/geckodriver')
driver.get(url)

# some little tricks to jump beyond "load more"
driver.execute_script("window.scrollTo(0,2000);")
driver.execute_script("document.elementFromPoint(200, 200).click();")
time.sleep(2)
driver.execute_script("document.elementFromPoint(20, 20).click();")

# infinite scrolling
for y in range(12):
    y = 2000 + 1000 * y
    driver.execute_script("window.scrollTo(0," + str(y) + ");")
    time.sleep(1.5)

res = []
exploded = False
pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

# start scraping
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

# GET request to save images
n = 0
for image_url in res:
    image_object = requests.get(image_url)
    image = Image.open(BytesIO(image_object.content))
    image.save(output_folder + str(n) + "." + image.format, image.format)
    n += 1

print("Saved " + str(n) + " pieces of art!")

driver.quit()
