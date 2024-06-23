from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Set up the WebDriver (replace the path with the location of your chromedriver)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to the Facebook login page
driver.get("https://www.facebook.com/")

# Find the email and password input fields
email_field = driver.find_element(By.ID, "email")
password_field = driver.find_element(By.ID, "pass")

# Enter the email and password
email_field.send_keys("xxx")
password_field.send_keys("yyy")

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load after login
time.sleep(50)

# Close the browser
driver.quit()