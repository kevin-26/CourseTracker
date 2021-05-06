from . import login, course
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests, time, getpass


driver = webdriver.Chrome('/usr/bin/chromedriver')
# driver = webdriver.Chrome(executable_path=r"./chromedriver.exe")
r = requests.get("https://classroom.google.com/u/0/h", allow_redirects=False)
user_id, password = '',''
if r.status_code >= 300:
    user_id = input("Please enter your mail-id:").strip()
    password = getpass.getpass(prompt='Please enter your password: ', stream=None).strip()
    while not login.logIn(driver, user_id, password):
        time.sleep(2)
        user_id = input("Please enter your mail-id:").strip()
        password = getpass.getpass(prompt='Please enter your password: ', stream=None).strip()
    print("Logged in")
else:
    print("Logged in")
    
    
while not WebDriverWait(driver, timeout = 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "gHz6xd"))):
    time.sleep(2)
check_height = driver.execute_script("return document.body.scrollHeight;")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    height = driver.execute_script("return document.body.scrollHeight;") 
    if height == check_height: 
        break 
    check_height = height   
google_s = login.getCourseList(driver)
google = []
for z in google_s:
    google.append(list(course.courseDetails(driver, z[0])))