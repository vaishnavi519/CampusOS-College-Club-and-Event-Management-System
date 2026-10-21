
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
EMAIL = "zavarvaishnavi08@gmail.com"
EVENT_ID = 6


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
        check("/login" not in driver.current_url, "Student login succeeds")

        driver.get(f"{BASE_URL}/app/events/{EVENT_ID}")
        wait.until(EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        ))
        wait.until(lambda d: "/login" not in d.current_url)

        body = driver.find_element(By.TAG_NAME, "body").text
        check("Test Event".lower() in body.lower(),
              "Selected event details are displayed")

        # Avoid submitting twice if already registered.
        buttons = driver.find_elements(By.TAG_NAME, "button")
        registered = any(
            "cancel registration" in b.text.lower()
            or "already registered" in b.text.lower()
            for b in buttons
        )

        if registered:
            print("INFO: Student appears to be already registered.")
            check(True, "No duplicate registration attempted")
        else:
            register_buttons = [
                b for b in buttons
                if b.is_displayed()
                and ("register" in b.text.lower()
                     or "join the waitlist" in b.text.lower())
            ]
            check(len(register_buttons) > 0,
                  "Registration action is available")

            register_buttons[0].click()
            wait.until(lambda d: (
                "cancel registration" in
                d.find_element(By.TAG_NAME, "body").text.lower()
                or "successfully registered" in
                d.find_element(By.TAG_NAME, "body").text.lower()
                or "already registered" in
                d.find_element(By.TAG_NAME, "body").text.lower()
            ))
            check(True, "Registration action returned a visible result")

        print("\nResulting page:")
        print(driver.find_element(By.TAG_NAME, "body").text[:1200])
        print(f"\nTEST COMPLETED: {passed} checks.")

    except Exception as error:
        print("\nTEST FAILED:", type(error).__name__, str(error))
        print("Current URL:", driver.current_url)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
