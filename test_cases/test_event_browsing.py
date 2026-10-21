
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"


def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    passed = 0

    def check(condition, message):
        nonlocal passed
        assert condition, message
        passed += 1
        print(f"PASS: {message}")

    try:
        # Test 1: Events route requires authentication
        driver.get(f"{BASE_URL}/app/events")
        wait.until(lambda d: "/login" in d.current_url)

        check(
            "/login" in driver.current_url,
            "Unauthenticated event browsing redirects to login",
        )

        # Test 2: Login page is displayed after redirect
        wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "form"))
        )
        check(
            driver.find_element(By.TAG_NAME, "form").is_displayed(),
            "Login form is visible after redirect",
        )

        # Test 3: Direct login route opens
        driver.get(f"{BASE_URL}/login")
        wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "form"))
        )
        check(
            "/login" in driver.current_url,
            "Login route opens successfully",
        )

        # Test 4: Homepage remains accessible
        driver.get(BASE_URL)
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        check(
            driver.current_url.startswith(BASE_URL),
            "Homepage remains accessible",
        )

        print(f"\nALL TESTS PASSED: {passed} checks.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
