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
    active = Column(Integer)

    def __init__(self, item=None, price=None, person_id=None, quantity=None, active=1):
        self.db_engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()
        self.item = item
        self.price = price
        self.person_id = person_id
        self.quantity = quantity
        self.active = active
        self.total_price = 0.0
        self.total_price_with_discounts = 0.0
        self.total_tax = 0.0
        self._avg_state_sales_tax = 0.0554
        self.discount = 0.0

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

    def remove_item_from_cart(self, item_object, person_object, search_item_name, search_item_price):
        if(self.is_item_in_cart_for_person(item_object, person_object, search_item_name, search_item_price)):
            self.session.query(Cart).filter(Cart.person_id == person_object.id).filter(Cart.item == item_object.name).update({Cart.active: 0}, synchronize_session='evaluate')
            self.session.commit()
            self.remove_item_price_from_total_price(search_item_price)
        else:
            print("Warning: That item does not exist in {}'s cart. No item was removed.".format(person_object.firstName))

    def is_item_in_cart_for_person(self, item_object, person_object, search_item_name, search_item_price):
        result_list = [p for (p,) in self.session.query(func.count(Cart.item)).filter(Cart.person_id == person_object.id).filter(Cart.item == search_item_name)]
        return result_list[0] == 1

    def set_discount(self, discount):
        self.discount = discount

    def add_item_price_to_total_price(self, item_price):
        self.total_price = self.total_price + item_price

    def remove_item_price_from_total_price(self, item_price):
        self.total_price = self.total_price - item_price

    def calculate_total_without_tax(self):
        self.total_price_with_discounts = self.total_price - (self.total_price * self.discount)

    def calculate_total_with_tax(self):
        self.calculate_total_without_tax()
        self.total_tax = self.total_price_with_discounts + (self.total_price * self._avg_state_sales_tax)

    def print_price_without_tax(self):
        self.calculate_total_without_tax()
        print("Cart Total without Tax: ${:.2f}".format(self.total_price_with_discounts))

    def print_price_with_tax(self):
        self.calculate_total_with_tax()
        print("Cart Total with Tax: ${:.2f}".format(self.total_tax))

    def print_cart(self, person_object):
        print("""********************\n{}'s Cart\n\nItems in Cart:""".format(person_object.firstName))
        for i in self.session.query(Cart).filter(Cart.person_id == person_object.id).filter(Cart.active == 1).order_by(Cart.id):
            print("Item: {0} Price: {1} Customer ID: {2}".format(i.item, i.price, i.person_id))
        self.print_price_without_tax()
        self.print_price_with_tax()
        print("""********************\n""")
    
    def teardown(self):
        self.session.close()


if __name__ == '__main__':
    cart = Cart()
    menu = [Pizza(), Side(), Dessert()]

    print("\n\n")
    customer = Customer()
    customer.Print_Person()
    justin = customer.session.query(Person).filter(Person.id == 1)[0]

    cart.print_cart(justin)
    # Adding 1 Cheese Pizza Small to Justin's cart
    cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Small", 
        1
    )
    cart.print_cart(justin)
    # Adding 2 Meat Lover's Pizzas Large to Justin's cart
    cart.print_price_without_tax()
    cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[2], 
        justin,
        "Large", 
        2
    )
    cart.print_cart(justin)
    # Removing an item that doesn't exist
    cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Veggie",
        5.99
    )
    cart.print_cart(justin)
    # Removing an item that does exist
    cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Cheese",
        5.99
    )
    cart.print_cart(justin)
    # Removing an item that does exist but the price does not match the item (Does not remove item)
    cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Meat Lovers",
        5.99
    )
    cart.print_cart(justin)
    cart.teardown()