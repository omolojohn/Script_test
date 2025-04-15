import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Setup WebDriver for Chrome
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Test Admin Login and Dashboard Access
def test_admin_login(driver):
    print("Starting test: Admin login and dashboard access")
    driver.get("https://lazylizard.click/en/")

    try:
        # Wait for the password field
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "password")))

        # Enter admin credentials
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("admin_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Verify successful login by checking for "Admin Dashboard"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Admin Dashboard')]")))

        assert "Admin Dashboard" in driver.page_source
        print("Admin login successful, dashboard accessible.")

    except TimeoutException:
        print("TimeoutException: Admin login failed.")

# Test Product Moderation (Approve/Reject Products)
def test_product_moderation(driver):
    print("Starting test: Product moderation")

    # Log in as Admin
    test_admin_login(driver)

    try:
        # Navigate to Product Moderation Page
        moderation_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Product Moderation"))
        )
        moderation_tab.click()

        # Wait for product list to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-list")))

        # Approve a product
        approve_button = driver.find_element(By.NAME, "approve_product")
        approve_button.click()
        assert "Product approved" in driver.page_source
        print("Product approved successfully.")

        # Reject a product
        reject_button = driver.find_element(By.NAME, "reject_product")
        reject_button.click()
        assert "Product rejected" in driver.page_source
        print("Product rejected successfully.")

    except TimeoutException:
        print("TimeoutException: Product moderation test failed.")

# Test Admin User Management (Ban/Unban, Role Change)
def test_admin_user_management(driver):
    print("Starting test: Admin user management")

    # Log in as Admin
    test_admin_login(driver)

    try:
        # Navigate to User Management Page
        user_management_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "User Management"))
        )
        user_management_tab.click()

        # Wait for user list to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "user-list")))

        # Ban a user
        ban_button = driver.find_element(By.NAME, "ban_user")
        ban_button.click()
        assert "User banned" in driver.page_source
        print("User banned successfully.")

        # Unban a user
        unban_button = driver.find_element(By.NAME, "unban_user")
        unban_button.click()
        assert "User unbanned" in driver.page_source
        print("User unbanned successfully.")

        # Change user role
        change_role_button = driver.find_element(By.NAME, "change_role")
        change_role_button.click()
        assert "User role updated" in driver.page_source
        print("User role changed successfully.")

    except TimeoutException:
        print("TimeoutException: User management test failed.")

if __name__ == "__main__":
    pytest.main()
