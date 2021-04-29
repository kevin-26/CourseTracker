from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests, time, getpass

def logIn(driver : webdriver, user_id : str, password : str):
    driver.get("https://classroom.google.com/u/0/h")
    while(True):
        driver.find_element_by_id("identifierId").send_keys(user_id)
        driver.find_element_by_id("identifierNext").click()
        time.sleep(3)
        if len(driver.find_elements_by_name("password")) > 0:
            break
        try:
            temp = driver.find_element_by_id("identifierId").get_attribute("outerHTML")
            temp = temp[temp.index("aria-invalid") + 14]
            if temp == 't':
                user_id = input("Invalid mail-id. \nPlease enter mail-id:")
                driver.find_element_by_id("identifierId").clear()
            else:
                print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
                driver.get("https://classroom.google.com/u/0/h")
                time.sleep(3)
                if '0/h' in driver.current_url:
                    return True
                return False
        except:
            print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
            driver.get("https://classroom.google.com/u/0/h")
            time.sleep(3)
            if '0/h' in driver.current_url:
                return True
            return False
    while(True):
        WebDriverWait(driver, timeout = 10).until(expected_conditions.visibility_of_element_located((By.NAME, "password"))).send_keys(password)
        driver.find_element_by_id("passwordNext").click()
        time.sleep(3)
        if '0/h' in driver.current_url:
            return True
        try:
            temp = driver.find_element_by_id("password").get_attribute("outerHTML")
            temp = temp[temp.index("aria-invalid") + 14]
            if temp == 't':
                password = getpass.getpass(prompt='Invalid password. Please enter your password: ', stream=None).strip()
                driver.find_element_by_name("password").clear()
            else:
                print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
                driver.get("https://classroom.google.com/u/0/h")
                time.sleep(3)
                if '0/h' in driver.current_url:
                    return True
                return False
        except:
            if '0/h' in driver.current_url:
                return True
            driver.get("https://classroom.google.com/u/0/h")
            time.sleep(3)
            if '0/h' in driver.current_url:
                return True
            print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
            return False
    
def getCourseList (driver: webdriver) -> []:
    l = driver.find_elements_by_tag_name('li')
    id = []
    for i in l:
        j = i.find_element_by_tag_name('div').get_attribute("class").split('-')[1]
        name = i.find_element_by_tag_name('h2').find_element_by_tag_name('div').text
        print("Are you currently enrolled in", name,"(Y/N)? ", end = '')
        if input().lower() == 'y':
            id.append("https://classroom.google.com/u/0/c/" + j)
    return id