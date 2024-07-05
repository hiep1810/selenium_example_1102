import os
import random
import time
from dotenv import load_dotenv
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants.post_query_selector import FacebookPostQuerySelector
from utils.driver_setup import setup_driver
from utils.element_interaction import find_and_click_element

class FacebookBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.bot = setup_driver()
        self._login()

    def _login(self):
        self.bot.get("https://www.facebook.com/")
        load_dotenv()

        email_field = self._wait_for_element(By.ID, "email")
        password_field = self._wait_for_element(By.ID, "pass")

        self._type_like_human(email_field, self.email)
        self._type_like_human(password_field, self.password)
        password_field.send_keys(Keys.RETURN)

        if find_and_click_element(self.bot, "//span[contains(text(), \"Always confirm that it's me\")]"):
            print("Element found and clicked!")
        else:
            print("Element not found after 10 attempts")

    def _wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.bot, timeout).until(EC.presence_of_element_located((by, value)))

    @staticmethod
    def _type_like_human(field, text):
        for char in text:
            field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))

    def navigate_to_page(self, page_link, timeout=10):
        self.bot.get(page_link)
        try:
            WebDriverWait(self.bot, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
            print(f"Navigated to {page_link} and waited for div[role=\"feed\"] successfully.")
        except Exception as e:
            print(f"An error occurred while navigating to {page_link} and waiting for div[role=\"feed\"]: {e}")

    def _human_like_mouse_scroll(self, times=1, do_before=None, do_after=None):
        for _ in range(times):
            if do_before:
                do_before()

            scroll_height = self.bot.execute_script("return document.body.scrollHeight")
            sum_height = 0

            while sum_height < scroll_height:
                random_height = random.uniform(50, 100)
                self.bot.execute_script(f"window.scrollBy(0, {random_height})")
                time.sleep(random.uniform(0.05, 0.1))
                sum_height += random_height

            print("Scrolled successfully!")
            time.sleep(2)

            if do_after:
                do_after()

    def extract_data_from_page(self, page_link):
        self.navigate_to_page(page_link)
        do_before, do_after = self._get_feeds_and_write_to_file()
        self._human_like_mouse_scroll(2, do_before, do_after)

    def _get_feeds_and_write_to_file(self):
        original_feed_html = None
        FPQS = FacebookPostQuerySelector

        def do_before():
            nonlocal original_feed_html
            nonlocal FPQS

            original_feed_div = self.bot.find_element(By.CSS_SELECTOR, FPQS.FEED_FIELD)
            original_feed_html = original_feed_div.get_attribute("innerHTML")

        def do_after():
            nonlocal original_feed_html
            nonlocal FPQS

            # Wait for the feed to be updated
            WebDriverWait(self.bot, 10, 1).until(
                lambda d: d.find_element(By.CSS_SELECTOR, FPQS.FEED_FIELD).get_attribute("innerHTML") != original_feed_html
            )

            # Click 'See more' button to show all post's text
            self._click_see_more_button()

            feed = self.bot.find_element(By.CSS_SELECTOR, FPQS.FEED_FIELD)
            posts = feed.find_elements(By.CSS_SELECTOR, ':scope > ' + FPQS.POSTS)

            for post in posts:
                header = post.find_element(By.CSS_SELECTOR, FPQS.POST_HEADER)
                print("=========================HEADER===========================")
                username = header.find_element(By.CSS_SELECTOR, FPQS.POST_HEADER_USERNAME)
                print(username.text)
                print("=========================POST_LINK===========================")
                link_span = post.find_element(By.CSS_SELECTOR, FPQS.POST_HEADER_POST_LINK_SPAN)
                link = link_span.find_element(By.CSS_SELECTOR, 'a')
                print(link.get_attribute('href'))

            self._save_elements_to_file(posts, "exact_match_elements.txt")

        return do_before, do_after

    def _click_see_more_button(self):
        bot = self.bot
        buttons = bot.find_elements(By.CSS_SELECTOR, FacebookPostQuerySelector.POST_HEADER_SEE_MORE)

        for button in buttons:
            try:
                self.bot.execute_script("arguments[0].click();", button)
                print("Clicked a 'See more' button.")
            except Exception as e:
                print(f"An error occurred while clicking 'See more' button: {e}")

    @staticmethod
    def _has_exact_classes(element, classes):
        class_attr = element.get_attribute("class")
        if not class_attr:
            return False
        element_classes = set(class_attr.split())
        specified_classes = set(classes.split())
        return element_classes == specified_classes

    @staticmethod
    def _save_elements_to_file(elements, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            for element in elements:
                file.write(f"{element.tag_name}: {element.text}\n")
                file.write("====================================================\n")
