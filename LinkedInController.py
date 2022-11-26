# import web driver, datetime, tqdm and own settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import settings

class LinkedInController:
    def __init__(self):
        """
        This function initializes the driver.
        """
        # create a new Chrome session
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def login(self, username, password):
        """
        This function logs into the linkedin account.
        Parameters:
            email: The email of the linkedin account.
            password: The password of the linkedin account.
        """
        # driver.get method() will navigate to a page given by the URL address
        self.driver.get('https://www.linkedin.com')
        print(datetime.now(), '/n Enter linkedin website\n')

        # locate email form by_class_name and fill in email
        self.driver.find_element("id", "session_key").send_keys(username)
        print(datetime.now(), ' Find username field and enter in username...\n')

        # locate password form by_class_name and fill in password
        self.driver.find_element("id", "session_password").send_keys(password)
        print(datetime.now(), ' Find password field and enter in password...\n')

        # locate submit button by_class_id and click it
        self.driver.find_element("xpath", "//button[@type='submit']").click()
        print(datetime.now(), ' Click login button, logging in...\n')

    def filter_page(self, page):
        """
        This function filters the page to only show people.
        Parameters:
            page: The page to be filtered.
        Returns:
            lis: The list of people on the page.
        """
        # driver.get method() will navigate to a filtered linkedin users page given by the URL address
        self.driver.get(f"{settings.filterPersonsUrl}&page={str(page)}")

        # locate each li tag name and return the list of all the li tags
        lis = self.driver.find_elements(
            "xpath", '//li[@class="reusable-search__result-container "]')
        return lis
