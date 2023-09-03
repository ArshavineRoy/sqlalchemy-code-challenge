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
    # Query for all Restaurant instances
    restaurant1 = session.query(Restaurant).first()
    customer1 = session.query(Customer).first()
    review1 = session.query(Review).first()

    # Now 'restaurants' is a list containing all Restaurant instances in your database
    # print(restaurant1)
    # print(customer1)
    print(restaurant1.all_reviews())