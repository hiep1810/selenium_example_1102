from selenium import webdriver
import time

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Example usage
if __name__ == "__main__":
    # Initialize the WebDriver (in this example, using Chrome)
    driver = webdriver.Chrome()

    try:
        # Navigate to a web page
        driver.get("https://example.com")

        # Wait for the page to load (optional, depending on the page)
        time.sleep(2)

        # Call the function to scroll to the bottom of the page
        scroll_to_bottom(driver)

        # Wait to observe the scroll effect (optional)
        time.sleep(2)
    finally:
        # Clean up and close the browser window
        driver.quit()