
import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_URL = "http://localhost:5173"
EMAIL = "zavarvaishnavi08@gmail.com"


def main():
    password = getpass.getpass(f"Password for {EMAIL}: ")

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1365,900")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    passed = 0

    def check(condition, message):
        nonlocal passed
        if not condition:
            raise AssertionError(message)
        passed += 1
        print(f"PASS: {message}")

    try:
        # Login
        driver.get(f"{BASE_URL}/login")
        wait.until(
            EC.visibility_of_element_located((By.NAME, "email"))
        ).send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

        wait.until(lambda d: "/login" not in d.current_url)
        check("/login" not in driver.current_url, "Student login succeeds")

        # Open the student dashboard
        driver.get(f"{BASE_URL}/app")
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        wait.until(lambda d: "/login" not in d.current_url)

        body = driver.find_element(By.TAG_NAME, "body").text.strip()
        check(len(body) > 0, "Dashboard displays content")

        print("\nDashboard text:")
        print(body[:1200])

        # Check for a useful student navigation link
        links = driver.find_elements(By.TAG_NAME, "a")
        visible_links = [
            link for link in links
            if link.is_displayed() and link.text.strip()
        ]

        check(
            len(visible_links) > 0,
            "Dashboard has visible navigation links"
        )

        # Check whether Browse Events is linked from the dashboard
        events_links = [
            link for link in visible_links
            if "event" in (
                link.text + " " + (link.get_attribute("href") or "")
            ).lower()
        ]

        check(
            len(events_links) > 0,
            "A navigation link to events is available"
        )

        print("\nALL TESTS PASSED:", passed, "checks.")

    except (TimeoutException, AssertionError) as error:
        print("\nFAIL:", error or "Page loading timed out")
        print("Current URL:", driver.current_url)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
