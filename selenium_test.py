import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure the WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--window-size=1920,1080')

# Initialize the WebDriver (using Chrome in this example)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Start the timer
start_time = time.time()

# Navigate to the desired page (e.g., a Reddit post)
driver.get('https://www.reddit.com/r/TelegramBots/comments/1da8xly/comment/l7j47dr/')


class Comment:
    def __init__(self, author, comment, sub_comments):
        self.author = author
        self.comment = comment
        self.sub_comments = self._parse_sub_comments(sub_comments)

    @staticmethod
    def _parse_sub_comments(sub_comments):
        """
        Recursively parse the sub-comments and create a list of `Comment` objects.
        """
        comments = []
        for sub_comment in sub_comments:
            author_name = sub_comment.get_property("author")
            comment_content = sub_comment.find_element(By.CSS_SELECTOR, "div[slot='comment']").text
            sub_sub_comments = sub_comment.find_elements(By.CSS_SELECTOR, "shreddit-comment")
            _comment = Comment(author_name, comment_content, sub_sub_comments)

            comments.append(_comment)
        return comments

    def to_dict(self):
        """
        Convert the `Comment` object to a dictionary.
        """
        return {
            "author_name": self.author,
            "comment_content": self.comment,
            "sub_comments": [sub_comment.to_dict() for sub_comment in self.sub_comments]
        }


try:
    # Wait for the element with class 'shreddit-comment' to appear
    elements = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'shreddit-comment-tree'))
    )

    comments = driver.find_elements(By.CSS_SELECTOR, "shreddit-comment")

    for comment in comments:
        author = comment.get_property("author")
        comment_content = comment.find_element(By.CSS_SELECTOR, "div[slot='comment']").text
        sub_comments = comment.find_elements(By.CSS_SELECTOR, "shreddit-comment")
        _comment = Comment(author, comment_content, sub_comments)

        print(_comment.to_dict())

finally:
    # End the timer
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total running time: {total_time:.2f} seconds")


    # Close the WebDriver
    driver.quit()
