# Test plan

## How these tests were chosen

SauceDemo is small enough that testing everything is possible, which makes it a
bad habit to get into. Instead I decomposed the application into the single
journey that matters, logging in and buying something, and then asked what
would have to go wrong to break it.

Each requirement below is one thing the system must do. Each has one test
aimed at it, and each test targets a specific way that requirement could fail
rather than simply exercising the page again.

The distinction that shaped most of these: **presence is not correctness.**
Asserting that a sort dropdown exists passes on a sort that does nothing.
Asserting that an image tag exists passes on a catalogue showing the same
picture six times. So every assertion below is written against an outcome.

## Traceability

| ID | Requirement | Test | Evidence produced |
|----|-------------|------|-------------------|
| R1 | Valid credentials grant access | test_valid_login_reaches_the_inventory | Lands on inventory.html and the Products heading renders |
| R2 | Invalid credentials are refused with a useful message | test_login_failures_show_the_right_message | Five parametrised cases, each asserting its specific message |
| R3 | A refused login does not grant access | test_a_wrong_password_does_not_let_you_through | URL is still the login page after a failed attempt |
| R4 | The catalogue lists every product | test_all_six_products_are_listed | Count of rendered items |
| R5 | Every product is identifiable | test_every_product_has_a_name | No blank names |
| R6 | Every product is visually distinct | test_every_product_image_is_distinct | Count of distinct image sources equals product count |
| R7 | Sorting by price ascending works | test_sort_price_low_to_high_actually_sorts | Extracted prices compared against a sorted copy |
| R8 | Sorting by price descending works | test_sort_price_high_to_low_actually_sorts | As above, reversed |
| R9 | Sorting by name works | test_sort_name_a_to_z_actually_sorts | Extracted names compared against a sorted copy |
| R10 | The cart starts empty | test_cart_starts_empty | Badge absent, count reads zero |
| R11 | Adding an item is reflected to the user | test_adding_one_item_updates_the_badge | Badge reads one |
| R12 | The count is accurate for multiple items | test_adding_two_items_updates_the_badge | Badge reads two |
| R13 | The item added is the item stored | test_the_item_added_is_the_item_in_the_cart | Cart contents compared by name |
| R14 | Removal actually removes | test_removing_the_only_item_empties_the_cart | Cart contents empty |
| R15 | Incomplete delivery details are refused | test_incomplete_details_are_rejected | Three parametrised cases, each asserting its field specific message |
| R16 | A complete order can be placed | test_a_complete_purchase_reaches_confirmation | Confirmation header text |

## Risk based ordering

R15 is tested before R16 deliberately. A checkout that refuses a valid order is
a visible failure that someone will report within minutes. A checkout that
accepts an order with no postcode is invisible until the parcel cannot be
delivered. The second is the more expensive defect, so it gets tested first.

R3 is separated from R2 for a similar reason. A system can display the correct
error message and still navigate the user through. Asserting only on the
message would not catch that, so the access control behaviour gets its own
test.

## Deliberately not covered

- Visual layout and CSS. Out of scope for a functional suite, and better served
  by a screenshot diffing tool than by assertions.
- The burger menu, About link and social links. They leave the application, so
  testing them tests someone else's site.
- Session expiry and back button behaviour. Worth adding, not yet written.
- Mobile viewports. Would need Appium or responsive emulation, which is the
  next thing on the list.
