import login, subject, requests, time, getpass
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(executable_path=r"../chromedriver.exe")
r = requests.get("https://lms-kjsce.somaiya.edu/my", allow_redirects=False)
if r.status_code >= 300:
    user_id = input("Please enter your mail-id:").strip()
    # "kevin26@somaiya.edu"
    password = getpass.getpass(prompt='Please enter your password: ', stream=None).strip()
    while not login.logIn(driver, user_id, password):
        user_id = input("Please enter your mail-id:").strip()
        password = getpass.getpass(prompt='Please enter your password: ', stream=None).strip()
        # password = input("Please enter your password:").strip()
    print("Logged in")
else:
    print("Logged in")
    
time.sleep(3)
a = WebDriverWait(driver, timeout = 5).until(expected_conditions.visibility_of_element_located((By.ID, "paging-control-limit-container-1")))
a.find_element_by_tag_name("button").click()
a.find_elements_by_tag_name('a')[2].click()
l = login.getCourseList(driver)
print(l)
for i in l:
    print(subject.getSubject(driver, i))