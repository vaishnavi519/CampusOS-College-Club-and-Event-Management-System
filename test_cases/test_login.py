
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
TIMEOUT = 10


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def test_login_page_loads(driver, wait):
    driver.get(f"{BASE_URL}/login")

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "form"))
    )

    assert driver.find_element(By.NAME, "email").is_displayed()
    assert driver.find_element(By.NAME, "password").is_displayed()
    assert driver.find_element(
        By.CSS_SELECTOR, "button[type='submit']"
    ).is_displayed()

    print("PASS: Login page and fields are visible.")


def test_empty_login_validation(driver, wait):
    driver.get(f"{BASE_URL}/login")

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "form"))
    )

    driver.find_element(
        By.CSS_SELECTOR, "button[type='submit']"
    ).click()

    wait.until(
        lambda d: "Email address is required." in d.find_element(
            By.TAG_NAME, "body"
        ).text
        and "Password is required." in d.find_element(
            By.TAG_NAME, "body"
        ).text
    )

    body_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Email address is required." in body_text
    assert "Password is required." in body_text

    print("PASS: Empty login fields show validation errors.")


def test_invalid_email_validation(driver, wait):
    driver.get(f"{BASE_URL}/login")

    wait.until(
        EC.visibility_of_element_located((By.NAME, "email"))
    ).send_keys("invalid-email")

    driver.find_element(
        By.NAME, "password"
    ).send_keys("testpassword123")

    driver.find_element(
        By.CSS_SELECTOR, "button[type='submit']"
    ).click()

    wait.until(
        lambda d: "Enter a valid email address." in
        d.find_element(By.TAG_NAME, "body").text
    )

    print("PASS: Invalid email format is rejected.")


def test_password_visibility_toggle(driver, wait):
    driver.get(f"{BASE_URL}/login")

    password = wait.until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )

    assert password.get_attribute("type") == "password"

    driver.find_element(
        By.CSS_SELECTOR, "button[aria-label='Show password']"
    ).click()

    assert driver.find_element(
        By.NAME, "password"
    ).get_attribute("type") == "text"

    driver.find_element(
        By.CSS_SELECTOR, "button[aria-label='Hide password']"
    ).click()

    assert driver.find_element(
        By.NAME, "password"
    ).get_attribute("type") == "password"

    print("PASS: Password visibility toggle works.")


def main():
    driver = create_driver()
    wait = WebDriverWait(driver, TIMEOUT)

    tests = [
        ("Login page", test_login_page_loads),
        ("Empty login validation", test_empty_login_validation),
        ("Invalid email validation", test_invalid_email_validation),
        ("Password visibility", test_password_visibility_toggle),
    ]

    passed = 0
    failed = 0

    try:
        for name, test in tests:
            try:
                test(driver, wait)
                passed += 1
            except Exception as error:
                failed += 1
                print(f"FAIL: {name}: {type(error).__name__}: {error}")

    finally:
        driver.quit()

    print("\n========== LOGIN TEST SUMMARY ==========")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
