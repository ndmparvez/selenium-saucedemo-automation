from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_IMAGES = (By.CLASS_NAME, "inventory_item_img")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def is_loaded(self):
        return self.text_of(self.TITLE) == "Products"

    def item_count(self):
        return len(self.all_visible(self.ITEMS))

    def names(self):
        return [e.text for e in self.all_visible(self.ITEM_NAMES)]

    def prices(self):
        return [float(e.text.replace("$", "")) for e in self.all_visible(self.ITEM_PRICES)]

    def image_sources(self):
        """The src of each product image.

        Returned rather than asserted on here so a test can decide what matters.
        Checking that the sources are distinct is what catches a catalogue
        serving the same picture for every product.
        """
        return [
            e.find_element(By.TAG_NAME, "img").get_attribute("src")
            for e in self.all_visible(self.ITEM_IMAGES)
        ]

    def sort_by(self, value):
        Select(self.visible(self.SORT)).select_by_value(value)

    def add_to_cart(self, item_name):
        slug = item_name.lower().replace(" ", "-")
        self.click((By.ID, "add-to-cart-" + slug))

    def cart_count(self):
        if not self.is_present(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def open_cart(self):
        from pages.cart_page import CartPage

        self.click(self.CART_LINK)
        return CartPage(self.driver)
