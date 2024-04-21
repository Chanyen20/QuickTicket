# import Selenium module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import pytz
import requests

USERNAME = "" # @todo 
PASSWORD = "" # @todo
TARGETURL = "" # @todo
TARGET_TIME_TW = datetime(2024, 4, 21, 14, 16, 0).astimezone(pytz.timezone('Asia/Taipei'))

# get Chrome Driver's exe file
options = Options()

#  減少資源消耗
# options.add_argument("--headless")
# options.chrome_executable_path = "/Users/janehsiung/Desktop/git/Python/autoGetTicket/chromedriver"
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

# getting use the Driver 
driver = webdriver.Chrome(options = options)

# connect to target website
driver.get(TARGETURL)

# 登入kktix
loginButton = driver.find_element(By.LINK_TEXT, "登入")
loginButton.click()

userNameInput = driver.find_element(By.ID, "user_login")
passwordInput = driver.find_element(By.ID, "user_password")

userNameInput.send_keys(USERNAME)
passwordInput.send_keys(PASSWORD)
passwordInput.send_keys(Keys.ENTER)

# ########
def countdown():
    max_attempts = 8
    attempt = 0

    while attempt < max_attempts:
        ticketPlusButtons = driver.find_elements(By.CSS_SELECTOR, ".btn-default.plus")
        
        # 如果找到至少一個元素，則跳出迴圈
        if len(ticketPlusButtons) > 0:
            break
        else:
            # 如果沒找到，刷新頁面並等待一段時間後重試
            print(f"元素未找到，正在重試...（嘗試次數：{attempt + 1}）")
            driver.refresh()
            # 等待網頁重新加載，這裡等待0.5秒，根據你的網絡速度和頁面大小調整
            if attempt < 5:
                time.sleep(0.4)
            else:
                time.sleep(0.5)
            attempt += 1

    if attempt == max_attempts:
        print("超過最大嘗試次數，未能找到元素。")
        driver.refresh()
        time.sleep(1200)
    else:
        print("找到元素，進行下一步操作。")
        if len(ticketPlusButtons) >= 4:
            for _ in range(2):
                ticketPlusButtons[(len(ticketPlusButtons)-1)].click()
            for _ in range(2):
                ticketPlusButtons[(len(ticketPlusButtons)-3)].click()
        else:
            time.sleep(1200)

        checkbox = driver.find_element(By.ID, "person_agree_terms")
        if checkbox:
            checkbox.click()
        else:
            time.sleep(1200)

        from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

        try:
            button_next = driver.find_element(By.XPATH, "//button[contains(., '下一步')]")
            if button_next.is_enabled():
                button_next.click()
            else:
                print("下一步按鈕目前不可用")
        except NoSuchElementException:
            print("未找到 '下一步' 按鈕。")
        except ElementNotInteractableException:
            print("下一步按鈕目前不可交互。")

        try:
            button_comp = driver.find_element(By.XPATH, "//button[contains(., '電腦配位')]")
            if button_comp.is_enabled():
                button_comp.click()
            else:
                print("電腦配位按鈕目前不可用")
        except NoSuchElementException:
            print("未找到 '電腦配位' 按鈕。")
        except ElementNotInteractableException:
            print("電腦配位按鈕目前不可交互。")

        try:
            button_self = driver.find_element(By.XPATH, "//button[contains(., '自行選位')]")
            if button_self.is_enabled():
                button_self.click()
            else:
                print("自行選位按鈕目前不可用")
        except NoSuchElementException:
            print("未找到 '自行選位' 按鈕。")
            time.sleep(1200)
        except ElementNotInteractableException:
            print("自行選位按鈕目前不可交互。")
            time.sleep(1200)
# ########

# 判斷是否開始搶票/重整

    # 首次檢查
response = requests.get('https://kktix.com')
server_time_str = response.headers['Date']
server_time_gmt = datetime.strptime(server_time_str, '%a, %d %b %Y %H:%M:%S GMT').replace(tzinfo=pytz.utc)
server_time_taiwan = server_time_gmt.astimezone(pytz.timezone('Asia/Taipei'))
delta_seconds = (TARGET_TIME_TW - server_time_taiwan).total_seconds()

    # 如果delta_seconds大于一定的阈值，先进行长时间等待
if delta_seconds > 10:  # 假设阈值为10秒
    print(f"初始等待时间：{delta_seconds - 3}秒")  # 留出一些缓冲时间
    time.sleep(delta_seconds - 3)

while True:
    response = requests.get('https://kktix.com')
    server_time_str = response.headers['Date']
    server_time_gmt = datetime.strptime(server_time_str, '%a, %d %b %Y %H:%M:%S GMT').replace(tzinfo=pytz.utc)
    server_time_taiwan = server_time_gmt.astimezone(pytz.timezone('Asia/Taipei'))

    delta_seconds = (TARGET_TIME_TW - server_time_taiwan).total_seconds()
    print("the server time is: " + server_time_taiwan.strftime('%Y-%m-%d %H:%M:%S'))
    print("the delta time is: " + str(delta_seconds))


    if delta_seconds <= 2:
        countdown()
        break
    elif delta_seconds > 0:
        # 如果还没到时间，等待一段时间后再次检查
        print(f"等待中...当前服务器时间（台湾时区）: {server_time_taiwan}, 目标时间（台湾时区）: {TARGET_TIME_TW}, 时间差: {delta_seconds}秒")
        time.sleep(min(delta_seconds - 2, 1))  # 每次检查间隔至少1秒，但不超过时间差减2秒
    else:
        # 如果已经错过了目标时间
        print("已经超过目标执行时间。")
        break


time.sleep(10)
input("按回车键结束脚本...")



