import sys
import pathlib
import requests
import time
from selenium import webdriver
from PIL import Image
from io import BytesIO
from threading import Thread

url = "https://www.instagram.com/savagesband"

driver = webdriver.Firefox(executable_path=r'/Users/rainer/Documents/workspace/python/instapeek/geckodriver')
driver.get(url)

# some little tricks to jump beyond "load more"
driver.execute_script("window.scrollTo(0,2000);")
driver.execute_script("document.elementFromPoint(200, 200).click();")
time.sleep(2)
driver.execute_script("document.elementFromPoint(20, 20).click();")

script = """
        setTimeout(scrollToBottom, 1000);
        function scrollToBottom(){
            bottom = document.body.scrollHeight;
            current = window.innerHeight+ document.body.scrollTop;
            if((bottom-current) >0){
                window.scrollTo(0, bottom);
                setTimeout ( scrollToBottom, 1000 );
            }
        };
        """

a1 = Thread(driver.execute_script(script))
a1.start()
a1.join()
# driver.quit()
