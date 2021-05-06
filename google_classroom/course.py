from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import time

def courseDetails(driver: webdriver, url: str):
    driver.get(url)
    #time.sleep(7)
    l = WebDriverWait(driver, timeout = 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div[jsname='rymPhb']")))
    # while not WebDriverWait(driver, timeout=10).until(expected_conditions.element_to_be_clickable(l.find_element_by_tag_name("div"))):
        # time.sleep(2)
    check_height = driver.execute_script("return document.body.scrollHeight;") 
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        height = driver.execute_script("return document.body.scrollHeight;") 
        if height == check_height: 
            break 
        check_height = height
    pg = BeautifulSoup(driver.page_source, "lxml")
    temp = pg.find(name="div", attrs={"jsname":"rymPhb"})
    assign, material, text = [], [], []
    for i in range(len(temp.contents)):
        if len(temp.contents[i]["class"]) > 4:
            j = temp.contents[i].contents[0].contents[0].contents
            text = j[2].contents[0].contents[1].contents[0].string.split(": ")[1]
            date = j[2].contents[1].contents[1].string
            if j[0]["aria-label"][0] == "A":
                assign.append([i, text, date])
            else:
                material.append([i, text, date])
    total = driver.find_elements(By.CSS_SELECTOR, "div[jsname='rymPhb'] > div")
    for i in assign:
        total[i[0]].click()
        time.sleep(3)
        assignment = BeautifulSoup(driver.page_source, "lxml")
        WebDriverWait(driver, timeout = 6).until(expected_conditions.visibility_of(driver.find_elements_by_class_name("W4hhKd")[-1]))
        details = assignment.find_all(name="div", attrs={"class":"W4hhKd"})[-1].contents #make DOM visible  
        i.append(details[1].string) #due date
        if i[-1] is None:
            i[-1] = "No due date"
        #i.append(details[0].contents[0].contents[0].string) #max marks
        if len(details[0].contents) == 0:
            i.append("No marks mentioned")
            i.append("No marks received")
        else:
            temp = details[0].contents[0].contents[0].contents
            if len(temp) > 1:
                i.append(temp[1].string.split()[-1])
                i.append(temp[1].string.split()[0])
            else:
                i.append(temp[0])
                i.append("No marks received")
        details = assignment.find_all(name="aside", attrs={"class":"asCVDb"})[-1].contents[0].contents[0].contents[1].contents[0]
        if details.contents[0].string[0] == 'A':
            i.append(details.contents[0].string + " (Not submitted)")
        else:
            i.append(details.contents[0].string)
        i[0] = driver.current_url
        driver.find_element_by_tag_name("nav").find_element_by_tag_name("div").find_element_by_tag_name("div").find_element_by_tag_name("div").find_element_by_tag_name("h1").find_element_by_tag_name("a").click()
        time.sleep(2)

    for i in material:
        total[i[0]].click()
        time.sleep(2)
        i[0] = driver.current_url
        driver.find_element_by_tag_name("nav").find_element_by_tag_name("div").find_element_by_tag_name("div").find_element_by_tag_name("div").find_element_by_tag_name("h1").find_element_by_tag_name("a").click()
        time.sleep(2)
    return assign, material