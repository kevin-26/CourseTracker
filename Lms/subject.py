from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests, time

def logIn(driver : webdriver, user_id : str, password : str):
    driver.get("https://lms-kjsce.somaiya.edu/login/index.php")
    login = WebDriverWait(driver, timeout = 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "potentialidp")))
    login.find_element_by_class_name("btn").click()
    time.sleep(1)
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
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_id("passwordNext").click()
        time.sleep(3)
        if 'edu/my' in driver.current_url:
            return True
            break
        try:
            temp = driver.find_element_by_id("password").get_attribute("outerHTML")
            temp = temp[temp.index("aria-invalid") + 14]
            if temp == 't':
                password = input("Invalid password. \nPlease enter the password:")
                driver.find_element_by_name("password").clear()
            else:
                print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
                return False
        except:
            if 'edu/my' in driver.current_url:
                break
            print("Kindly try again. One of the following reasons may be possible for the error:\n1. No internet connection\n2. You have 2-factor authentication enabled for your mail account")
            return False
    
def getSubject(url : str) -> {} :
    driver.get(url)
    time.sleep(3)
    topics = driver.find_element_by_css_selector('ul.topics')
    sections = topics.find_elements_by_css_selector('li.section')
    subject_data = {}
    c = 'a'
    for section in sections:
        section_data = []
        try:
            sectionName = section.get_attribute("aria-label")
            section_data.append(sectionName)
            # activities = section.find_elements_by_css_selector('div.activityinstance')
            activities = section.find_elements_by_css_selector('li.activity')
            for activity in activities:
                data = {}
                try:
                    name = activity.find_element_by_class_name('instancename').text
                    # print(name)
                    if(name == "Announcements"):
                        continue
                    # Reference dictionary
                    ref_data = {}
                    activity_url = activity.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    data[name] = {}
                    isResource = activity.get_attribute("class").split(' ')
                    if isResource[2] == "modtype_assign":
                        ref_data["is_resource"] = 0
                    elif isResource[2] == "modtype_resource":
                        ref_data["is_resource"] = 1
                    else:
                        ref_data["is_resource"] = -1
                    
                    ref_data["url"] = activity_url
                    try:
                        uploadStr = activity.find_element_by_css_selector('span.resourcelinkdetails').get_attribute('innerHTML')
                        # Convert this string to some comparable data
                        ref_data["upload_time"] = uploadStr
                        # print(uploadStr)
                    except:
                        pass
                    data[name] = ref_data
                    section_data.append(data)
                except:
                    pass
                    # print(activity.get_attribute('outerHTML'))
            subject_data[c] = section_data 
            c = chr(ord(c)+1)
        except:
            print(section.get_attribute('outerHTML'))
    print(subject_data)
    return subject_data


    

driver = webdriver.Chrome()
r = requests.get("https://lms-kjsce.somaiya.edu/my", allow_redirects=False)
if r.status_code >= 300:
    user_id = "email"
    password = "password"
    while not logIn(driver, user_id, password):
        user_id = input("Please enter your mail-id:").strip()
        password = input("Please enter your password:").strip()
    print("Logged in")
    subject_url = "https://lms-kjsce.somaiya.edu/course/view.php?id=1411"
    oneSub = getSubject(subject_url)
else:
    print("Logged in")


