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
output_folder = "./Instagram@" + sys.argv[1] + "/" if len(sys.argv) > 1 else "./images/"

# initialize a selenium web driver
driver = webdriver.Firefox(executable_path=r'/Users/rainer/Documents/workspace/python/instapeek/geckodriver')
driver.get(url)

# some little tricks to jump beyond "load more"
driver.execute_script("window.scrollTo(0,2000);")
driver.execute_script("document.elementFromPoint(200, 200).click();")
time.sleep(2)
driver.execute_script("window.scrollTo(0,2000);")
driver.execute_script("document.elementFromPoint(20, 20).click();")

# infinite scrolling
# for y in range(12):
#     y = 2000 + 1000 * y
#     driver.execute_script("window.scrollTo(0," + str(y) + ");")
#     time.sleep(1.5)
script = """
        setTimeout(scrollToBottom, 500);
        function scrollToBottom(){
            bottom = document.body.scrollHeight;
            current = window.innerHeight+ document.body.scrollTop;
            if((bottom-current) >0){
                window.scrollTo(0, bottom);
                setTimeout ( scrollToBottom, 1000 );
            }
        };
        """
driver.execute_script(script)

res = []
cnt = 0
exploded = False
pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
max_ = int(sys.maxsize)
lastFailTime = float('-inf')
# start scraping
for i in range(1, max_):
    if exploded:
        break
    print(i)
    for j in range(1, 4):
        try:
            res += driver.find_element_by_xpath("//div[@class='_cmdpi']/div[" +str(i)+ "]/div[" + str(j) + "]/a/div/div/img").get_attribute("src"),
        except:
            print("*** Loading Instagram ***")
            currentFailTime = time.time()
            if cnt < 10 and currentFailTime - lastFailTime >= 1.0:
                print(" Slow network! waiting for retry...")
                time.sleep(10)
                cnt += 1
                lastFailTime = time.time()
            elif cnt < 10 and currentFailTime - lastFailTime < 1.0:
                print("Scrape completes...")
                exploded = True
            else:
                print("Task failed! Stop retry...")
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
