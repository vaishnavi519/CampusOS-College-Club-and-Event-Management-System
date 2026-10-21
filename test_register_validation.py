
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get(f"{BASE_URL}/register")

    form = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "form"))
    )
    print("PASS: Registration form is visible.")

    inputs = form.find_elements(By.TAG_NAME, "input")
    assert len(inputs) >= 3, (
        f"Expected registration fields, found {len(inputs)} inputs."
    )
    print(f"PASS: Registration form has {len(inputs)} input fields.")

    submit_buttons = form.find_elements(
        By.CSS_SELECTOR, "button[type='submit']"
    )
    if not submit_buttons:
        submit_buttons = form.find_elements(By.TAG_NAME, "button")

    assert submit_buttons, "Submit button not found."
    submit_buttons[0].click()

    wait.until(
        lambda d: len(
            d.find_elements(
                By.CSS_SELECTOR,
                "[aria-invalid='true'], [role='alert'], "
                "[id$='-error']"
            )
        ) > 0
    )
    print("PASS: Empty registration form triggers validation.")

    assert "/register" in driver.current_url
    print("PASS: Invalid registration stays on the registration page.")

    print("\nALL REGISTRATION VALIDATION TESTS PASSED.")

finally:
    driver.quit()
