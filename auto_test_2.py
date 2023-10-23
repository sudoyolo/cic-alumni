from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_signin():
    browser = webdriver.Chrome()
    browser.get('http://127.0.0.1:5000/')
    time.sleep(1)
    signin = browser.find_element(By.CLASS_NAME, 'nav-item')
    signin.click()
    time.sleep(1)
    name = browser.find_element(By.ID, 'name')
    name.send_keys('Harshvir Sandhu')
    mail = browser.find_element(By.ID, 'mail')
    mail.send_keys('harshvir2173@gmail.com')
    year = browser.find_elements(by=By.TAG_NAME, value='option')
    # print(year)
    year[-1].click()
    browser.find_element(by=By.TAG_NAME, value='button').click()
    time.sleep(5)
    browser.find_element(By.ID, 'name').send_keys('Harshvir Sandhu')
    browser.find_element(By.ID, '\'otp').send_keys('00000')
    browser.find_element(By.TAG_NAME, 'button').click()
    time.sleep(5)


def test_cards():
    browser = webdriver.Chrome()
    browser.get('http://127.0.0.1:5000/')
    time.sleep(1)
    options = browser.find_elements(by=By.TAG_NAME, value='option')
    years = options[5:]
    for i in range(len(years)):
        options = browser.find_elements(by=By.TAG_NAME, value='option')
        courses = options[1:4]
        years = options[5:]
        time.sleep(2)
        courses[0].click()
        years[i].click()
        year = years[i].text
        time.sleep(2)
        browser.find_element(By.CLASS_NAME, 'submit').click()
        jobs = browser.find_elements(By.CLASS_NAME, 'occup')
        names = browser.find_elements(By.CLASS_NAME, 'name')
        details = browser.find_elements(By.CLASS_NAME, 'details')
        for name, job, detail in zip(names, jobs, details):
            # print(name.text, ' --- ', job.text, ' --- ', year, ' --- ', detail.text) # prints email, location, etc; takes time
            print(name.text, ' --- ', job.text, ' --- ', year)
        browser.refresh()

test_signin()
test_cards()