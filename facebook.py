from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import random


driver = webdriver.Firefox()
driver.implicitly_wait(10)

def fb_login():
    url = "http://www.facebook.com/"

    driver.get(url)

    sleep(random.random(2,5))

    mail = "mail_here"
    pass_= 'password_here'

    email = driver.find_element(By.ID, "email")
    email.send_keys(mail)
    sleep(random.random(2,5))

    pas = driver.find_element(By.ID, "pass")
    pas.send_keys(pass_)
    sleep(random.random(2,5))
    
    login = driver.find_element(By.NAME, "login")
    login.click()

    sleep(random.random(2,5))

def like(url):
    driver.get(url)
    sleep(random.random(2,5))

    driver.find_element(By.XPATH, "//*[@id='watch_feed']/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div[1]").click()
    sleep(random.random(2,5))

    screenshot_name = url + "_screenshot" + ".png"
    driver.save_screenshot(screenshot_name)

input("press to close")
driver.quit()
