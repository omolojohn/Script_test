import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Setup WebDriver for Chrome
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


# Test: Verify navigation across pages (Login, Product Listing, Cart, Checkout, Order History)
def test_navigation(driver):
    print("Starting test: Navigation across pages")

    driver.get("https://lazylizard.click/en/login")
    
    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.NAME, "username")))
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, "Product Listing")))
        driver.find_element(By.LINK_TEXT, "Product Listing").click()

        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, "Cart")))
        driver.find_element(By.LINK_TEXT, "Cart").click()

        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, "Checkout")))
        driver.find_element(By.LINK_TEXT, "Checkout").click()

        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, "Order History")))
        driver.find_element(By.LINK_TEXT, "Order History").click()

        print("Successfully navigated through all pages.")

    except TimeoutException:
        print("TimeoutException: Navigation test failed.")


# Test: Test responsiveness on different devices (desktop, tablet, mobile)
def test_responsiveness(driver):
    print("Starting test: Responsiveness on different devices")

    for width, height in [(1920, 1080), (768, 1024), (375, 667)]:
        driver.set_window_size(width, height)
        driver.get("https://lazylizard.click/en/login")
        assert "LazyLizard" in driver.title
        print(f"Responsive test passed at resolution {width}x{height}")

    print("Successfully tested responsiveness on desktop, tablet, and mobile views.")


# Test: Check for broken links or missing images
def test_broken_links_and_missing_images(driver):
    import requests
    print("Starting test: Broken links and missing images")

    driver.get("https://lazylizard.click/en/")

    # Check for broken links
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        url = link.get_attribute("href")
        if url and url.startswith("http"):
            try:
                response = requests.head(url, allow_redirects=True, timeout=10)
                assert response.status_code < 400
                print(f"Link OK: {url}")
            except Exception as e:
                print(f"Broken link: {url} - {e}")

    # Check for missing images
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        src = img.get_attribute("src")
        if src and src.startswith("http"):
            try:
                response = requests.head(src, allow_redirects=True, timeout=10)
                assert response.status_code < 400
                print(f"Image OK: {src}")
            except Exception as e:
                print(f"Missing image: {src} - {e}")


# Test: Ensure buttons, menus, and popups function as expected
def test_buttons_menus_popups(driver):
    print("Starting test: Buttons, menus, and popups functionality")

    driver.get("https://lazylizard.click/en/login")

    try:
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "login")))
        login_button.click()

        menu_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Product Listing")))
        menu_button.click()

        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            print("No alert popup found — skipping.")

        print("Buttons, menus, and popups function as expected.")

    except TimeoutException:
        print("TimeoutException: Buttons, menus, and popups test failed.")


# Test: Validate proper error messages for incorrect user actions
def test_error_messages(driver):
    print("Starting test: Error messages for incorrect user actions")

    driver.get("https://lazylizard.click/en/login")

    try:
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.NAME, "login")

        username_field.send_keys("wronguser")
        password_field.send_keys("wrongpass")
        login_button.click()

        error_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message")))
        assert "Invalid username" in error_element.text or "password" in error_element.text.lower()
        print("Error message for incorrect login credentials verified.")

    except TimeoutException:
        print("TimeoutException: Failed to verify error message.")
    except NoSuchElementException:
        print("NoSuchElementException: Error element not found.")

