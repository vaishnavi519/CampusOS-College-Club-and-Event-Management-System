
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        assert condition, message
        passed += 1
        print("PASS:", message)

    try:
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.visibility_of_element_located(
            (By.NAME, "email")
        )).send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()
        wait.until(lambda d: "/login" not in d.current_url)
        check("/login" not in driver.current_url, "Student login")

        # Open the clubs page
        driver.get(f"{BASE_URL}/app/clubs")
        wait.until(EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        ))
        wait.until(lambda d: "/login" not in d.current_url)

        body = driver.find_element(By.TAG_NAME, "body").text.strip()
        check(bool(body), "Clubs page displays content")

        print("\nClubs page text:")
        print(body[:1200])

        check(
            any(word in body.lower() for word in
                ("club", "no clubs", "search", "filter")),
            "Club-related content or empty state is visible"
        )

        print("\nALL TESTS PASSED:", passed, "checks.")

    except Exception as error:
        print("\nTEST FAILED:", type(error).__name__, str(error))
        print("Current URL:", driver.current_url)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
