from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from Menu import *

Base = declarative_base()


class Cart(Base):
    """ A cart class to keep track of a customer's items. """
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True)
    item = Column(String)
    price = Column(Integer)

    def __init__(self, item=[], price=[]):
        self.item = item
        self.price = price
        self.total_price = 0.0
        self._avg_tax = 0.0554

    def add_item_to_cart(self, item_object):
        self.item.append(item_object.name)
        self.price.append(item_object.priceOne)
        # print("HI \t{}".format(item_object.name))
        # print("HI \t{}".format(item_object.priceOne))

    def remove_item_from_cart(self, item_id):
        print("Remove item from cart")

    def get_item_count(self):
        return len(self._item)

    def calculate_total_price(self):
        for price in self.price:
            self.total_price = price + self.total_price

    def get_price(self):
        self.calculate_total_price()
        return self.total_price

    def print_cart(self):
        print("""********************\nItems in Cart:""")
        for item in self.item:
            print("""{}""".format(item))
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
    # Cart Object
    cart = Cart()
    # Menu objects
    menu = [Pizza(), Side(), Dessert()]

    # for obj in menu:
    #     for item in obj.session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id):
    #         print(item.name)
        # obj.Print_Menu()

    print("\n\n")
    # print(menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0].name)
    # print(menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0].priceOne)
    cart.add_item_to_cart(menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0])
    cart.print_cart()
    print("Cart Total: ${:.2f}".format(cart.get_price()))
    cart.add_item_to_cart(menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[2])
    cart.print_cart()
    print("Cart Total: ${:.2f}".format(cart.get_price()))
    # print(cart.get_item_count())
    