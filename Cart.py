from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Cart(Base):
    """ A cart class to keep track of a customer's items. """
    def __init__(self, item=[], price=[]):
        self.item = item
        self.price = price
		self._total_price = 0

    def add_item_to_cart(self, item_object):
        self.item.append(item_object.item)
		self.price.append(item_object.price)

    def remove_item_from_cart(self, item_id):
        print("Remove item from cart")

    def get_item_count(self):
        return len(self._item)
		
	def get_price(self):
		for price in self.price:
			self._total_price += price

    def print_cart(self):
        for item in self.item:
            print("""**********\n{}""".format(item))
        print("""**********\n""")


if __name__ == '__main__':
    # Cart Object
    cart = Cart()
    cart.add_item_to_cart("Pizza")
    cart.print_cart()
