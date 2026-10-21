
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
EMAIL = "zavarvaishnavi08@gmail.com"


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1365,900")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    passed = 0

    def check(condition, message):
        nonlocal passed
        assert condition, message
        passed += 1
        print("PASS:", message)

    try:
       
        # Test Case 3: Empty login fields
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.visibility_of_element_located(
            (By.NAME, "email")
        ))

        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

        wait.until(lambda d: (
            "email address is required" in
            d.find_element(By.TAG_NAME, "body").text.lower()
            and "password is required" in
            d.find_element(By.TAG_NAME, "body").text.lower()
        ))

        body = driver.find_element(By.TAG_NAME, "body").text.lower()

        check(
            "email address is required" in body
            and "password is required" in body,
            "Empty login fields show required-field errors"
        )

        # Test Case 2: Invalid password
        driver.get(f"{BASE_URL}/login")

        wait.until(EC.visibility_of_element_located(
            (By.NAME, "email")
        )).send_keys(EMAIL)

        driver.find_element(
            By.NAME, "password"
        ).send_keys("DefinitelyWrongPassword123!")

        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

        wait.until(lambda d: (
            "/login" in d.current_url
            and (
                "invalid" in d.find_element(
                    By.TAG_NAME, "body"
                ).text.lower()
                or "incorrect" in d.find_element(
                    By.TAG_NAME, "body"
                ).text.lower()
                or "credentials" in d.find_element(
                    By.TAG_NAME, "body"
                ).text.lower()
                or "password" in d.find_element(
                    By.TAG_NAME, "body"
                ).text.lower()
                or "failed" in d.find_element(
                    By.TAG_NAME, "body"
                ).text.lower()
            )
        ))

        check(
            "/login" in driver.current_url,
            "Invalid password does not log in"
        )

        print(f"\nALL TESTS PASSED: {passed} checks.")

    except Exception as error:
        print("\nTEST FAILED:", type(error).__name__, str(error))
        print("Current URL:", driver.current_url)
        print("Page text:",
              driver.find_element(By.TAG_NAME, "body").text[:1000])

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
