from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import time


def find_and_click_element(driver, xpath, max_attempts=10, wait_time=5):
    attempt = 0
    element = None

    while attempt < max_attempts:
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            break
        except:
            attempt += 1
            time.sleep(wait_time)

    if element:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        return True
    else:
        return False
