"""Cart behaviour.

The cart badge is the only feedback a user gets that an action worked, so it is
tested as a first class outcome rather than as decoration.
"""
import pytest

from pages.login_page import LoginPage

ITEM = "Sauce Labs Backpack"
OTHER_ITEM = "Sauce Labs Bike Light"


@pytest.fixture
def inventory(driver):
    return LoginPage(driver).load().login("standard_user", "secret_sauce")


def test_cart_starts_empty(inventory):
    assert inventory.cart_count() == 0


def test_adding_one_item_updates_the_badge(inventory):
    inventory.add_to_cart(ITEM)
    assert inventory.cart_count() == 1


def test_adding_two_items_updates_the_badge(inventory):
    inventory.add_to_cart(ITEM)
    inventory.add_to_cart(OTHER_ITEM)
    assert inventory.cart_count() == 2


def test_the_item_added_is_the_item_in_the_cart(inventory):
    """The badge counting to one does not prove the right thing went in."""
    inventory.add_to_cart(ITEM)
    cart = inventory.open_cart()
    assert cart.item_names() == [ITEM]


def test_removing_the_only_item_empties_the_cart(inventory):
    inventory.add_to_cart(ITEM)
    cart = inventory.open_cart()
    cart.remove(ITEM)
    assert cart.item_names() == []
