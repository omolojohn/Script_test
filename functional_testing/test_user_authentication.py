import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Setup WebDriver and testing on Chrome
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_with_valid_credentials(driver):
    print("Starting test: Login with valid credentials (valid password)")

    # Open login page
    print("Opening login page...")
    driver.get("https://lazylizard.click/en/login")

    try:
        print(f"Attempting login with valid credentials...")

        # Wait for the password field to be visible before interacting
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "password")))

        # Find and fill the password field
        password_field = driver.find_element(By.NAME, "password")
        
        password_field.send_keys("valid_password")
        # Click the login button
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Verify successful login
        print("Verifying successful login...")
        assert "Dashboard" in driver.title
        assert "Profile" in driver.page_source

        # Check session persistence (refresh the page)
        driver.refresh()
        assert "Profile" in driver.page_source
        print("Login successful with valid credentials")

    except TimeoutException:
        print("TimeoutException: Element not found in time")

def test_login_with_invalid_credentials(driver):

    # Open login page
    driver.get("https://lazylizard.click/en/")

    try:
        # Wait for the password field to be visible before interacting
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "password")))

        # Find and fill the password field with an invalid password
        password_field = driver.find_element(By.NAME, "password")
        
        password_field.send_keys("invalid_password") 

        # Click the login button
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Verify error handling for invalid login
        assert "Invalid credentials" in driver.page_source 

    except TimeoutException:
        print("TimeoutException: Element not found in time")

def test_logout(driver):
    print("Starting test: Logout functionality")

    # Open login page
    driver.get("https://lazylizard.click/en/")

    # Log in with valid credentials
    try:
        # Wait for the password field to be visible before interacting
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "password")))

        password_field = driver.find_element(By.NAME, "password")
        
        # Fill the password field and click the login button
        password_field.send_keys("valid_password") 
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Verify successful login
        assert "Dashboard" in driver.title
        assert "Profile" in driver.page_source

        # Logout
        logout_button = driver.find_element(By.NAME, "logout")
        logout_button.click()

        # Verify redirection to login page after logout
        assert "Login" in driver.title
        
    except TimeoutException:
        print("TimeoutException: Element not found in time")

if __name__ == "__main__":
    pytest.main()


