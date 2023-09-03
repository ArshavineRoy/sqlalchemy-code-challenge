from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Customer, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # session.query(Restaurant).delete()
    # session.query(Customer).delete()
    # session.query(Review).delete()

    fake = Faker()


    ke_restaurants = [
        "Carnivore Restaurant",
        "Talisman Restaurant",
        "Mama Oliech Restaurant",
        "Nyama Mama",
        "Habesha Restaurant",
        "The Talisman",
        "Java House",
        "Artcaffe",
        "Cafe Deli",
        "Mama Rocks Gourmet Burgers",
        "About Thyme Restaurant",
        "Cafe Maghreb",
        "Lord Erroll Gourmet Restaurant",
        "Que Pasa Bar & Bistro",
        "Sankara Nairobi, Sarabi Rooftop Bar",
        "Anghiti Restaurant",
        "Seven Seafood & Grill",
        "Zen Garden",
        "Hashmi BBQ",
        "Le Palanka"
    ]

    restaurants = []
    for i in range(20):
        restaurant = Restaurant(
            name = random.choice(ke_restaurants),
            price = random.randint(100, 1000)
        )

        session.add(restaurant)
        session.commit()

        restaurants.append(restaurant)

    # print(fake.first_name())
    # print(fake.last_name())


    customers = []
    for i in range (20):
        customer = Customer(
            first_name = fake.first_name(),
            last_name = fake.last_name()                        
        )

        session.add(customer)
        session.commit()

        customers.append(customer)

    # reviews = []
    # for restaurant in restaurants:
    #     for i in range(random.randint(1,5)):
            
    #         review = Review(
    #             star_rating=random.randint(0, 10),
    #             restaurant_id=restaurant.id,
    #         )

    #         reviews.append(review)

    # session.bulk_save_objects(reviews)
    # session.commit()
    # session.close()