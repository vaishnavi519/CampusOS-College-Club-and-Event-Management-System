
import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_URL = "http://localhost:5173"
EMAIL = "zavarvaishnavi08@gmail.com"


def main():
    password = getpass.getpass(
        f"Enter the password for {EMAIL}: "
    )

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
        # 1. Log in using the existing student account.
        driver.get(f"{BASE_URL}/login")

        wait.until(
            EC.visibility_of_element_located((By.NAME, "email"))
        ).send_keys(EMAIL)

        driver.find_element(
            By.NAME, "password"
        ).send_keys(password)

        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

        wait.until(
            lambda d: "/login" not in d.current_url
        )

        check(
            "/login" not in driver.current_url,
            "Student login succeeds"
        )

        # 2. Open Browse Events.
        driver.get(f"{BASE_URL}/app/events")

        wait.until(
            lambda d: "/login" not in d.current_url
        )

        check(
            "/app/events" in driver.current_url,
            "Browse Events page opens"
        )

        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 3. Find links to individual event detail pages.
        event_links = wait.until(
            lambda d: [
                link for link in d.find_elements(
                    By.CSS_SELECTOR, "a[href*='/app/events/']"
                )
                if link.is_displayed()
                and link.get_attribute("href").rstrip("/")
                != f"{BASE_URL}/app/events"
            ] or False
        )

        check(
            len(event_links) > 0,
            "At least one event detail link is available"
        )

        # Save the event title before navigating.
        event_title = event_links[0].text.strip()
        event_url = event_links[0].get_attribute("href")

        print(f"Opening event: {event_title or event_url}")

        # 4. Open the first available event.
        driver.get(event_url)

        wait.until(
            lambda d: d.current_url.rstrip("/") == event_url.rstrip("/")
        )

        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        body = driver.find_element(By.TAG_NAME, "body").text.strip()

        check(
            len(body) > 0,
            "Event details page displays content"
        )

        check(
            "/app/events/" in driver.current_url,
            "Individual event details URL opens"
        )

        print("\nEvent details page text:")
        print(body[:1500])

        print(f"\nALL TESTS PASSED: {passed} checks.")

    except TimeoutException:
        print("\nFAIL: Timed out waiting for a page or event link.")
        print("Current URL:", driver.current_url)
        print("Check that the frontend and backend are running.")

    except AssertionError as error:
        print("\nFAIL:", error)
        print("Current URL:", driver.current_url)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
