from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests, time, getpass

def logIn(driver : webdriver, user_id : str, password : str):
    driver.get("https://lms-kjsce.somaiya.edu/login/index.php")
    login = WebDriverWait(driver, timeout = 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "potentialidp")))
    login.find_element_by_class_name("btn").click()
    # time.sleep(1)
    while(True):
        driver.find_element_by_id("identifierId").send_keys(user_id)
        driver.find_element_by_id("identifierNext").click()
        time.sleep(2)
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
                return False
        except:
            print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
            return False
    while(True):
        WebDriverWait(driver, timeout = 10).until(expected_conditions.visibility_of_element_located((By.NAME, "password"))).send_keys(password)
        driver.find_element_by_id("passwordNext").click()
        time.sleep(3)
        if 'edu/my' in driver.current_url:
            return True
        try:
            temp = driver.find_element_by_id("password").get_attribute("outerHTML")
            temp = temp[temp.index("aria-invalid") + 14]
            if temp == 't':
                password = getpass.getpass(prompt='Invalid password. Please enter your password: ', stream=None).strip()
                driver.find_element_by_name("password").clear()
            else:
                print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
                driver.get("https://lms-kjsce.somaiya.edu/login/index.php")
                time.sleep(3)
                if 'edu/my' in driver.current_url:
                    return True
                return False
        except:
            if 'edu/my' in driver.current_url:
                return True
            driver.get("https://lms-kjsce.somaiya.edu/login/index.php")
            time.sleep(3)
            if '0/h' in driver.current_url:
                return True
            print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
            return False
    
def getCourseList (driver: webdriver):
    time.sleep(1)
    a = driver.find_element_by_id("page-container-1")
    l = a.find_elements(By.CSS_SELECTOR, "div[class='card dashboard-card']")
    id = []
    for i in l:
        name = i.find_elements_by_tag_name('div')[1].find_element_by_tag_name('div').find_element_by_tag_name('a').find_element_by_class_name('multiline').text
        print("Are you currently enrolled in", name,"(Y/N)? ", end = '')
        if input().lower() == 'y':
            id.append(["https://lms-kjsce.somaiya.edu/course/view.php?id=" + str(i.get_attribute('data-course-id')), name])
    return id