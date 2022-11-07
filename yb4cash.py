from urllib.parse import urlparse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import schedule
from time import sleep
import random
import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv

dotenv_path = join(dirname(abspath("__file__")), './.env')
load_dotenv(dotenv_path)

mobile_emulation = { "deviceName": "iPhone 8" }
chrome_options = webdriver.ChromeOptions()
# uncomment this to run the browser in headless mode (background)
# chrome_options.headless = True
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.implicitly_wait(30)

folder = "./screenshots/"

def fb_login():
    url = "http://www.facebook.com/"
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
    sleep(5)

    save_login = driver.find_element(By.XPATH, "//*[@id='root']/div[1]/div/div/div[3]/div[2]/form/div/button")
    if save_login:
        sleep(random.randint(2,5))
        save_login.click()
    
    sleep(random.randint(3,5))

def like(job_url, screenshot_folder=folder):
    driver.get(job_url)
    sleep(20)
    print('liking: ', job_url)
    while True:
        try:
            driver.find_element(By.LINK_TEXT, "Like").click()
        except NoSuchElementException:
            driver.find_element(By.XPATH, "//*[@id='screen-root']/div/div[2]/div[6]/div[6]/div[1]").click()
        except:
            break
        sleep(random.randint(3,5))
        
        print('Done')

        # if path does not exist create
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        
        # split job url
        job_desc = urlparse(job_url).path.strip('/')
        if 'reel' in job_desc:
            job_desc = job_desc.split('/')[1]
        
        screenshot_name = job_desc + "_screenshot" + ".png"
        screenshot_path = os.path.join(screenshot_folder, screenshot_name)
        
        # save screenshot
        print('Saving...')
        driver.save_screenshot(screenshot_path)
        sleep(random.randint(2,5))
        print('Done')

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
            sleep(5)
    except NoSuchElementException:
        sleep(5)

def get_tasks():
    sleep(3)
    # task_hall
    driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div[2]/div[1]/img").click()
    sleep(3)
    # get_jobs
    driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[3]/button").click()
    
    sleep(5)
    # get 4 jobs
    # simply change the initial 1 + the amount of jobs you want
    # the bot to do
    # to do 4 jobs -> 1 + 4 = 5
    for i in range(1, 3):
        print('get task', i)
        driver.find_elements(By.TAG_NAME, "button")[i].click() 
        sleep(1)
    
    sleep(2)
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
    sleep(random.randint(2,5))
    # go to register jobs
    driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div[4]/div[1]/img").click()
    # get upload input links
    sleep(3)
    div_boxes = driver.find_elements(By.CLASS_NAME, "card.ar-text")[1:]
    for element in div_boxes:
        div_item = element.find_element(By.CLASS_NAME, 'info')
        i = div_item.find_elements(By.TAG_NAME, 'i')
        if i[2].get_attribute("data-text") == job_link:
            submit_box = element

    upload = submit_box.find_element(By.CLASS_NAME, 'van-uploader__input')
    url_path = urlparse(job_link).path.strip('/')
    if 'reel' in job_link:
        url_path = url_path.split('/')[1]
    os.chdir(folder)
    screenshots = os.listdir()
    print('submitting_job: ', job_link)
    for shot in screenshots:
        if url_path in shot:
            file_path = os.path.abspath(shot)
            upload.send_keys(file_path)
            # click submit    
    
    sleep(5)
    #click submit
    submit_box.find_element(By.TAG_NAME, 'button').click()

    os.chdir('..')
    print('Done...')
    sleep(5)
        
def main():
    yb_login()
    #get_tasks()
    job_urls = get_job_links()
    
    fb_login()
    sleep(2)
    #for link in job_urls:
    #    sleep(2) 
    like(job_urls[-1])
    # yb_login()
    # for link in job_urls:
    #    submit_job(link)

    #this should be uncommented to close the browser
    driver.quit()

#time_list = ["10:30", "15:25", "12:10", "08:50", "13:40", "18:50", "16:20"]
#time_today = random.choice(time_list)
#schedule.every().day.at(time_today).do(main)

#while True:
#    schedule.run_pending()
#    time.sleep(1)
#    time_today = random.choice(time_list)

if __name__ == "__main__":
    main()
