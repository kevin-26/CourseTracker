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
                        if activity.find_element_by_tag_name("form").find_element_by_tag_name("img").get_attribute("alt")[0] == 'C':
                            ref_data["submission"] = "Submitted"
                        else:
                            ref_data["submission"] = "Not submitted"
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
    
    for j, k in subject_data.items():
        for z in k[1:]:
            details = list(z.items())[0][1]
            if details.get("is_resource") == 0:
                driver.get(details["url"])
                table = WebDriverWait(driver, timeout=10).until(expected_conditions.visibility_of(driver.find_element_by_class_name("generaltable")))
                temp = table.find_elements_by_tag_name("tr")
                grade = temp[1].find_element_by_tag_name("td").text
                if grade[0] == "N":
                    details["max_marks"] = "Not mentioned"
                    details["marks_received"] = "No marks received"
                else:
                    details["max_marks"] = grade
                    details["marks_received"] = grade
                details["due_date"] = temp[2].find_element_by_tag_name("td").text
    return subject_data