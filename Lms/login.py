from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests, time

def logIn(driver, user_id, password):
    driver.get("https://lms-kjsce.somaiya.edu/login/index.php")
    login = WebDriverWait(driver, timeout = 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "potentialidp")))
    login.find_element_by_class_name("btn").click()
    time.sleep(1)
    while(True):
        driver.find_element_by_id("identifierId").send_keys(user_id)
        driver.find_element_by_id("identifierNext").click()
        time.sleep(2)
        try:
            temp = driver.find_element_by_id("identifierId").get_attribute("outerHTML")
            temp = temp[temp.index("aria-invalid") + 14]
            if temp == 'f':
                break
        except ValueError:
            break
        user_id = input("Invalid mail-id. \nPlease enter mail-id:")
        driver.find_element_by_id("identifierId").clear()
    while(True):
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_id("passwordNext").click()
        time.sleep(2)
        try:
            temp = driver.find_element_by_id("password").get_attribute("outerHTML")
            temp = temp[temp.index("aria-invalid") + 14]
            if temp == 'f':
                break
        except ValueError:
            break
        password = input("Invalid password. \nPlease enter the password:")
        driver.find_element_by_name("password").clear()
    
driver = webdriver.Chrome(executable_path=r"../chromedriver.exe")
r = requests.get("https://lms-kjsce.somaiya.edu/my", allow_redirects=False)
if r.status_code >= 300:
    user_id = "ab12@gmail.com"
    password = "abc"
    logIn(driver, user_id, password)
    
else:
    print("Logged in")