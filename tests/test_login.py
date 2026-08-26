"""Login coverage.

One test per failure mode rather than one test per field. The question asked of
each case is not "does the field exist" but "what does a user see when this
goes wrong, and is it the right thing".
"""
import pytest

from pages.login_page import LoginPage

VALID_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.mark.smoke
def test_valid_login_reaches_the_inventory(driver):
    inventory = LoginPage(driver).load().login(VALID_USER, PASSWORD)
    assert inventory.is_loaded()
    assert "inventory.html" in driver.current_url


@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("no_such_user", "secret_sauce", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ],
    ids=[
        "wrong_password",
        "unknown_user",
        "missing_username",
        "missing_password",
        "locked_out_account",
    ],
)
def test_login_failures_show_the_right_message(driver, username, password, expected):
    page = LoginPage(driver).load()
    page.login(username, password)
    assert expected in page.error_message()


def test_a_wrong_password_does_not_let_you_through(driver):
    """Separate from the message assertion above, deliberately.

    A system can show the correct error and still navigate. Asserting the
    message alone would not catch that, so the security relevant behaviour
    gets its own test.
    """
    page = LoginPage(driver).load()
    page.login("standard_user", "wrong_password")
    assert "inventory.html" not in driver.current_url
