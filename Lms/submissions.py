from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests, time, os

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def submission(driver, url : str, filePath: str) -> {} : # needs url of submission and file path
    driver.get(url)
    time.sleep(3)
    button = driver.find_element_by_css_selector('div.fp-btn-add')
    actions = ActionChains(driver)
    actions.click(button)
    actions.perform()
    time.sleep(3)
    chooseFileBtn = driver.find_element_by_name("repo_upload_file")
    chooseFileBtn.send_keys(os.path.abspath(filePath))
    # chooseFileBtn.send_keys(Keys.RETURN)
    chooseFileBtn = driver.find_element_by_css_selector('button.fp-upload-btn')
    actions.click(chooseFileBtn)
    actions.perform()
    submitBtn = driver.find_element_by_css_selector('input#id_submitbutton')
    actions.click(submitBtn)
    actions.perform()
    