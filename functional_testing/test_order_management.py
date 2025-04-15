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

# Test: Buyers should see their order history with correct details
def test_buyers_order_history(driver):
    print("Starting test: Buyers' order history")

    # Log in as Buyer
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "password")))
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("buyer_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Verify login by checking for Buyer Dashboard
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Buyer Dashboard')]")))

        assert "Buyer Dashboard" in driver.page_source
        print("Buyer login successful.")

        # Navigate to Order History
        order_history_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Order History"))
        )
        order_history_tab.click()

        # Wait for order history to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "order-list")))

        # Verify the order details
        order_list = driver.find_elements(By.CLASS_NAME, "order-item")
        assert len(order_list) > 0  # Ensure there are orders
        assert "order_id" in order_list[0].text  # Check if order contains ID
        print("Order history displayed correctly.")

    except TimeoutException:
        print("TimeoutException: Buyers' order history test failed.")

# Test: Sellers should receive notifications when an order is placed
def test_sellers_notifications(driver):
    print("Starting test: Sellers' notifications on new order")

    # Log in as Seller
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("seller_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("seller_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Verify login by checking for Seller Dashboard
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Seller Dashboard')]")))

        assert "Seller Dashboard" in driver.page_source
        print("Seller login successful.")

        # Simulate order placement (buyer's action)
        driver.get("https://lazylizard.click/en/products") 
        order_button = driver.find_element(By.NAME, "place_order")
        order_button.click()

        # Wait for the notification to be sent
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "notification")))

        # Verify that a new order notification appears
        notifications = driver.find_elements(By.CLASS_NAME, "notification")
        assert any("New Order" in notification.text for notification in notifications)
        print("Seller received order notification.")

    except TimeoutException:
        print("TimeoutException: Sellers' notification test failed.")

# Test: Admins should see all orders and be able to manage them
def test_admin_order_management(driver):
    print("Starting test: Admin order management")

    # Log in as Admin
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("admin_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("admin_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Verify login by checking for Admin Dashboard
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Admin Dashboard')]")))

        assert "Admin Dashboard" in driver.page_source
        print("Admin login successful.")

        # Navigate to Order Management page
        order_management_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Order Management"))
        )
        order_management_tab.click()

        # Wait for order list to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "order-list")))

        # Verify that the admin can see all orders
        order_list = driver.find_elements(By.CLASS_NAME, "order-item")
        assert len(order_list) > 0  # Ensure there are orders
        print("Admin can view all orders.")

        # Admin managing an order (e.g., marking as shipped)
        manage_button = driver.find_element(By.NAME, "manage_order")
        manage_button.click()

        # Wait for the order management action to complete
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "order-status-shipped")))

        assert "Shipped" in driver.page_source
        print("Order managed (marked as shipped) successfully.")

    except TimeoutException:
        print("TimeoutException: Admin order management test failed.")
    
if __name__ == "__main__":
    pytest.main()
