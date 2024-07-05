from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from config.settings import WINDOW_USER_DATA


def setup_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_argument(f"user-data-dir={WINDOW_USER_DATA}")
        # chrome_options.add_argument(r'--profile-directory=Default')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        return driver
    except Exception as e:
        print(f"An error occurred while setting up the driver: {e}")
        return None