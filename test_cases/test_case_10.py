
import getpass
import sys
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)

BASE_URL = "http://localhost:5173"
ADMIN_EMAIL = "vaishnavi.zavar@mitwpu.edu.in"
STUDENT_EMAIL = "zavarvaishnavi08@gmail.com"
EVENT_TITLE = "Test Event"
WAIT_TIME = 20


def main():
    driver = None
    passed = 0
    failed = 0

    def check(condition, message):
        nonlocal passed, failed

        if condition:
            passed += 1
            print(f"PASS: {message}")
        else:
            failed += 1
            print(f"FAIL: {message}")
            raise AssertionError(message)

    try:
        admin_password = getpass.getpass("Club Admin password: ")
        student_password = getpass.getpass("Student password: ")

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, WAIT_TIME)

        def login(email, password):
            driver.get(BASE_URL + "/login")

            email_box = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'input[name="email"]')
                )
            )
            password_box = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'input[name="password"]')
                )
            )

            email_box.clear()
            email_box.send_keys(email)
            password_box.clear()
            password_box.send_keys(password)

            wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[type="submit"]')
                )
            ).click()

            wait.until(lambda d: "/login" not in d.current_url)

        print("\nCAMPUSOS - TEST CASE 10")
        print("Attendance and notifications workflow")
        print("=" * 45)

        # TEST 1: Club Admin login
        login(ADMIN_EMAIL, admin_password)
        check(
            "/login" not in driver.current_url,
            "Club Admin login"
        )

        # TEST 2: Open the event registrations page
        driver.get(BASE_URL + "/club-admin/events")

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[normalize-space()='My events']")
            )
        )

        title = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//*[normalize-space()='{EVENT_TITLE}']")
            )
        )

        card = driver.execute_script(
            """
            let e = arguments[0];

            while (e && e !== document.body) {
                const controls = Array.from(
                    e.querySelectorAll('a, button')
                );

                const found = controls.some(
                    c => (c.innerText || '')
                        .trim()
                        .toLowerCase()
                        .includes('registrations')
                );

                if (found) return e;
                e = e.parentElement;
            }

            return null;
            """,
            title,
        )

        if card is None:
            check(False, f"Found registrations card for {EVENT_TITLE}")

        registration_control = next(
            (
                el for el in card.find_elements(
                    By.XPATH, ".//*[self::a or self::button]"
                )
                if el.is_displayed()
                and el.is_enabled()
                and "registrations" in el.text.lower()
            ),
            None,
        )

        if registration_control is None:
            check(False, "Found Registrations control")

        registration_control.click()
        wait.until(EC.url_contains("/registrations"))

        check(
            True,
            "Event registrations page opened"
        )

        # TEST 3: Find the student in the registration list
        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        print(
            "\nRegistration page preview:\n",
            driver.find_element(By.TAG_NAME, "body").text[:1800]
        )

        student_elements = driver.find_elements(
            By.XPATH,
            f"//*[normalize-space()='{STUDENT_EMAIL}']"
        )

        student_element = next(
            (
                el for el in student_elements
                if el.is_displayed()
                and el.tag_name.lower() in ("span", "p", "div")
                and el.text.strip() == STUDENT_EMAIL
            ),
            None,
        )

        if student_element is None:
            check(
                False,
                f"Student {STUDENT_EMAIL} is registered for "
                f"{EVENT_TITLE}"
            )

        student_row = driver.execute_script(
            """
            let e = arguments[0];

            while (e && e !== document.body) {
                if (e.classList &&
                    e.classList.contains('record')) {
                    return e;
                }
                e = e.parentElement;
            }

            return null;
            """,
            student_element,
        )

        if student_row is None:
            check(False, "Located student's registration row")

        check(True, "Student found in registration list")

        # TEST 4: Mark the student present
        present_button = next(
            (
                b for b in student_row.find_elements(
                    By.TAG_NAME, "button"
                )
                if b.is_displayed()
                and b.is_enabled()
                and b.text.strip().lower() == "present"
            ),
            None,
        )

        if present_button is None:
            check(False, "Found Present button in student row")

        present_button.click()

        wait.until(
            lambda d: (
                "marked present" in student_row.text.lower()
                or any(
                    el.text.strip().lower() == "present"
                    for el in student_row.find_elements(
                        By.CSS_SELECTOR,
                        ".badge, [class*='badge']"
                    )
                )
            )
        )

        check(True, "Attendance marked Present")

        # TEST 5: Log in as the student
        driver.get(BASE_URL + "/")

        driver.execute_script(
            """
            window.localStorage.clear();
            window.sessionStorage.clear();
            """
        )
        driver.delete_all_cookies()

        login(STUDENT_EMAIL, student_password)

        check(
            "/login" not in driver.current_url,
            "Student login"
        )

        # TEST 6: Load notifications page
        driver.get(BASE_URL + "/app/notifications")

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[normalize-space()='Notifications']")
            )
        )

        notification_text = wait.until(
            lambda d: (
                text if (text := d.find_element(
                    By.TAG_NAME, "body"
                ).text.strip()) else False
            )
        )

        check(
            bool(notification_text),
            "Notifications page loaded"
        )

        print(
            "\nNotifications page preview:\n",
            notification_text[:1200]
        )

        # TEST 7: Verify registration confirmation notification
        confirmation = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(normalize-space(.), "
                    "'Event registration confirmed')]"
                )
            )
        )

        check(
            confirmation.is_displayed(),
            "Registration confirmation notification is visible"
        )

        # Final result
        print("\n" + "=" * 45)
        print(f"Passed checks: {passed}")
        print(f"Failed checks: {failed}")

        if failed == 0 and passed == 7:
            print("ALL TESTS PASSED")
        else:
            print("TESTS FAILED")

        print("=" * 45)

        if failed > 0 or passed != 7:
            sys.exit(1)

    except (TimeoutException, AssertionError, WebDriverException) as error:
        print(f"\nTEST FAILED: {error}")
        traceback.print_exc()

        if driver is not None:
            try:
                print("Current URL:", driver.current_url)
                print(
                    "Page text:",
                    driver.find_element(
                        By.TAG_NAME, "body"
                    ).text[:2500]
                )
            except WebDriverException:
                pass

        sys.exit(1)

    finally:
        if driver is not None:
            try:
                input("\nPress Enter to close Chrome...")
            except EOFError:
                pass

            try:
                driver.quit()
            except WebDriverException:
                pass


if __name__ == "__main__":
    main()
