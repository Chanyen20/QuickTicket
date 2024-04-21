# import Selenium module
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# get Chrome Driver's exe file
options = Options()
options.chrome_executable_path = "../"

# getting use the Driver 
driver = webdriver.Chrome(options = options)
driver.get("")
driver.close()
