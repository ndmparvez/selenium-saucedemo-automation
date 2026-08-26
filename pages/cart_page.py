from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def item_names(self):
        """Names in the cart, or an empty list.

        The presence check comes first because waiting ten seconds for items
        that were deliberately removed is the slowest possible way to assert
        that a cart is empty.
        """
        if not self.is_present(self.ITEMS):
            return []
        return [e.text for e in self.all_visible(self.ITEM_NAMES)]

    def remove(self, item_name):
        slug = item_name.lower().replace(" ", "-")
        self.click((By.ID, "remove-" + slug))

    def checkout(self):
        from pages.checkout_page import CheckoutPage

        self.click(self.CHECKOUT)
        return CheckoutPage(self.driver)
