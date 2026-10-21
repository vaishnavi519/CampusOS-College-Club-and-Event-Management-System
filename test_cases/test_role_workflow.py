import getpass
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:5173"


def new_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def login(driver, email, password):
    driver.get(BASE_URL + "/login")
    wait = WebDriverWait(driver, 20)

    email_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="email"]')
        )
    )
    password_box = driver.find_element(
        By.CSS_SELECTOR, 'input[name="password"]'
    )

    email_box.send_keys(email)
    password_box.send_keys(password)

    driver.find_element(
        By.CSS_SELECTOR, 'button[type="submit"]'
    ).click()

    try:
        wait.until(lambda d: "/login" not in d.current_url)
        time.sleep(1)
        return True
    except Exception:
        print("Login failed for:", email)
        print("Page:", driver.find_element(By.TAG_NAME, "body").text[:500])
        return False


def check_page(driver, path, heading):
    driver.get(BASE_URL + path)
    time.sleep(2)

    text = driver.find_element(By.TAG_NAME, "body").text

    if heading.lower() in text.lower():
        print(f"PASS: {path} displays '{heading}'")
        return True

    print(f"FAIL: {path} did not display '{heading}'")
    print("Current URL:", driver.current_url)
    return False


def check_restricted_page(driver, path):
    driver.get(BASE_URL + path)
    time.sleep(2)

    current_path = driver.current_url.split("localhost:5173")[-1].rstrip("/")

    if current_path != path.rstrip("/"):
        print(f"PASS: Student blocked from {path}")
        return True

    print(f"FAIL: Student was not redirected from {path}")
    return False


accounts = [
    (
        "Club Admin",
        "vaishnavi.zavar@mitwpu.edu.in",
        getpass.getpass("Club Admin password: "),
    ),
    (
        "Faculty",
        "faculty@campusos.com",
        getpass.getpass("Faculty password: "),
    ),
    (
        "Student",
        "zavarvaishnavi08@gmail.com",
        getpass.getpass("Student password: "),
    ),
]

results = []

for role, email, password in accounts:
    driver = None

    try:
        driver = new_browser()
        print(f"\n--- {role.upper()} CHECK ---")

        if not login(driver, email, password):
            results.append(False)
            continue

        if role == "Club Admin":
            results.append(
                check_page(driver, "/club-admin/events", "My events")
            )

        elif role == "Faculty":
            results.append(
                check_page(driver, "/faculty/pending", "Pending events")
            )

        else:
            results.append(
                check_page(driver, "/app/events", "Events")
            )
            results.append(
                check_restricted_page(driver, "/club-admin/events")
            )
            results.append(
                check_restricted_page(driver, "/faculty/pending")
            )

    except Exception as error:
        print(f"ERROR during {role} check:", repr(error))
        results.append(False)

    finally:
        if driver is not None:
            driver.quit()

print("\n--- FINAL RESULT ---")
print(f"Passed: {sum(results)}/{len(results)}")

if results and all(results):
    print("ALL TESTS PASSED: Role-based access checks.")
else:
    print("Some checks failed. Review the output above.")