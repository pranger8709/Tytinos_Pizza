from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# GLOBALS
Base = declarative_base()


class Coupon(Base):
    def __init__(self, type, discount):
        self.type = type
        self.discount = discount

    __tablename__ = 'coupon'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    discount = Column(Integer)

    def get_discount(self):
        return self.discount / 100

    def __repr__(self):
        return "Type: {}, Discount: {}%".format(self.type, self.discount)


# Use SQLAlchemy to store and retrieve objects from the internal SQLite database
class Database(Coupon):
    def __init__(self):
        self.db_engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()

    def teardown(self):
        self.session.remove()

    def test(self):
        self.add_data("New User", 20)
        self.add_data("Weekly Special", 15)
        self.add_data("Refer Friend", 25)

        # Test if data appears
        assert self.session.query(Coupon).filter(Coupon.discount == 20).first().get_discount() == 0.2
        assert self.session.query(Coupon).filter(Coupon.discount == 15).first().get_discount() == 0.15
        assert self.session.query(Coupon).filter(Coupon.discount == 25).first().get_discount() == 0.25

    def add_data(self, coupon_type, coupon_discount):
        self.session.add(Coupon(type=coupon_type, discount=coupon_discount))
        self.session.commit()

    def view_data(self):
        for instance in self.session.query(Coupon).order_by(Coupon.id):
            print("{}: {}".format(instance.type, instance.discount))


class ApplyCoupon(object):
    """ A class which uses strategy design pattern to apply a coupon discount to total price before taxes. """

    def __init__(self, coupon_type, order_total):
        self._coupon_type = coupon_type
        self._order_total = order_total

    def apply_discount(self):
        return self._coupon_type.apply_discount(self._order_total)


class Strategy(object):
    @abstractmethod
    def apply_discount(self, order_total):
        """ Calculate new total after applying coupon discount amount """


class NewUserCoupon(Strategy):
    def apply_discount(self, order_total):
        return order_total - (order_total * 0.2)


class WeeklySpecialCoupon(Strategy):
    def apply_discount(self, order_total):
        return order_total - (order_total * 0.15)


class ReferFriendCoupon(Strategy):
    def apply_discount(self, order_total):
        return order_total - (order_total * 0.25)


if __name__ == '__main__':
    total_price = 17.49
    db = Database()
    db.test()
    db.add_data("Monthly Special", 10)
    db.view_data()


    # New User Coupon
    # coupon = NewUserCoupon()
    # cost = ApplyCoupon(coupon, total_price)
    # print("New User Coupon Total: {}".format(cost.apply_discount()))
    #
    # # Weekly Special Coupon
    # coupon = WeeklySpecialCoupon()
    # cost = ApplyCoupon(coupon, total_price)
    # print("Weekly Special Coupon Total: {}".format(cost.apply_discount()))
    #
    # # Refer a Friend Coupon
    # coupon = ReferFriendCoupon()
    # cost = ApplyCoupon(coupon, total_price)
    # print("Refer a Friend Coupon Total: {}".format(cost.apply_discount()))
