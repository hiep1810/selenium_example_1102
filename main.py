from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from config.settings import EMAIL, PASSWORD
from utils.driver_setup import setup_driver
from utils.login import login_to_facebook
from utils.element_interaction import find_and_click_element
import time

from utils.navigation import navigate_to_page


def has_exact_classes(element, classes):
    """
    Check if an element has only the specified classes and no others.

    Args:
        element (WebElement): The element to check.
        classes (str): A space-separated string of class names.

    Returns:
        bool: True if the element has only the specified classes, False otherwise.
    """
    # Get the element's class attribute
    class_attr = element.get_attribute("class")

    # If the class attribute is None, return False
    if class_attr is None:
        return False

    # Split the class names into a list
    element_classes = class_attr.split()
    specified_classes = classes.split()

    # Check if the length of the two lists is the same and if every specified class is in the element's class list
    return len(element_classes) == len(specified_classes) and all(cls in element_classes for cls in specified_classes)


def human_like_scroll_to_bottom(driver, scroll_pause_time=0.5, scroll_height=300, times=10):
    """
    Scrolls the page in a more human-like manner.

    :param driver: The WebDriver instance.
    :param scroll_pause_time: Time in seconds to wait between each scroll action.
    :param scroll_height: The height in pixels to scroll each time.
    :param times: The number of times to perform the scroll action.
    """
    for _ in range(times):
        # Scroll down by a portion of the page
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")

        # Wait for the page to load more content
        time.sleep(scroll_pause_time)


def get_total_scroll_height(driver):
    """
    Returns the current scroll height of a web page.

    :param driver: The WebDriver instance.
    :return: The current scroll height in pixels.
    """
    total_scroll_height = driver.execute_script("return document.documentElement.scrollHeight;")
    return total_scroll_height


def get_current_scroll_position(driver):
    """
    Returns the current vertical scroll position of a web page.

    :param driver: The WebDriver instance.
    :return: The current vertical scroll position in pixels.
    """
    # Retrieve the current vertical scroll position
    current_scroll_position = driver.execute_script("return window.scrollY;")

    return current_scroll_position


def check_auto_navigation(driver, expected_url, timeout=10):
    """
    Checks if the page automatically navigates away from the expected URL.

    :param driver: The WebDriver instance.
    :param expected_url: The expected URL to remain at.
    :param timeout: The maximum time to wait to check for auto-navigation.
    :return: True if the page navigated away, False otherwise.
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.current_url != expected_url
        )
        print(f"Page auto-navigated to {driver.current_url}")
        return True
    except:
        print(f"Page did not auto-navigate and remains at {expected_url}")
        return False


def save_elements_to_file(elements, file_path):
    """
    Save the text content of elements to a file.

    :param elements: List of WebElement objects.
    :param file_path: The path of the file where content will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for element in elements:
            file.write(f"{element.tag_name}: {element.text}\n")
            file.write("====================================================\n")


def click_see_more_button(driver):
    """
    Clicks the 'See more' buttons if found within the elements.

    :param driver: The WebDriver instance.
    :return: The number of 'See more' buttons clicked.
    """
    see_more_buttons = driver.find_elements(By.CSS_SELECTOR,
                                            'div.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.xzsf02u.x1s688f[role="button"][tabindex="0"]'
                                            )

    clicked_count = 0

    for button in see_more_buttons:
        try:
            driver.execute_script("arguments[0].click();", button)
            clicked_count += 1
            print("Clicked a 'See more' button.")
        except Exception as e:
            print(f"An error occurred while clicking 'See more' button: {e}")

    return clicked_count

def main():
    driver = setup_driver()

    login_to_facebook(driver, EMAIL, PASSWORD)

    element_xpath = "//span[contains(text(), \"Always confirm that it's me\")]"

    if find_and_click_element(driver, element_xpath):
        print("Element found and clicked!")
    else:
        print("Element not found after 10 attempts")

    navigate_to_page(driver,  "https://www.facebook.com/groups/nghienshoppingviet/?sorting_setting=CHRONOLOGICAL", 'div[role="feed"]')


    # Find the div element with role="feed"
    feed_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

    human_like_scroll_to_bottom(driver, scroll_pause_time=1, scroll_height=get_total_scroll_height(driver), times=3)
    elements = feed_div.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')
    exact_match_elements = [elem for elem in elements if has_exact_classes(elem, "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")]

    # Check and click 'See more' button if found
    click_see_more_button(driver)
    elements = feed_div.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')
    exact_match_elements = [elem for elem in elements if has_exact_classes(elem, "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")]

    # Save the exact match elements to a file
    save_elements_to_file(exact_match_elements, "exact_match_elements.txt")

    time.sleep(500)

    driver.quit()


if __name__ == "__main__":
    main()
