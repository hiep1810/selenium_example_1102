from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the WebDriver using ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to the Facebook login page
driver.get("https://www.facebook.com/")

# Find the email and password input fields
email_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "email"))
)
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "pass"))
)

# Enter the email and password
email_field.send_keys("xxxx")
password_field.send_keys("yyyy")

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load after login
time.sleep(5)

# Define the XPath expression to find the target element
xpath = "//span[contains(text(), \"Always confirm that it's me\")]"

# Try finding the element up to 10 times
max_attempts = 10
attempt = 0
element = None

while attempt < max_attempts:
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        break
    except:
        attempt += 1
        time.sleep(5)  # Wait for 5 second before the next attempt

# Check if the element was found and interact with it
if element:
    # Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # Use ActionChains to move to the element and click it
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()
    print("found and clicked!")
else:
    print("Element not found after 10 attempts")

# Wait for some time to observe the result
time.sleep(5)

# Close the browser
driver.quit()
