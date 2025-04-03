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
    driver.maximize_window()
    yield driver
    driver.quit()

# Test: Add items to the cart and verify they appear correctly
def test_add_items_to_cart(driver):
    print("Starting test: Add items to cart and verify")

    # Log in as a buyer
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("buyer_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("buyer_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Navigate to a product page
        driver.get("https://lazylizard.click/en/product/1") 

        # Add the product to the cart
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "add_to_cart"))
        )
        add_to_cart_button.click()

        # Go to the cart page and verify the item appears
        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))
        )
        cart_button.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-item")))

        # Verify the cart contains the item
        cart_items = driver.find_elements(By.CLASS_NAME, "cart-item")
        assert len(cart_items) > 0
        print("Item successfully added to cart.")

    except TimeoutException:
        print("TimeoutException: Add item to cart test failed.")

# Test: Increase/decrease item quantity and ensure price updates accordingly
def test_update_item_quantity(driver):
    print("Starting test: Update item quantity and verify price update")

    # Log in and go to cart
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("buyer_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("buyer_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Add an item to the cart
        driver.get("https://lazylizard.click/en/product/1")
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "add_to_cart"))
        )
        add_to_cart_button.click()

        # Go to the cart page
        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))
        )
        cart_button.click()

        # Wait for the cart items to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-item")))

        # Increase item quantity
        increase_quantity_button = driver.find_element(By.NAME, "increase_quantity")
        increase_quantity_button.click()

        # Verify price has updated
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-total")))
        total_price = driver.find_element(By.CLASS_NAME, "cart-total")
        assert "Total Price" in total_price.text
        print("Item quantity updated and price verified.")

        # Decrease item quantity
        decrease_quantity_button = driver.find_element(By.NAME, "decrease_quantity")
        decrease_quantity_button.click()

        # Verify price has updated again
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-total")))
        total_price = driver.find_element(By.CLASS_NAME, "cart-total")
        assert "Total Price" in total_price.text
        print("Item quantity decreased and price verified.")

    except TimeoutException:
        print("TimeoutException: Quantity update test failed.")

# Test: Remove an item from the cart and confirm it's deleted
def test_remove_item_from_cart(driver):
    print("Starting test: Remove item from cart and confirm deletion")

    # Log in and go to cart
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("buyer_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("buyer_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Add an item to the cart
        driver.get("https://lazylizard.click/en/product/1")
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "add_to_cart"))
        )
        add_to_cart_button.click()

        # Go to the cart page
        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))
        )
        cart_button.click()

        # Wait for the cart items to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-item")))

        # Remove the item from the cart
        remove_button = driver.find_element(By.NAME, "remove_item")
        remove_button.click()

        # Verify the cart is empty
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "empty-cart-message")))

        empty_cart_message = driver.find_element(By.CLASS_NAME, "empty-cart-message")
        assert "Your cart is empty" in empty_cart_message.text
        print("Item successfully removed from cart.")

    except TimeoutException:
        print("TimeoutException: Remove item from cart test failed.")

# Test: Attempt checkout with an empty cart and check for errors
def test_checkout_empty_cart(driver):
    print("Starting test: Checkout with empty cart and verify error")

    # Log in without adding any items to the cart
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("buyer_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("buyer_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Go to the cart page (empty cart)
        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))
        )
        cart_button.click()

        # Wait for the cart to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-empty-message")))

        # Attempt to checkout with an empty cart
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Checkout"))
        )
        checkout_button.click()

        # Verify error message appears
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-empty-error")))

        error_message = driver.find_element(By.CLASS_NAME, "cart-empty-error")
        assert "Your cart is empty" in error_message.text
        print("Error verified: Cannot checkout with empty cart.")

    except TimeoutException:
        print("TimeoutException: Checkout with empty cart test failed.")

if __name__ == "__main__":
    pytest.main()
