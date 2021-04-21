from bs4 import BeautifulSoup
from selenium import webdriver
import time

def courseDetails(driver: webdriver, url: str):
    driver.get(url)
    time.sleep(7)
    pg = BeautifulSoup(driver.page_source, "lxml")
    temp = pg.find(name="div", attrs={"jsname":"rymPhb"})
    assign, material, text = [], [], []
    print(len(temp.contents))
    for i in temp.contents:
        if len(i["class"]) > 4:
            j = i.contents[0].contents[0].contents
            text = j[2].contents[0].contents[1].contents[0].string.split(": ")[1]
            date = j[2].contents[1].contents[1].string
            if j[0]["aria-label"][0] == "A":
                assign.append([i, text, date])
            else:
                material.append([i, text, date])
    print(assign, material)