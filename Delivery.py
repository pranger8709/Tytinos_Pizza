from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from Menu import *
from Person import *


Base = declarative_base()


class Delivery(Base):
    """ A delivery class to give the customer a choice between Delivery and store pickup. """
    __tablename__ = 'delivery'
    
    id = Column(Integer, primary_key=True)
    delivery_type = Column(String)
    delivery_price = Column(Float)
    active = Column(Integer)

    def __init__(self, delivery_type=None, delivery_price=None, active=1):
        self.db_engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()
        self.delivery_type = delivery_type
        self.delivery_price = delivery_price
        self.active = active

    def get_delivery_price_from_deliver_type_name(self, delivery_type_name):
        delivery_type = self.session.query(Delivery).filter(Delivery.delivery_type == delivery_type_name)
        return delivery_type[0].delivery_price

    def add_delivery_type(self, delivery_type_name, delivery_price):
        self.session.add(Delivery(delivery_type=delivery_type_name, delivery_price=delivery_price))
        self.session.commit()

    def add_standard_delivery_types(self):
        self.session.add(Delivery(delivery_type="Delivery", delivery_price=3.99))
        self.session.add(Delivery(delivery_type="Pick up", delivery_price=0.00))
        self.session.add(Delivery(delivery_type="Door Dash", delivery_price=3.99))
        self.session.commit()

    def remove_delivery_type(self, delivery_type_name, delivery_type_price):
        if(self.does_delivery_type_exist(delivery_type_name, delivery_type_price)):
            self.session.query(Delivery).filter(Delivery.delivery_type == delivery_type_name).filter(Delivery.delivery_price == delivery_type_price).update({Delivery.active: 0}, synchronize_session='evaluate')
            self.session.commit()
        else:
            print("Warning: That delivery type does not exist. No delivery type was removed.")
    
    def does_delivery_type_exist(self, delivery_type_name, delivery_type_price):
        result_list = [
            p for (p,) in self.session.query(func.count(Delivery.delivery_type))
            .filter(Delivery.delivery_type == delivery_type_name)
            .filter(Delivery.delivery_price == delivery_type_price)
        ]
        return result_list[0] == 1
    
    def print_delivery_types(self):
        print("""********************\nDelivery Types:""")
        for i in self.session.query(Delivery):
            print("Type: {0} Price: {1} Active: {2}".format(i.delivery_type, i.delivery_price, i.active))
        print("""********************\n""")


if __name__ == '__main__':
    d = Delivery()
    d.add_standard_delivery_types()
    print(d.does_delivery_type_exist("Delivery", 3.99))
    print(d.does_delivery_type_exist("Pick up", 0.00))
    print(d.does_delivery_type_exist("Door Dash", 3.99))
    d.print_delivery_types()
    d.remove_delivery_type("Pick up", 0.00)
    d.print_delivery_types()
