from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time

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

    hotel_list = []
    hotel = {
        "Property": title.text,
        "Address": address[0],
        "City": address[1],
        "State": "null",
        "Title": driver.title,
        "Url": driver.current_url,
        "Total # of Reviews": total.text,
    }
    for i in range(3):
        # Get Reviews
        reviews = driver.find_elements_by_xpath("//div[@class='_2wrUUKlw _3hFEdNs8']")
        for review in reviews:
            try:
                location = review.find_element_by_class_name("_1TuWwpYf").text
            except:
                location = "None"

            text = review.find_element_by_tag_name("q").text
            date_of_stay = review.find_element_by_class_name("_34Xs-BQm").text.split(
                ":"
            )[1]

            # Toggle Review Details
            # All Element
            test = WebDriverWait(review, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="XUVJZtom"]'))
            )
            try:
                test.click()
            except:
                pass
            # Wait for the reload of element then grab it again
            test = WebDriverWait(review, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="_1fSlsEgr"]'))
            )
            trip_type = ""
            room_tip = ""
            try:
                trip_type = review.find_element_by_class_name("_2bVY3aT5").text
            except:
                trip_type = "none"
            try:
                room_tip = review.find_element_by_class_name("_1Dn9wASK").text
                room_tip = room_tip.replace("Room Tip:", "")
            except:
                room_tip = "none"

            overall_rating = review.find_element_by_class_name("nf9vGX55")
            overall_rating = overall_rating.find_element_by_tag_name(
                "span"
            ).get_attribute("class")
            overall_rating = int(
                overall_rating.replace("ui_bubble_rating bubble_", "")[0]
            )

            rating_details = review.find_elements_by_class_name("_3ErKuh24")
            # Rate Types
            rate_types = {}
            for details in rating_details:
                label = details.text
                rate = details.find_element_by_xpath('//span[@class="_3-8hSrXs"]/span')
                rate = rate.get_attribute("class").replace(
                    "ui_bubble_rating bubble_", ""
                )[0]
                rate_types[label] = rate

            review_item = {
                "location": location,
                "review": text,
                "Date of Stay": date_of_stay,
                "Trip Type": trip_type,
                "Room Tip": room_tip,
                "Overall Rating": overall_rating,
            }

            hotel.update(review_item)
            hotel.update(rate_types)
            hotel_list.append(hotel)
        next = driver.find_element_by_class_name("next")
        next.click()
        time.sleep(10)

    df = pd.DataFrame(hotel_list)
    df.to_csv("hotelReviews.csv", index=0, encoding="utf-8")

finally:
    driver.quit()
