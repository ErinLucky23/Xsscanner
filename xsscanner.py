#!/usr/bin/python3
import sys
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
options = Options()
driverPath = Service(executable_path="/snap/bin/geckodriver")
options.add_argument("-headless")



#Checks if you supplied proper argument number, will need to sanatize it so you don't just put random stuff. Right now you can have "./xsscanner 1 2 3" and it works.
if len(sys.argv)==4:
    with open("{0}".format(sys.argv[1])) as f:
        wordList = f.read().splitlines()
    targetSite = "{0}".format(sys.argv[2])
    name = "{0}".format(sys.argv[3])
else:
    sys.stderr.write("Usage: {0} <wordlist> <site> <nameofelement>\n".format(sys.argv[0]))
    sys.exit() #kills script to not open selenium



#Main function
driver = webdriver.Firefox(options=options, service=driverPath) 
wait = WebDriverWait(driver, 0, .01)
driver.get(str(targetSite))
driver.implicitly_wait(3)
print("Getting website and waiting...")
for x in wordList:
    inputBox = driver.find_element(By.NAME, str(name))
    inputBox.clear()
    inputBox.send_keys(str(x))
    inputBox.send_keys(Keys.ENTER)
    time.sleep(0.4)
    try:
        if wait.until(ec.alert_is_there()):
            print("Your XSS Script: " + str(x))
            driver.quit()
            sys.exit()
    except TimeoutException :
        driver.back()
        time.sleep(0.4)

print("No XXS Vulerbility found")
