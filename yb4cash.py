from urllib.parse import urlparse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import random
import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv

dotenv_path = join(dirname(abspath("__file__")), './.env')
load_dotenv(dotenv_path)

mobile_emulation = { "deviceName": "iPhone 8" }
chrome_options = webdriver.ChromeOptions()
# chrome_options.headless = True
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(executable_path="./chromedriver",options=chrome_options)


folder = "./screenshots/"

def fb_login():
    url = "http://www.facebook.com/"
    driver.implicitly_wait(10)
    driver.get(url)

    sleep(random.randint(2,5))

    mail = os.environ.get("FACEBOOK_MAIL")

    pass_ = os.environ.get("FACEBOOK_PASS")

    email = driver.find_element(By.ID, "m_login_email")
    email.send_keys(mail)
    sleep(random.randint(2,5))

    pas = driver.find_element(By.ID, "m_login_password")
    pas.send_keys(pass_)
    sleep(random.randint(2,5))
    
    login = driver.find_element(By.NAME, "login")
    login.click()

    save_login = driver.find_element(By.XPATH, "//*[@id='root']/div[1]/div/div/div[3]/div[2]/form/div/button")
    if save_login:
        sleep(random.randint(2,5))
        save_login.click()

def like(job_url, screenshot_folder=folder):
    driver.get(job_url)
    sleep(random.randint(2,5))

    driver.find_element(By.LINK_TEXT, "Like").click()
    sleep(random.randint(2,5))

    # if path does not exist create
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)
    
    job_desc = urlparse(job_url).path.strip('/')
    screenshot_name = job_desc + "_screenshot" + ".png"
    screenshot_path = os.path.join(screenshot_folder, screenshot_name)
    
    # save screenshot
    driver.save_screenshot(screenshot_path)

def yb_login():
    mail = os.environ.get("YB4CASH_NUMBER")
    pass_ = os.environ.get("YB4CASH_PASS")

    url = "http://www.yb4cash.com/"

    driver.get(url)

    # Check if elements are loaded
    sleep(5)

    # check whether code is present 
    # in case of the user is already connnected 
    # it will not appear
    try:
        codes = driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[2]/form/div[1]/div[1]/i")
        if codes:
            # select 237 as code
            driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[2]/form/div[1]/div[1]/i").click()
            # click cameroon
            driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/span[1]").click()
            # enter username
            username = driver.find_element(By.NAME, "username")
            username.send_keys(mail)
            # enter password
            pas = driver.find_element(By.NAME, "password")
            pas.send_keys(pass_)
            #  click on login
            login = driver.find_element(By.CLASS_NAME, "loginbtn")
            login.click()
    except NoSuchElementException:
        sleep(5)

    # close_first_ad
    # driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[10]/div[2]/i").click()
    # # close_scnd_ad
    # driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[9]/div[2]/i").click()

def get_tasks():
    # task_hall
    driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div[2]/div[1]/img").click()
    # get_jobs
    driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[3]/button").click()
    # get 4 jobs
    for i in range(2, 6):
        driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[2]/div/div/div[2]/div[{}]/div/div[2]/div[1]/div[2]/button".format(i)).click() 
    # go back
    driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[1]/div/div/div/div[1]/i").click()

def get_job_links():
    # go to register jobs
    driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div[4]/div[1]/img").click()
    

    sleep(5)
    action = ActionChains(driver)
    action.key_down(Keys.ARROW_DOWN)
    sleep(5)
    action.key_up(Keys.ARROW_DOWN)
    action.perform()
    # copy links
    item_div = driver.find_elements(By.CLASS_NAME, 'info')
    job_links = [item.find_elements(By.TAG_NAME, 'i')[2].get_attribute("data-text") for item in item_div]
    
    return job_links

def submit_job(job_link):
    # go to register jobs
    driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div[4]/div[1]/img").click()
    # get upload input links
    sleep(5)
    div_boxes = driver.find_elements(By.CLASS_NAME, "card.ar-text")[1:]
    for element in div_boxes:
        div_item = element.find_element(By.CLASS_NAME, 'info')
        i = div_item.find_elements(By.TAG_NAME, 'i')
        if i[2].get_attribute("data-text") == job_link:
            submit_box = element
            upload_button = element.find_element(By.CLASS_NAME, 'btn.van-button.van-button--default.van-button--normal.van-button--block')

    upload = submit_box.find_element(By.CLASS_NAME, 'van-uploader__input')
    url_path = urlparse(job_link).path.strip('/')
    os.chdir(folder)
    screenshots = os.listdir()
    for shot in screenshots:
        if url_path in shot:
            # file_name = shot
            file_path = os.path.abspath(shot)
            upload.send_keys(file_path)
            # click submit    
            upload_button.click()

    os.chdir('..')
        

if __name__ == "__main__":
    fb_login()
    sleep(5)
    yb_login()
    # get_tasks()
    job_urls = get_job_links()
    for link in job_urls:
        print('liking: ', like)
        sleep(random.randint(2,10))
        like(link)

    yb_login()
    for link in job_urls:
        print('submitting_job: ', link)
        submit_job(link)

    # input("press to close")
    # driver.quit()