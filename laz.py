from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

url = "https://www.tripadvisor.com.ph/Hotel_Review-g47685-d93179-Reviews-Hampton_Inn_White_Plains_Tarrytown-Elmsford_New_York.html#REVIEWS"

driver = webdriver.Chrome()
driver.get(url)


# search = driver.find_element_by_id('q')
# search.send_keys("graphics card")
# search.send_keys(Keys.RETURN)

try:
    # Get initial Data
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_1lV02aLs")))
    title = main.find_element_by_class_name('_1mTlpMC3')
    address = main.find_element_by_xpath(
        '//div[@class="_3RG_koBJ"]/div/div/div/span[2]')
    address = address.text.split(",")
    total = main.find_element_by_class_name('_33O9dg0j')
    hotel_item = {
        "title": title.text,
        "address": address[0],
        "city": address[1],
        "state": address[2],
        "reviews": total.text

    }
    print(hotel_item)

    # Get Reviews
    reviews = driver.find_elements_by_xpath(
        "//div[@class='_2wrUUKlw _3hFEdNs8']")

    for review in reviews:
        location = review.find_element_by_class_name("_1EpRX7o3")
        location = location.find_element_by_tag_name("span").text
        if "contribution" in location:
            next
        else:
            print(location)
        text = review.find_element_by_tag_name('q').text
        date_of_stay = review.find_element_by_class_name(
            '_34Xs-BQm').text.split(":")[1]

        # Toggle Review Details
        test = WebDriverWait(review, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="XUVJZtom"]')))
        test.click()
        # Wait for the reload of element then grab it again
        test = WebDriverWait(review, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="_1fSlsEgr"]')))

        # trip_type = review.find_element_by_class_name('_2bVY3aT5').text

        # print(trip_type)


finally:
    driver.quit()
