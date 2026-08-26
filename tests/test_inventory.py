"""Inventory page.

The theme here is that presence is not correctness. Asserting an image tag
exists passes on a catalogue showing the same picture six times. Asserting a
sort control exists passes on a sort that does nothing. Each test below checks
the outcome, not the widget.
"""
import pytest

from pages.login_page import LoginPage


@pytest.fixture
def inventory(driver):
    return LoginPage(driver).load().login("standard_user", "secret_sauce")


def test_all_six_products_are_listed(inventory):
    assert inventory.item_count() == 6


def test_every_product_has_a_name(inventory):
    assert all(name.strip() for name in inventory.names())


def test_sort_price_low_to_high_actually_sorts(inventory):
    inventory.sort_by("lohi")
    prices = inventory.prices()
    assert prices == sorted(prices)


def test_sort_price_high_to_low_actually_sorts(inventory):
    inventory.sort_by("hilo")
    prices = inventory.prices()
    assert prices == sorted(prices, reverse=True)


def test_sort_name_a_to_z_actually_sorts(inventory):
    inventory.sort_by("az")
    names = inventory.names()
    assert names == sorted(names)


def test_every_product_image_is_distinct(inventory):
    """Six products should mean six different pictures.

    This is the assertion that catches a broken catalogue. It is also the one
    that fails for problem_user, which is covered in tests/test_broken_users.py.
    """
    sources = inventory.image_sources()
    assert len(set(sources)) == len(sources)
