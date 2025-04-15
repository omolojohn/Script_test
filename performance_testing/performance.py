from locust import HttpUser, task, between

class Shopper(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def browse_products(self):
        self.client.get("/en/products")

    @task(2)
    def add_to_cart(self):
        self.client.post("/en/cart/add", json={"product_id": 1, "quantity": 1})

    @task(1)
    def view_cart(self):
        self.client.get("/en/cart")

    @task(1)
    def checkout(self):
        self.client.get("/en/checkout")

# locust -f locustfile.py --host=https://lazylizard.click
