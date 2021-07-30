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

# Watch these: https://www.youtube.com/watch?v=wCoTJdhRcQE


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
    total = main.find_element_by_class_name("_33O9dg0j").text.replace("reviews", "")

    hotel_list = []
    hotel = {
        "Property": title.text,
        "Address": address[0],
        "City": address[1],
        "State": "null",
        "Title": driver.title,
        "Url": driver.current_url,
        "Total # of Reviews": total,
    }
    for i in range(2):
        # Get Reviews
        # reviews = driver.find_elements_by_xpath("//div[@class='_2wrUUKlw _3hFEdNs8']")
        reviews = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='_2wrUUKlw _3hFEdNs8']")
            )
        )
        # Toggle Review Details
        # All Element
        test = (
            WebDriverWait(driver, 10)
            .until(EC.element_to_be_clickable((By.XPATH, '//div[@class="XUVJZtom"]')))
            .click()
        )
        # Wait for the reload of element then grab it again
        test = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@class="_1fSlsEgr"]'))
        )
        for review in reviews:
            try:
                location = review.find_element_by_class_name("_1TuWwpYf").text
            except:
                location = "None"

            text = review.find_element_by_tag_name("q").text
            date_of_stay = review.find_element_by_class_name("_34Xs-BQm").text.split(
                ":"
            )[1]

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
            next = (
                WebDriverWait(driver, 10)
                .until(EC.element_to_be_clickable((By.CLASS_NAME, "next")))
                .click()
            )

        df = pd.DataFrame(hotel_list)
    df.to_csv("hotelReviews.csv", index=0, encoding="utf-8")

finally:
    driver.close()
    driver.quit()
