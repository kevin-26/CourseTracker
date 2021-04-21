from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests, time, getpass, login, course


driver = webdriver.Chrome(executable_path=r"../chromedriver.exe")
r = requests.get("https://classroom.google.com/u/0/h", allow_redirects=False)
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
    
    
time.sleep(6)
l = login.getCourseList(driver)
for i in l:
    course.courseDetails(driver, i)