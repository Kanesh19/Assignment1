import pandas as pd
import numpy as np
import random

from faker import Faker

class Datas:
    def __init__(self):
        self.fake = Faker()

    def customer_table(self, num_customer=150):
        customers = []
        for _ in range(num_customer):
            customers.append({
                "customer_id": _ + 1,
                "name": self.fake.name(),
                "email": self.fake.email(),
                "phone": self.fake.phone_number(),
                "location": self.fake.address(),
                "signup_date": self.fake.date_this_year(),
                "is_premium": random.choice([0, 1]),
                "preferred_cuisine": random.choice(['Indian', 'Chinese', 'Japanese', 'Italy']),
                "total_orders": random.randint(1, 100),
                "average_rating": random.randint(0, 5)
            })
        df = pd.DataFrame(customers)
        df.drop(columns=["signup_date"], inplace=True)
        return df
    print(customer_table)



    def restaurant_table(self, num_restaurant=150):
        restaurants = []
        for _ in range(num_restaurant):
            restaurants.append({
            "restaurant_id": _ + 1,
            "name": self.fake.name(),
            "cuisine_type": random.choice(['Indian', 'Chinese', 'Japanese', 'France', 'Italy']),
            "location": self.fake.address(),
            "owner_name": self.fake.name(),
            "average_delivery_time": random.randint(10, 60),
            "contact_number": self.fake.phone_number(),
            "rating": random.randint(0, 5),
            "total_orders":random.randint(1, 1000),
            "is_active": random.choice([0, 1])
            })
        df = pd.DataFrame(restaurants)
        df.drop(columns=['contact_number'], inplace=True)
        return df
        
    print(restaurant_table)


    def order_table(self, num_order=150):
        customers = self.customer_table()
        restaurants = self.restaurant_table()
        orders = []
        for _ in range(num_order):
            orders.append({
                "order_id": _+1,
                "customer_id": random.choice(customers["customer_id"]),
                "restaurant_id": random.choice(restaurants["restaurant_id"]),
                "order_date": self.fake.date_this_year(),
                "delivery_time": random.randint(10, 60),
                "status": self.fake.random_element([ 'Pending', 'Delivered', 'Cancelled']),
                "total_amount": random.randint(10, 5000),
                "payment_mode": self.fake.random_element(['Credit Card', 'Cash', 'UPI']),
                "discount_applied": self.fake.random_element(['10%', '15%', '20%', '25%', '40%']),
                "feedback_rating": random.randint(0, 5)
            })
        return pd.DataFrame(orders)
    print(order_table)


    def delivery_table(self, num_delivery=150):
        orders = self.order_table()
        delivery = []
        for _ in range(num_delivery):
            delivery.append({
                "delivery_id": _+1,
                "order_id": random.choice(orders["order_id"]),
                "delivery_person_id": _+1,
                "delivery_status":self.fake.random_element(['On the way', 'Delivered']),
                "distance": random.randint(1, 20),
                "delivery_time": random.randint(10, 60),
                "estimated_time":random.randint(1, 40),
                "delivery_fee": random.randint(15, 1000),
                "vehicle_type": self.fake.random_element(['Bike', 'Car'])
            })
        return pd.DataFrame(delivery)
    print(delivery_table)
    



