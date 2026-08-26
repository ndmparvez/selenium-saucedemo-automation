from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTCODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_details(self, first, last, postcode):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTCODE, postcode)
        self.click(self.CONTINUE)
        return self

    def error_message(self):
        return self.text_of(self.ERROR)

    def total_text(self):
        return self.text_of(self.TOTAL)

    def finish(self):
        self.click(self.FINISH)
        return self

    def confirmation_text(self):
        return self.text_of(self.COMPLETE_HEADER)
