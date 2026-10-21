
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:5173"


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get(f"{BASE_URL}/login")

    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )

    # Test 1: Login form exists
    form = driver.find_element(By.TAG_NAME, "form")
    assert form.is_displayed()
    print("PASS: Login form is visible.")

    # Test 2: Email and password fields exist
    inputs = driver.find_elements(
        By.CSS_SELECTOR, "form input"
    )
    assert len(inputs) >= 2
    print("PASS: Login form contains input fields.")

    # Test 3: Submit empty form
    buttons = driver.find_elements(
        By.CSS_SELECTOR, "form button[type='submit']"
    )

    if not buttons:
        buttons = driver.find_elements(
            By.CSS_SELECTOR, "form button"
        )

    assert buttons, "Login submit button was not found."
    buttons[0].click()

    # Wait for client-side validation to show an error
    wait.until(
        lambda d: len(
            d.find_elements(
                By.CSS_SELECTOR,
                "[aria-invalid='true'], [role='alert']"
            )
        ) > 0
    )

    print("PASS: Empty login form triggers validation.")

    # Test 4: Page stays on login
    assert "/login" in driver.current_url
    print("PASS: Invalid form does not navigate away.")

    print("\nALL LOGIN VALIDATION TESTS PASSED.")

finally:
    driver.quit()
