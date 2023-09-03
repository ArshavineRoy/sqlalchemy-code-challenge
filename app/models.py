#!/usr/bin/env python
from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, DateTime, func, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Create an SQLAlchemy engine and session
engine = create_engine('sqlite:///restaurants.db')
Session = sessionmaker(bind=engine)
session = Session()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    price = (Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    reviews = relationship('Review', back_populates='restaurant_review', cascade='all, delete-orphan')
    customers = association_proxy('reviews', 'customer_review',
        creator=lambda cus: Review(customer=cus))


    def __repr__(self):

        return f'Restaurant(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'price={self.price})'
    
    # Instance methods
    # returns a collection of all the reviews for the Restaurant
    def all_reviews(self):
        return session.query(Review).filter_by(restaurant_id=self.id).all()
    
    # returns a collection of all the customers who reviewed the Restaurant
    def all_customers(self):
        # return list({review.customer_review for review in self.reviews})
        return session.query(Customer).distinct().join(Review).filter(Review.restaurant_review == self).all()

    
    

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    reviews = relationship('Review', back_populates='customer_review', cascade='all, delete-orphan')
    restaurants = association_proxy('reviews', 'restaurant_review',
        creator=lambda rs: Review(restaurant=rs))

    def __repr__(self):

        return f'Customer(id={self.id}, ' + \
            f'first_name={self.first_name}, ' + \
            f'last_name={self.last_name})'
    
    # Instance methods
    # returns a collection of all the reviews that the Customer has left
    def all_reviews(self):
        return self.reviews
        # return session.query(Review).filter_by(customer_id=self.id).all()

    # returns a collection of all the restaurants that the Customer has reviewed
    def all_restaurants(self):
        if not self.restaurants:
            return "This customer has not left any restaurant reviews."
        return self.restaurants

    # returns the full name of the customer
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    # returns the restaurant instance that has the highest star rating from this customer
    def favorite_restaurant(self):

        reviews = self.all_reviews()

        if not reviews:
            return "Customer has no reviews for any restaurant."
        
        highest_rating_review = max(reviews, key=lambda review: review.star_rating)
        return session.query(Restaurant).filter_by(id=highest_rating_review.restaurant_id).first()
    


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)

    star_rating = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    restaurant_review = relationship('Restaurant', back_populates='reviews')
    customer_review = relationship('Customer', back_populates='reviews')

    def __repr__(self):

        return f'Review(id={self.id}, ' + \
            f'star_rating={self.star_rating}, ' + \
            f'restaurant_id={self.restaurant_id})'

    # Instance methods
    # returns the Customer instance for this review
    def customer(self):
        return session.query(Customer).filter_by(id=self.customer_id).first()
    
    # returns the restaurant instance for this review
    def restaurant(self):
        return session.query(Restaurant).filter_by(id=self.restaurant_id).first()
    

if __name__ == '__main__':

    # Instances for testing
    restaurant1 = session.query(Restaurant).first()
    customer1 = session.query(Customer).first()
    customer2 = session.query(Customer).filter_by(id=2).first()
    # customer2_reviews = session.query(Review).filter_by(customer_id=2).all()
   
    review1 = session.query(Review).first()

    # print(restaurant1)
    print(customer1.favorite_restaurant())
    # print(customer2.all_restaurants())

    # print(restaurant1.all_customers())