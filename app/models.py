from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
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
    name = (String())
    price = (Integer())


    def __repr__(self):

        return f'Restaurant(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'price={self.price})'


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = (String())
    last_name = (String())

    def __repr__(self):

        return f'Customer(id={self.id}, ' + \
            f'first_name={self.first_name}, ' + \
            f'last_name={self.last_name})'

    

class Review(Base):
    # __tablename__ = 'reviews'

    # id = Column(Integer(), primary_key=True)
    pass
    