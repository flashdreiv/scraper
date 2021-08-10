from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd

url = "https://training.gov.au/Search/SearchOrganisation?nrtCodeTitle=BSB50120&scopeItem=Qualification&tabIndex=1&ImplicitNrtScope=True&orgSearchByScopeSubmit=Search&IncludeUnregisteredRtosForScopeSearch=False"

opts = webdriver.ChromeOptions()
opts.headless = True

driver = webdriver.Chrome(options=opts)
driver.get(url)


try:
    data = []
    for i in range(30):
        body = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@id='gridRtoSearchResults']/table/tbody/tr")
            )
        )

        for tr in body:
            code = tr.find_elements_by_tag_name("td")[0].text or "none"
            name = tr.find_elements_by_tag_name("td")[1].text or "none"
            website = tr.find_elements_by_tag_name("td")[2] or "none"
            website = (
                website.find_element_by_xpath("//child::li").get_attribute("href")
                or "none"
            )
            general_enquiries = tr.find_elements_by_tag_name("td")[3].text or "none"
            registration = tr.find_elements_by_tag_name("td")[4].text or "none"

            item = {
                "Code": code,
                "Name": name,
                "Website": website,
                "General Inquiries": general_enquiries,
                "Registration": registration,
            }

            data.append(item)
        next = (
            WebDriverWait(driver, 10)
            .until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//span[@class="t-icon t-arrow-next"]',
                    )
                )
            )
            .click()
        )
        time.sleep(1)
    df = pd.DataFrame(data)
    df.to_csv("trainings.csv", index=0, encoding="utf-8")

finally:
    driver.quit()
