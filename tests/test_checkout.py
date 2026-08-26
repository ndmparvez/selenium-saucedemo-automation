"""Checkout.

The negative cases come first because a checkout that accepts incomplete
address details is a worse defect than one that will not complete at all. A
failed order is visible. A shipped order with no postcode is not.
"""
import pytest

from pages.login_page import LoginPage

ITEM = "Sauce Labs Backpack"


@pytest.fixture
def checkout(driver):
    inventory = LoginPage(driver).load().login("standard_user", "secret_sauce")
    inventory.add_to_cart(ITEM)
    return inventory.open_cart().checkout()


@pytest.mark.parametrize(
    "first,last,postcode,expected",
    [
        ("", "Parvez", "E15 2FT", "First Name is required"),
        ("Nadeem", "", "E15 2FT", "Last Name is required"),
        ("Nadeem", "Parvez", "", "Postal Code is required"),
    ],
    ids=["missing_first_name", "missing_last_name", "missing_postcode"],
)
def test_incomplete_details_are_rejected(checkout, first, last, postcode, expected):
    checkout.fill_details(first, last, postcode)
    assert expected in checkout.error_message()


@pytest.mark.smoke
def test_a_complete_purchase_reaches_confirmation(checkout):
    checkout.fill_details("Nadeem", "Parvez", "E15 2FT").finish()
    assert "Thank you for your order" in checkout.confirmation_text()
