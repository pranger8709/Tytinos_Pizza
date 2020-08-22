from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from Menu import *
from Person import *


Base = declarative_base()


class Cart(Base):
    """ A cart class to keep track of a customer's items and the item's associated price. """
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True)
    item = Column(String)
    price = Column(Float)
    person_id = Column(Integer)
    quantity = Column(Integer)

    def __init__(self, item=None, price=None, person_id=None, quantity=None):
        self.db_engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()
        self.item = item
        self.price = price
        self.person_id = person_id
        self.quantity = quantity
        self.total_price = 0.0
        self.total_tax = 0.0
        self._avg_state_sales_tax = 0.0554

    def add_data(self, coupon_type, coupon_discount):
        self.session.add(Coupon(type=coupon_type, discount=coupon_discount))
        self.session.commit()

    def add_item_to_cart(self, item_object, person_object, item_size, item_quantity):
        if(item_size == "Small"):
            for i in range(item_quantity):
                self.session.add(Cart(item=item_object.name, price=item_object.priceOne, person_id=person_object.id, quantity=item_quantity))
                self.session.commit()
                self.add_item_price_to_total_price(item_object.priceOne)
        elif(item_size == "Medium"):
            for i in range(item_quantity):
                self.session.add(Cart(item=item_object.name, price=item_object.priceTwo, person_id=person_object.id, quantity=item_quantity))
                self.session.commit()
                self.add_item_price_to_total_price(item_object.priceTwo)
        elif(item_size == "Large"):
            for i in range(item_quantity):
                self.session.add(Cart(item=item_object.name, price=item_object.priceThree, person_id=person_object.id, quantity=item_quantity))
                self.session.commit()
                self.add_item_price_to_total_price(item_object.priceThree)

    def remove_item_from_cart(self, item_id):
        print("Remove item from cart")

    def add_item_price_to_total_price(self, item_price):
        self.total_price = self.total_price + item_price

    def calculate_total_tax_price(self):
        self.total_tax = self.total_price * self._avg_state_sales_tax

    def get_price(self, person_object):
        return self.total_price

    def print_cart(self, person_object):
        print("""********************\nItems in Cart:""")
        for i in self.session.query(Cart).filter(Cart.person_id == person_object.id).order_by(Cart.id):
            print("Item: {0} Price: {1} Customer ID: {2}".format(i.item, i.price, i.person_id))
        print("""********************\n""")


class Checkout(Cart):
    def __init__(self):
        self.db_engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()

    def teardown(self):
        self.session.close() # or remove()


if __name__ == '__main__':
    cart = Cart()
    menu = [Pizza(), Side(), Dessert()]

    print("\n\n")
    customer = Customer()
    customer.Print_Person()
    justin = customer.session.query(Person).filter(Person.id == 1)[0]

    cart.print_cart(justin)
    cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Small", 
        1
    )
    cart.print_cart(justin)
    print("Cart Total: ${:.2f}".format(cart.get_price(justin)))
    cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[2], 
        justin,
        "Large", 
        2
    )
    cart.print_cart(justin)
    print("Cart Total: ${:.2f}".format(cart.get_price(justin)))
    