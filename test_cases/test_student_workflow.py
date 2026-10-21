
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
EMAIL = "zavarvaishnavi08@gmail.com"

# Enter the existing test student's password when prompted.
import getpass


def main():
    password = getpass.getpass("Enter the password for zavarvaishnavi08@gmail.com: ")

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1365,900")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    passed = 0

    def check(condition, message):
        nonlocal passed
        assert condition, message
        passed += 1
        print(f"PASS: {message}")

    try:
        # 1. Log in as the student.
        driver.get(f"{BASE_URL}/login")

        wait.until(
            EC.visibility_of_element_located((By.NAME, "email"))
        ).send_keys(EMAIL)

        driver.find_element(By.NAME, "password").send_keys(password)

        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

        wait.until(
            lambda d: "/login" not in d.current_url
        )

        check(
            "/login" not in driver.current_url,
            "Student login succeeds",
        )

        # 2. Verify the student dashboard.
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        body = driver.find_element(By.TAG_NAME, "body").text
        check(
            len(body.strip()) > 0,
            "Authenticated page displays content",
        )

        # 3. Open Browse Events.
        driver.get(f"{BASE_URL}/app/events")

        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        wait.until(
            lambda d: "/login" not in d.current_url
        )

        check(
            "/app/events" in driver.current_url,
            "Student can open Browse Events",
        )

        # 4. Verify event content has loaded.
        wait.until(
            lambda d: (
                "bootcamp" in d.find_element(
                    By.TAG_NAME, "body"
                ).text.lower()
                or "test event" in d.find_element(
                    By.TAG_NAME, "body"
                ).text.lower()
                or "no events" in d.find_element(
                    By.TAG_NAME, "body"
                ).text.lower()
            )
        )

        body = driver.find_element(By.TAG_NAME, "body").text.lower()

        check(
            "bootcamp" in body
            or "test event" in body
            or "no events" in body,
            "Event list or empty state is displayed",
        )

        print(f"\nALL TESTS PASSED: {passed} checks.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
