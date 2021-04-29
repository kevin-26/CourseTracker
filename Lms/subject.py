from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests, time


def getSubject(driver, url : str) -> {} :
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
    return subject_data