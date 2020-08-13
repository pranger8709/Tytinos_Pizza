from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Cart(Base):
    """ A cart class to keep track of a customer's items. """
    def __init__(self, item=[], price=None):
        self._item = item
        self._price = price

    def add_item_to_cart(self, new_item):
        self._item.append(new_item)

    def get_item_count(self):
        return len(self._item)

    def remove_item_from_cart(self, item_id):
        print("Remove item from cart")

    def print_cart(self):
        for item in self._item:
            print("""**********\n{}""".format(item))
        print("""**********\n""")


if __name__ == '__main__':
    # Cart Object
    cart = Cart()
    cart.add_item_to_cart("Pizza")
    cart.print_cart()
