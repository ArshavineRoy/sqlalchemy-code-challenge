from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, DateTime, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    price = (Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    reviews = relationship('Review', back_populates='restaurant', cascade='all, delete-orphan')
    customers = association_proxy('reviews', 'customer',
        creator=lambda cus: Review(customer=cus))


    def __repr__(self):

        return f'Restaurant(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'price={self.price})'

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    reviews = relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    restaurants = association_proxy('reviews', 'restaurant',
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

    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    def __repr__(self):

        return f'Review(id={self.id}, ' + \
            f'star_rating={self.star_rating}, ' + \
            f'restaurant_id={self.restaurant_id})'