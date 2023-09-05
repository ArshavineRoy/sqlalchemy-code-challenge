#!/usr/bin/env python3
from db import session
from models import Restaurant, Customer, Review

# Example Instances for Testing

restaurant1 = session.query(Restaurant).first()
restaurant_x = session.query(Restaurant).filter_by(id=18).first()

customer1 = session.query(Customer).first()
customer_x = session.query(Customer).filter_by(id=4).first()

review1 = session.query(Review).first()
review_x = session.query(Review).filter_by(id=5).first()


if __name__ == '__main__':
    print(restaurant1.all_reviews())
