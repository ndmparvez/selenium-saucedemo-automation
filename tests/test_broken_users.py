"""The same journeys, run against SauceDemo's deliberately faulty accounts.

These are expected to fail, and that is the point.

A suite that has only ever run green against a healthy system is a suite with
no evidence that it detects anything. Running the same assertions against
accounts that are known to be broken is how you find out whether they are load
bearing or decorative.

What these runs caught, and how each was reproduced, is written up in
docs/defect_report.md.

Run them on their own:
    pytest -m broken_user

They are excluded from CI, because a known defect in a third party demo site is
not a regression in this repository and should not gate a commit.
"""
import time

import pytest

from pages.login_page import LoginPage

PASSWORD = "secret_sauce"
LOGIN_BUDGET_SECONDS = 5


@pytest.mark.broken_user
def test_problem_user_sees_distinct_product_images(driver):
    inventory = LoginPage(driver).load().login("problem_user", PASSWORD)
    sources = inventory.image_sources()
    distinct = len(set(sources))
    assert distinct == len(sources), (
        "Expected " + str(len(sources)) + " distinct product images, found "
        + str(distinct)
    )


@pytest.mark.broken_user
def test_problem_user_can_enter_a_last_name_at_checkout(driver):
    inventory = LoginPage(driver).load().login("problem_user", PASSWORD)
    inventory.add_to_cart("Sauce Labs Backpack")
    checkout = inventory.open_cart().checkout()
    checkout.type(checkout.LAST_NAME, "Parvez")
    entered = checkout.visible(checkout.LAST_NAME).get_attribute("value")
    assert entered == "Parvez", "Last name field contained: " + repr(entered)


@pytest.mark.broken_user
def test_performance_glitch_user_logs_in_within_budget(driver):
    page = LoginPage(driver).load()
    started = time.monotonic()
    inventory = page.login("performance_glitch_user", PASSWORD)
    inventory.is_loaded()
    elapsed = time.monotonic() - started
    assert elapsed < LOGIN_BUDGET_SECONDS, (
        "Login took " + format(elapsed, ".1f") + "s against a "
        + str(LOGIN_BUDGET_SECONDS) + "s budget"
    )
