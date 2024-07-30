from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

import os
import time
import pandas as pd
import getpass

home_url = 'https://www.linkedin.com/login'

mail = input('LinkedIn Email/Username: ')
password = getpass.getpass('LinkedIn Password: ')
    
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)
job_data = []


driver.get(home_url)
driver.implicitly_wait(5)

driver.find_element(By.XPATH, "//input[@type = 'text']").send_keys(mail)
driver.find_element(By.XPATH, "//input[@type = 'password']").send_keys(password)
driver.find_element(By.XPATH,"//button[@class='btn__primary--large from__button--floating']").click()
keyword = input('Enter the Keyword: ')
location = input('Enter the Location: ')
url = f'https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}'

driver.get(url)

def scrape_job():
    jobs = driver.find_elements(By.XPATH, "//ul[@class='scaffold-layout__list-container']/li")

    for job in jobs:
        driver.execute_script("arguments[0].scrollIntoView();", job)
        time.sleep(1)
        try:
            job_title = driver.find_element(By.XPATH,"//h1[@class='t-24 t-bold inline']").text
        except:
            job_title = None
        try:
            company_name = driver.find_element(By.XPATH, "//div[@class='job-details-jobs-unified-top-card__company-name']").text
        except:
            company_name = None
        try:
            posted_on = driver.find_element(By.XPATH,"//div[1]//div[1]//main[1]//div[1]//div[2]//div[2]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//div[1]//div[1]//div[1]//div[3]//div[1]//span[3]").text
        except:
            posted_on = None
        try:
            num_app = driver.find_element(By.XPATH,"//div[1]//div[1]//main[1]//div[1]//div[2]//div[2]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//div[1]//div[1]//div[1]//div[3]//div[1]//span[5]").text
        except:
            num_app = None
        try:
            job_link = driver.find_element(By.XPATH, "//a[@class = 'disabled ember-view job-card-container__link job-card-list__title job-card-list__title--link']").get_attribute("href")
        except:
            job_link = None

        job_data.append({
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'Posted On': posted_on,
            'Number of Applicants': num_app,
            'Link': job_link
        })

def next_page(driver):
    try:
        next_button = driver.find_element(By.XPATH, "//button[@class = 'artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view jobs-search-pagination__button jobs-search-pagination__button--next']")
        next_button.click()
        time.sleep(2)
        return True
    except:
        return False
    
def start_scraping():
    while True:
        try:
            scrape_job()
            if not next_page(driver):
                break
            
        except (StaleElementReferenceException, TimeoutException):
            # If an exception occurs, refresh the elements and retry
            print("Encountered StaleElementReferenceException, retrying...")
            time.sleep(2)
            continue

        except Exception as e:
            print(f"An error occurred: {e}")
            break
        
    driver.quit()
            
    df = pd.DataFrame(job_data)
    df.to_csv('filtered_list.csv', index = False)

start_scraping()