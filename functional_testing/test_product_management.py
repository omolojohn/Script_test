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

# Test: Add a new product with all required details (name, price, description, image, category)
def test_add_new_product(driver):
    print("Starting test: Add a new product")

    # Log in as a seller
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("seller_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("seller_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Navigate to product management page
        product_management_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Product Management"))
        )
        product_management_tab.click()

        # Click to add a new product
        add_product_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "add_product"))
        )
        add_product_button.click()

        # Fill in the product details
        name_field = driver.find_element(By.NAME, "product_name")
        name_field.send_keys("New Product")

        price_field = driver.find_element(By.NAME, "product_price")
        price_field.send_keys("100")

        description_field = driver.find_element(By.NAME, "product_description")
        description_field.send_keys("This is a new product.")

        image_field = driver.find_element(By.NAME, "product_image")
        image_field.send_keys("/path/to/product_image.jpg")

        category_field = driver.find_element(By.NAME, "product_category")
        category_field.send_keys("Electronics")

        # Submit the form
        submit_button = driver.find_element(By.NAME, "submit_product")
        submit_button.click()

        # Verify the product was added by checking the success message or product listing
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-list")))

        product_list = driver.find_element(By.CLASS_NAME, "product-list")
        assert "New Product" in product_list.text
        print("Product successfully added.")

    except TimeoutException:
        print("TimeoutException: Add new product test failed.")

# Test: Attempt to add a product with missing details and verify validation messages
def test_add_product_with_missing_details(driver):
    print("Starting test: Add product with missing details")

    # Log in as a seller
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("seller_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("seller_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Navigate to product management page
        product_management_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Product Management"))
        )
        product_management_tab.click()

        # Click to add a new product
        add_product_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "add_product"))
        )
        add_product_button.click()

        # Leave required fields blank (e.g., name and price)
        price_field = driver.find_element(By.NAME, "product_price")
        price_field.send_keys("100")

        description_field = driver.find_element(By.NAME, "product_description")
        description_field.send_keys("This is a new product.")

        # Submit the form with missing fields (name)
        submit_button = driver.find_element(By.NAME, "submit_product")
        submit_button.click()

        # Verify the validation message
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "validation-message")))
        validation_message = driver.find_element(By.CLASS_NAME, "validation-message")
        assert "Product name is required" in validation_message.text
        print("Validation message for missing name verified.")

    except TimeoutException:
        print("TimeoutException: Add product with missing details test failed.")

# Test: Edit an existing product and ensure changes are saved
def test_edit_product(driver):
    print("Starting test: Edit an existing product")

    # Log in as a seller
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("seller_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("seller_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Navigate to product management page
        product_management_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Product Management"))
        )
        product_management_tab.click()

        # Find and click on the product to edit
        edit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "edit_product"))
        )
        edit_button.click()

        # Edit the product details
        name_field = driver.find_element(By.NAME, "product_name")
        name_field.clear()
        name_field.send_keys("Updated Product Name")

        price_field = driver.find_element(By.NAME, "product_price")
        price_field.clear()
        price_field.send_keys("120")

        description_field = driver.find_element(By.NAME, "product_description")
        description_field.clear()
        description_field.send_keys("Updated description for the product.")

        # Submit the edited product details
        submit_button = driver.find_element(By.NAME, "submit_product")
        submit_button.click()

        # Verify that the changes are saved
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-list")))

        product_list = driver.find_element(By.CLASS_NAME, "product-list")
        assert "Updated Product Name" in product_list.text
        print("Product edited successfully.")

    except TimeoutException:
        print("TimeoutException: Edit product test failed.")

# Test: Delete a product and confirm it no longer appears in listings
def test_delete_product(driver):
    print("Starting test: Delete a product and confirm deletion")

    # Log in as a seller
    driver.get("https://lazylizard.click/en/login")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username")))
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("seller_username")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("seller_password")

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Navigate to product management page
        product_management_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Product Management"))
        )
        product_management_tab.click()

        # Find and click on the product to delete
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "delete_product"))
        )
        delete_button.click()

        # Confirm deletion in the confirmation dialog
        confirmation_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "confirm_delete"))
        )
        confirmation_button.click()

        # Verify that the product no longer appears in the product listings
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-list")))
        product_list = driver.find_element(By.CLASS_NAME, "product-list")
        assert "Updated Product Name" not in product_list.text
        print("Product deleted successfully.")

    except TimeoutException:
        print("TimeoutException: Delete product test failed.")

if __name__ == "__main__":
    pytest.main()
