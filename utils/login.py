from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import random


def login_to_facebook(driver, email, password):
    driver.get("https://www.facebook.com/")

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pass"))
    )

    for char in email:
        email_field.send_keys(char)
        time.sleep(random.uniform(0.01, 0.05))

    for char in password:
        password_field.send_keys(char)
        time.sleep(random.uniform(0.01, 0.05))

    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
