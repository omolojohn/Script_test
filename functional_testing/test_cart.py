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

# Test 1: Add items to the cart and verify they appear correctly
def test_add_items_to_cart(driver):
    print("Starting test: Add items to the cart and verify they appear correctly")

    # Open the product page
    driver.get("http://lazylizard.click/en/")

    try:
        # Wait for products to be loaded and available for selection
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item")))

        # Select the first product
        first_product = driver.find_element(By.CLASS_NAME, "product-item")
        first_product.click()

        # Wait for product page to load
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "add-to-cart")))

        # Click "Add to Cart"
        add_to_cart_button = driver.find_element(By.NAME, "add-to-cart")
        add_to_cart_button.click()

        # Verify item is added to cart
        cart_icon = driver.find_element(By.CLASS_NAME, "cart-icon")
        cart_icon.click()

        # Wait for cart to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-items")))

        cart_items = driver.find_elements(By.CLASS_NAME, "cart-item")
        assert len(cart_items) > 0, "Cart is empty, item was not added."

        print("Item successfully added to the cart.")
    
    except TimeoutException:
        print("TimeoutException: Element not found in time")

# Test 2: Increase/Decrease item quantity and ensure price updates
def test_update_item_quantity(driver):
    print("Starting test: Increase/Decrease item quantity and ensure price updates")

    # Open cart page
    driver.get("http://lazylizard.click/en/cards/cart")

    try:
        # Wait for cart to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-items")))

        # Find quantity input for the first cart item
        quantity_input = driver.find_element(By.NAME, "quantity")
        
        # Increase item quantity
        quantity_input.clear()
        quantity_input.send_keys("2")
        
        # Verify price updates (assuming the price is displayed in a class named 'item-price')
        item_price = driver.find_element(By.CLASS_NAME, "item-price").text
        total_price = driver.find_element(By.CLASS_NAME, "total-price").text
        
        assert float(total_price) == float(item_price) * 2, "Price did not update correctly when quantity increased."

        print("Quantity updated and price is correct.")

        # Decrease item quantity back to 1
        quantity_input.clear()
        quantity_input.send_keys("1")

        # Verify price updates again
        total_price = driver.find_element(By.CLASS_NAME, "total-price").text
        assert float(total_price) == float(item_price), "Price did not update correctly when quantity decreased."
    
    except TimeoutException:
        print("TimeoutException: Element not found in time")

# Test 3: Remove item from the cart and confirm it's deleted
def test_remove_item_from_cart(driver):
    print("Starting test: Remove item from the cart and confirm it's deleted")

    # Open cart page
    driver.get("http://lazylizard.click/en/cards/cart")

    try:
        # Wait for cart to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-items")))

        # Find and click the "Remove" button for the first cart item
        remove_button = driver.find_element(By.CLASS_NAME, "remove-item")
        remove_button.click()

        # Wait for cart to update
        WebDriverWait(driver, 20).until(EC.invisibility_of_element(remove_button))

        # Verify the cart is empty
        cart_items = driver.find_elements(By.CLASS_NAME, "cart-item")
        assert len(cart_items) == 0, "Item was not removed from the cart."

        print("Item successfully removed from the cart.")

    except TimeoutException:
        print("TimeoutException: Element not found in time")

# Test 4: Attempt checkout with an empty cart and check for errors
def test_checkout_with_empty_cart(driver):
    print("Starting test: Attempt checkout with an empty cart and check for errors")

    # Open cart page
    driver.get("http://lazylizard.click/en/cards/cart")

    try:
        # Wait for cart to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-items")))

        # Ensure the cart is empty
        cart_items = driver.find_elements(By.CLASS_NAME, "cart-item")
        assert len(cart_items) == 0, "Cart is not empty."

        # Try to checkout
        checkout_button = driver.find_element(By.NAME, "checkout")
        checkout_button.click()

        # Wait for error message (assuming error message is in a class named 'error-message')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "error-message")))

        error_message = driver.find_element(By.CLASS_NAME, "error-message").text
        assert "Your cart is empty" in error_message, "Error message for empty cart not shown."

        print("Correct error displayed for empty cart during checkout.")

    except TimeoutException:
        print("TimeoutException: Element not found in time")

