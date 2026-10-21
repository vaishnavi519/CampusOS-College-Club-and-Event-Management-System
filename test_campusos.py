
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:5173"


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
        print(f"PASS: {message}")

    try:
        # Test 1: Homepage
        driver.get(BASE_URL)
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        wait.until(lambda d: d.title.strip() != "")

        check(
            driver.current_url.startswith(BASE_URL),
            "Homepage loads successfully",
        )

        # Test 2: Login page
        driver.get(f"{BASE_URL}/login")
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        check(
            "/login" in driver.current_url,
            "Login page opens",
        )

        check(
            len(driver.find_elements(By.TAG_NAME, "input")) > 0,
            "Login page contains input fields",
        )

        # Test 3: Registration page
        driver.get(f"{BASE_URL}/register")
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        check(
            "/register" in driver.current_url,
            "Registration page opens",
        )

        check(
            len(driver.find_elements(By.TAG_NAME, "input")) > 0,
            "Registration page contains input fields",
        )

        # Test 4: Unauthenticated access protection
        protected_routes = [
            "/app",
            "/app/clubs",
            "/app/events",
            "/app/notifications",
            "/app/profile",
            "/app/registrations",
            "/club-admin",
            "/faculty",
            "/admin",
        ]

        for route in protected_routes:
            driver.get(f"{BASE_URL}{route}")

            wait.until(
                lambda d: (
                    "/login" in d.current_url
                    or "/register" in d.current_url
                )
            )

            check(
                "/login" in driver.current_url,
                f"{route} redirects unauthenticated users to login",
            )

        print(f"\nALL TESTS PASSED: {passed} checks completed.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
