# selenium-saucedemo-automation

[![tests](https://github.com/ndmparvez/selenium-saucedemo-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/ndmparvez/selenium-saucedemo-automation/actions/workflows/ci.yml)

A Selenium WebDriver and pytest suite covering the SauceDemo purchase journey,
using the Page Object Model and gated in CI on every push.

## Why the tests are the tests

Rather than testing every element on every page, I decomposed the application
into the one journey that matters, logging in and buying something, and then
asked what would have to go wrong to break it. Each requirement gets one test
aimed at a specific failure mode. The traceability table in
[docs/test_plan.md](docs/test_plan.md) maps every requirement to the test that
demonstrates it and the evidence that test produces.

The principle that shaped most of it: **presence is not correctness.**
Asserting a sort control exists passes on a sort that does nothing. Asserting
an image tag exists passes on a catalogue showing the same picture six times.
So the assertions here are written against outcomes, not against the DOM.

## The suite is also run against known broken accounts

SauceDemo ships accounts that are seeded with defects. The same journeys are
run against those in [tests/test_broken_users.py](tests/test_broken_users.py),
and those runs fail on purpose. What they caught, and how each failure was
reproduced, goes in [docs/defect_report.md](docs/defect_report.md).

This is the part I think matters. A suite that has only ever run green against
a healthy system is a suite with no evidence that it detects anything. Running
it against something known to be broken is the only way to find out whether the
assertions are load bearing or decorative.

Those tests are excluded from CI, because a seeded defect in a third party demo
site is not a regression in this repository and should not gate a commit.

## Running it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                           # everything except the broken account runs
pytest -m smoke                  # the core journey only
pytest -m broken_user --headed   # the diagnostic runs, watch them fail
pytest --headed                  # any run, with a visible browser
```

Chrome is required. Selenium Manager resolves the matching driver, so there is
no chromedriver to install. An HTML report is written to `report.html` on
every run, and CI uploads it as an artifact whether the run passed or failed.

## Layout

```
conftest.py                 driver fixture, headed flag, teardown
pages/
  base_page.py              explicit wait helpers, inherited by every page
  login_page.py
  inventory_page.py
  cart_page.py
  checkout_page.py
tests/
  test_login.py
  test_inventory.py
  test_cart.py
  test_checkout.py
  test_broken_users.py      diagnostic runs, expected to fail
docs/
  test_plan.md              requirement to test to evidence traceability
  defect_report.md          findings from the broken account runs
.github/workflows/ci.yml
```

## Design decisions worth stating

**Page Object Model.** Locators live in the page classes and never in a test.
When SauceDemo changes an id, one file changes.

**No time.sleep anywhere.** Every lookup goes through an explicit
`WebDriverWait` in `pages/base_page.py`. The implicit wait is pinned at zero,
because mixing implicit and explicit waits makes timeout behaviour
unpredictable.

**A fresh browser per test.** Function scoped, not session scoped. Sharing one
browser is faster but makes every failure depend on what ran before it, which
is a bad trade when the point of the suite is diagnosable failures.

**Short timeout for absence checks.** Asserting a cart is empty should not cost
ten seconds of waiting for items that were deliberately removed, so
`is_present` takes a shorter timeout.

## Not covered yet

Mobile viewports and Appium, session expiry and back button behaviour, visual
regression. The first of those is the next thing on the list.

## Credentials

The accounts used here are the demo logins SauceDemo publishes on its own login
page. Nothing private is committed.
