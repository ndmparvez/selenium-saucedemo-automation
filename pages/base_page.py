"""Base page object.

Every page inherits from this so two rules are enforced in one place rather
than trusted to each page: every lookup goes through an explicit wait, and
nothing anywhere calls time.sleep. A suite that sleeps is slow, flaky, or both.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10


class BasePage:
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def all_visible(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.clickable(locator).click()

    def type(self, locator, text):
        field = self.visible(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator):
        return self.visible(locator).text

    def is_present(self, locator, timeout=3):
        """Short timeout on purpose.

        This is used to assert that something is absent. Using the default ten
        second wait for that would add ten seconds to every negative check.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False
