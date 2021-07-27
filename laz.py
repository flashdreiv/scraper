from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

url = "https://www.tripadvisor.com.ph/Hotel_Review-g47685-d93179-Reviews-Hampton_Inn_White_Plains_Tarrytown-Elmsford_New_York.html#REVIEWS"

driver = webdriver.Chrome()
driver.get(url)


try:
    # Get initial Data
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_1lV02aLs"))
    )
    title = main.find_element_by_class_name("_1mTlpMC3")
    address = main.find_element_by_xpath(
        '//div[@class="_3RG_koBJ"]/div/div/div/span[2]'
    )
    address = address.text.split(",")
    total = main.find_element_by_class_name("_33O9dg0j")

    # Get Reviews
    reviews = driver.find_elements_by_xpath(
        "//div[@class='_2wrUUKlw _3hFEdNs8']")
    review_list = []
    headers = title.text + "," + \
        address[0] + "," + address[1] + "," + total.text

    for review in reviews:
        location = review.find_element_by_class_name("_1EpRX7o3")
        location = location.find_element_by_tag_name("span").text
        if "contribution" in location:
            location = "None"
        text = review.find_element_by_tag_name("q").text
        date_of_stay = review.find_element_by_class_name(
            "_34Xs-BQm").text.split(":")[1]

        # Toggle Review Details
        test = WebDriverWait(review, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="XUVJZtom"]'))
        )
        try:
            test.click()
        except:
            pass
        # Wait for the reload of element then grab it again
        test = WebDriverWait(review, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[@class="_1fSlsEgr"]'))
        )
        trip_type = ""
        room_tip = ""
        try:
            trip_type = review.find_element_by_class_name("_2bVY3aT5").text
            room_tip = review.find_element_by_class_name("_1Dn9wASK").text
        except:
            trip_type = "none"
            room_tip = "none"

        review_item = {
            "location": location,
            "review": text,
            "Date of Stay": date_of_stay,
            "Trip Type": trip_type,
            "Room Tip": room_tip,
        }

        review_list.append(review_item)

    df = pd.DataFrame(review_list)
    df.to_csv("hotelReviews.csv", index=1)


finally:
    driver.quit()
