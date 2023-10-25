from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager

class ImageScraperDriver:
    """
    Generic search engine Image Scraper based on Selenium for firefox
    """

    def __init__(self, images_xpath, selected_image_xpath, show_more_xpaths, search_url, num_images, image_queue, headless, url_blacklist=[], start_at=0):
        self.images_xpath = images_xpath
        self.selected_image_xpath = selected_image_xpath
        self.show_more_xpaths = show_more_xpaths
        self.search_url = search_url

        options = webdriver.ChromeOptions()
        options.add_argument("ignore-certificate-errors")
        options.add_argument("incognito")
        options.add_argument("log-level=3")
        options.add_argument("disable-gpu")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if headless: 
            options.add_argument("headless")

        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.implicitly_wait(2)
        
        self.errors = 0 + start_at
        self.successes = 0 + start_at
        self.total = 0 + start_at
        self.num_images = num_images + start_at

        self.image_queue = image_queue
        self.url_blacklist = url_blacklist
        

    def show_more_check(self, show_more_btn=None):
        """
        Checks if a show more button is visible / clickable when scrolling through images

        Returns:
            True if show more is visible
            False if show more is not visible
        """
        if show_more_btn is None:
            show_more_btn = []
            for show_more in self.show_more_xpaths:
                show_more_btn += self.driver.find_elements(
                    By.XPATH, show_more)            

        for i in range(len(show_more_btn)):
            if show_more_btn[i].is_displayed():
                return i

        return -1

    def click_show_more(self):
        """
        Clicks the show more button

        Returns:
            True if successful in clicking the button
            False if unsuccessful
        """
        show_more_btn = []
        for show_more in self.show_more_xpaths:
            show_more_btn += self.driver.find_elements(
                By.XPATH, show_more)
            
        index = self.show_more_check(show_more_btn)
        if index != -1:
            show_more_btn[index].click()
            print(f"Clicked Show More")
            return True
        else:
            return False

    def scroll_show_more(self):
        """
        scrolls until you hit the show more button
        """
        html = self.driver.find_element(By.TAG_NAME, 'html')

        keep_scrolling = True
        while keep_scrolling:
            html.send_keys(Keys.END)
            keep_scrolling = self.show_more_check() == -1
            print(f"Scrolling...")


    def get_images(self):
        """
        Starts clicking through images and adding them to the image queue
        """

        images = self.driver.find_elements(By.XPATH, self.images_xpath)

        if len(images) <= self.total:
            return True

        for i in range(self.total, len(images)):
            self.total += 1
            try:
                image = images[i]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", image)
                time.sleep(0.1)
                image.click()
                selected_image = self.driver.find_elements(By.XPATH, self.selected_image_xpath)

                image_src = selected_image[0].get_attribute("src")
                print(f"{image_src}")

                if isinstance(image_src, str):
                    if not any(word in image_src for word in self.url_blacklist):
                        self.successes += 1
                        print(f"{self.successes}: {image_src}")
                        self.image_queue.put((self.successes, image_src), block=True)
                    else:
                        print(f"{image_src} was has words in blacklist")
                
            except Exception as e:
                print(f"Error Happened {e}")
                self.errors += 1
            if self.successes >= self.num_images:
                return True
        return False


    def run(self):
        self.driver.get(self.search_url)
        while self.successes < self.num_images:
            print(f"🔎 Loading New Image Page 🔎")
            self.scroll_show_more()
            print(f"🔎 Searching... 🔎")
            if self.get_images():
                break
            self.scroll_show_more()
            self.click_show_more()







# index = 0
# filename = f"{folderpath}/{query}/{index}.jpg"
