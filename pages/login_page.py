from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self):
        self.driver.get(self.URL)
        return self

    def login(self, username, password):
        """Submit credentials and hand back the inventory page.

        Returns the next page object even when login is expected to fail, so a
        test can assert on the error message without a different call shape for
        the negative cases.
        """
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return InventoryPage(self.driver)

    def error_message(self):
        return self.text_of(self.ERROR)
