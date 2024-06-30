from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def navigate_to_page(driver, url, wait_for_selector, timeout=10):
    driver.get(url)
    try:
        # Wait for a specific element that signifies the page has fully loaded
        # The 'wait_for_selector' parameter should be a CSS selector string for the element you want to wait for
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_selector))
        )
        print(f"Navigated to {url} and waited for {wait_for_selector} successfully.")
    except Exception as e:
        print(f"An error occurred while navigating to {url} and waiting for {wait_for_selector}: {e}")