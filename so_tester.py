from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, random

url = "http://222.127.1.115:8081/"

opts = webdriver.ChromeOptions()
# opts.headless = True

driver = webdriver.Chrome()

driver.get(url)


time.sleep(1)

username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")

username.send_keys("dreivan.orprecio")
password.send_keys("aljay123")

username.send_keys(Keys.ENTER)


shit = (
    WebDriverWait(driver, 10)
    .until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='navbar-toggler sidenav-toggler ml-auto']")
        )
    )
    .click()
)

cs_module = (
    WebDriverWait(driver, 10)
    .until(EC.element_to_be_clickable((By.XPATH, "//li[@class='nav-item']/a[1]")))
    .click()
)

so = (
    WebDriverWait(driver, 10)
    .until(
        EC.element_to_be_clickable((By.XPATH, "//ul[@class='nav nav-collapse']/li/a"))
    )
    .click()
)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-target='#addRowModal']"))
).click()

time.sleep(1)
distribution = driver.find_element_by_xpath("//span[@title='***Select Distibution***']")
distribution.click()
distribution = driver.find_element_by_xpath("//span[@class='select2-results']/ul/li[2]")
distribution.click()

docno = driver.find_element_by_xpath("//input[@id='docno']")
docno.send_keys("5002")

time.sleep(1)
customer = driver.find_element_by_xpath("//span[@title='***Select Customer***']")
customer.click()
rand_customer = random.randint(2, 1000)
customer = driver.find_element_by_xpath(
    f"//span[@class='select2-results']/ul/li[{rand_customer}]"
)
customer.click()


product_type = driver.find_element_by_xpath(
    "//span[@title='***Select Product Type***']"
)
product_type.click()
rand_prod_type = random.randint(2, 3)
product_type = driver.find_element_by_xpath("//span[@class='select2-results']/ul/li[2]")
product_type.click()

time.sleep(0.5)
price_category = driver.find_element_by_xpath(
    "//span[@title='***Select Price Category***']"
)
price_category.click()
price_category = driver.find_element_by_xpath(
    "//span[@class='select2-results']/ul/li[2]"
)
price_category.click()

terms = driver.find_element_by_xpath("//span[@title='***Select Terms***']")
terms.click()
rand_terms = random.randint(2, 6)
terms = driver.find_element_by_xpath("//span[@class='select2-results']/ul/li[2]")
terms.click()

discount = driver.find_element_by_xpath("//span[@title='***Select Discount***']")
discount.click()
discount = driver.find_element_by_xpath("//span[@class='select2-results']/ul/li[2]")
discount.click()

percent = driver.find_element_by_id("percent")
rand_percent = random.randint(0, 50)
percent.send_keys(rand_percent)

# btn add prduct

add_product = driver.find_element_by_id("btnAdd")
y = random.randint(0, 4)
for i in range(0, y):
    add_product.click()

time.sleep(1)
products = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//div[contains(@id,'row_')]/div[1]")
    )
)

for product in products:
    try:
        drop_down = WebDriverWait(product, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[@title='***Select Product***']")
            )
        )
        drop_down.click()
        rand_product = random.randint(2, 8)
        z = drop_down.find_element_by_xpath(
            f"//span[@class='select2-results']/ul/li[{rand_product}]"
        ).click()

        qty = product.find_element_by_xpath(
            f"//input[@id='quantity_{products.index(product)}']"
        )
        rand_qty = random.randint(0, 100)
        qty.send_keys(rand_qty)
        time.sleep(0.1)
        price = driver.find_element_by_xpath(
            f"//input[@id='price_{products.index(product)}']"
        )
        price.clear()
        rand_price = random.randint(10, 1000)
        price.send_keys(rand_price)
        time.sleep(0.1)
    except:
        break


compute = driver.find_element_by_id("totalCompute")
compute.click()


remarks = driver.find_element_by_id("remarksid")
remarks.send_keys("Automated testing")

submit = driver.find_element_by_id("SavedSalesOrder")
submit.click()
time.sleep(0.1)
time.sleep(10)
driver.quit()
