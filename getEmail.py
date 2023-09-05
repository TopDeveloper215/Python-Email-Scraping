import pandas as pd
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from getExistingCSV import getExistingCSV
import time


url = "https://arbetsformedlingen.se/platsbanken/annonser"


def get_data(url):
    browser_options = ChromeOptions()
    browser_options.headless = False

    driver = Chrome(options=browser_options)
    job_driver = Chrome(options=browser_options)
    driver.get(url)
    driver.implicitly_wait(10)


    data = []
    startID = getExistingCSV()["total_row_count"] + 1
    existingCSVFileCount = getExistingCSV()["num_csv"]
    print(startID, existingCSVFileCount)
    profession_selection_dropdown_toggle = driver.find_element(
        By.ID, "option-yrkedropdown-toggle")
    profession_selection_dropdown_toggle.click()
    profession_categories = driver.find_elements(
        By.CLASS_NAME, "option-groups-list")[0].find_elements(By.TAG_NAME, "li")
    profession_selection_dropdown_toggle.click()
    # job_categories = driver.find_elements(By.CLASS_NAME, "link-wrapper")

    for category_index in range(len(profession_categories)):
        if category_index < existingCSVFileCount:
            continue
        profession_selection_dropdown_toggle = driver.find_element(
            By.ID, "option-yrkedropdown-toggle")
        profession_selection_dropdown_toggle.click()
        tmp_profession_categories = driver.find_elements(
        By.CLASS_NAME, "option-groups-list")[0].find_elements(By.TAG_NAME, "li")
        tmp_profession_categories[category_index].click()
        sub_categories = driver.find_elements(
            By.CLASS_NAME, "col-options")[0].find_elements(By.TAG_NAME, "label")
        profession_selection_dropdown_toggle.click()
        for index in range(len(sub_categories)):
            if index == 0:
                continue
            print(index, "th subcategory")
            profession_selection_dropdown_toggle = driver.find_element(
            By.ID, "option-yrkedropdown-toggle")
            profession_selection_dropdown_toggle.click()
            clear_button = driver.find_elements(By.CLASS_NAME, "clear-filter-btn")[0]
            clear_button.click()
            tmp_profession_categories = driver.find_elements(
            By.CLASS_NAME, "option-groups-list")[0].find_elements(By.TAG_NAME, "li")
            tmp_profession_categories[category_index].click()
            tmp_sub_categories = driver.find_elements(
            By.CLASS_NAME, "col-options")[0].find_elements(By.TAG_NAME, "label")
            tmp_sub_categories[index].click()
            profession_selection_dropdown_toggle.click()

            print("Get total pages for each category", index)
            try:
                total_pages = int(driver.find_elements(
                By.CLASS_NAME, 'digi-navigation-pagination__page-button--last')[0].find_elements(By.CLASS_NAME, 'digi-navigation-pagination__page-text')[0].get_attribute('innerHTML'))
            except:
                total_pages = len(driver.find_elements(By.CLASS_NAME, "digi-navigation-pagination__page-text"))
                print('less than 6', index)
                if total_pages == 0:
                    total_pages = 1
                    
            print(total_pages, index,'totalpages')

            for page in range(total_pages):
                print(page, 'page')
                jobs_per_page = driver.find_elements(
                    By.CLASS_NAME, "header-container")
                print(len(jobs_per_page))
                for job in jobs_per_page:
                    job_url = job.find_elements(By.TAG_NAME, 'a')[
                        0].get_attribute('href')
                    job_driver.get(job_url)
                    job_driver.implicitly_wait(10)
                    column = {
                        "No": len(data) + startID,
                        "JobLink": job_url,
                        "Contact Info": ''
                    }
                    try:
                        contact_info = job_driver.find_elements(By.CLASS_NAME, 'dont-break-out')[
                            0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('innerHTML')
                        if '<' in contact_info:
                            column['Contact Info'] = contact_info.split(
                                '<')[0] + contact_info.split('>')[1]
                        else:
                            column['Contact Info'] = contact_info
                    except:
                        try:
                            column['Contact Info'] = job_driver.find_elements(
                                By.CLASS_NAME, 'application-info')[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                        except:
                            try:
                                column['Contact Info'] = job_driver.find_elements(
                                    By.CLASS_NAME, 'application-info')[0].find_elements(
                                    By.CLASS_NAME, 'break-word')[0].get_attribute('innerHTML')
                            except:
                                continue
                    print(column)
                    data.append(column)
                if page < total_pages-1 :
                    current_url = driver.current_url
                    current_url = current_url.split("&page=")[0]
                    print(current_url)
                    driver.get(current_url + '&page=' + str(page+2))
                    driver.implicitly_wait(10)
        export_csv(data, category_index+1)
        startID = startID + len(data)
        data = []

    driver.quit()
    return data


def export_csv(data, index):
    df = pd.DataFrame(data)
    # Apply transformations if needed
    df.to_csv("contact_info"+str(index)+'.csv', index=False)
    print(df)  # DEBUG


def main():
    data = get_data(url=url)
    print('DONE')


if __name__ == '__main__':
    main()
