
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("http://localhost:5173/register")
    driver.refresh()

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "form"))
    )

    driver.find_element(
        By.CSS_SELECTOR, "button[type='submit']"
    ).click()

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".field__error")
        )
    )

    driver.implicitly_wait(1)

    print("\n--- Registration form diagnostic ---")

    for name in ["name", "email", "password", "confirmPassword"]:
        field = driver.find_element(By.NAME, name)
        container = field.find_element(
            By.XPATH, "./ancestor::div[contains(@class, 'field')]"
        )

        print(f"\nInput: {name}")
        print("Value:", repr(field.get_attribute("value")))
        print("Invalid:", repr(field.get_attribute("aria-invalid")))
        print("Described by:", repr(field.get_attribute("aria-describedby")))
        print("Field content:", repr(container.text))

    print("\n--- Browser console errors ---")
    for entry in driver.get_log("browser"):
        if entry["level"] == "SEVERE":
            print(entry["message"])

finally:
    driver.quit()
