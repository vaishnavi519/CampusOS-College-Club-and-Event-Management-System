
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # Test 1: Homepage
    driver.get(BASE_URL)
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    assert driver.title.strip()
    print("PASS: Homepage loads.")

    # Test 2: Login page
    driver.get(f"{BASE_URL}/login")
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )
    assert "/login" in driver.current_url
    print("PASS: Login page opens.")

    # Test 3: Registration page
    driver.get(f"{BASE_URL}/register")
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )
    assert "/register" in driver.current_url
    print("PASS: Registration page opens.")

    # Test 4: Protected pages redirect without authentication
    protected_routes = [
        "/app",
        "/app/clubs",
        "/app/events",
        "/app/notifications",
        "/app/profile",
    ]

    for route in protected_routes:
        driver.get(f"{BASE_URL}{route}")

        wait.until(
            lambda d: "/login" in d.current_url
        )

        assert "/login" in driver.current_url, (
            f"{route} did not redirect to login"
        )
        print(f"PASS: {route} redirects to login.")

    print("\nALL NAVIGATION TESTS PASSED.")

finally:
    driver.quit()
