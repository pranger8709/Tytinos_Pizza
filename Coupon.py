from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import func


Base = declarative_base()


class Coupon(Base):
    """ A class which uses the strategy design pattern to apply a coupon discount to total price before taxes.
        A database will be used because we must also track the person_id so that the same person cannot 
        just keep using the same coupon discount."""
    __tablename__ = 'coupon'
    
    id = Column(Integer, primary_key=True)
    coupon_type = Column(String)
    discount = Column(Float)
    person_id = Column(Integer)
    active = Column(Integer)

    def __init__(self, coupon_type=None, discount=None, person_id=None, active=1):
        self.db_engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()
        self.coupon_type = coupon_type
        self.discount = discount
        self.person_id = person_id
        self.active = active

    def add_standard_coupon_types(self):
        self.session.add(Coupon(coupon_type="New User", discount=0.20, person_id=0))
        self.session.add(Coupon(coupon_type="Weekly Special", discount=0.15, person_id=0))
        self.session.add(Coupon(coupon_type="Refer Friend", discount=0.25, person_id=0))
        self.session.commit()

    def get_discount_amount_from_coupon_name(self, coupon_type_name):
        discount_amount = self.session.query(Coupon).filter(Coupon.coupon_type == coupon_type_name)
        return discount_amount[0].discount
    
    def apply_coupon_to_cart_for_person_id(self, coupon_type_name, discount_amount, cart_object, person_object):
        self.session.add(Coupon(coupon_type=coupon_type_name, discount=discount_amount, person_id=person_object.id))
        self.session.commit()
        cart_object.set_discount(discount_amount)


    def check_if_person_id_has_used_coupon(self, coupon_type_name, person_object):
        result_list = [
            p for (p,) in self.session.query(func.count(Coupon.coupon_type))
            .filter(Coupon.coupon_type == coupon_type_name)
            .filter(Coupon.person_id == person_object.id)
        ]
        return result_list[0] == 1

    def print_coupon_table(self):
        print("""********************\nCoupons:""")
        for i in self.session.query(Coupon):
            print("Type: {0} Discount: {1} Person ID: {2} Active: {3}".format(i.coupon_type, i.discount, i.person_id, i.active))
        print("""********************\n""")


class Strategy(object):
    @abstractmethod
    def get_discount_amount(self, coupon_type_name):
        """ Get the discount amount from the discount name """
    
    @abstractmethod
    def apply_coupon_to_cart_for_person_id(self, coupon_object, cart_object, person_object):
        """ Apply the coupon to the person_id. This will prevent a customer from using the same coupon multiple times. """

    @abstractmethod
    def check_if_person_id_has_used_coupon(self, coupon_object, person_object):
        """ Returns true if the customer has already used the coupon. """

class NewUserCoupon(Strategy):
    def __init__(self):
        self.coupon_name = "New User"
    
    def get_discount_amount(self, coupon_object):
        return coupon_object.get_discount_amount_from_coupon_name(self.coupon_name)

    def apply_coupon_to_cart_for_person_id(self, coupon_object, cart_object, person_object):
        coupon_object.apply_coupon_to_cart_for_person_id(self.coupon_name, self.get_discount_amount(coupon_object), cart_object, person_object)

    def check_if_person_id_has_used_coupon(self, coupon_object, person_object):
        return coupon_object.check_if_person_id_has_used_coupon(self.coupon_name, person_object)


class WeeklySpecialCoupon(Strategy):
    def __init__(self):
        self.coupon_name = "Weekly Special"
    
    def get_discount_amount(self, coupon_object):
        return coupon_object.get_discount_amount_from_coupon_name(self.coupon_name)

    def apply_coupon_to_cart_for_person_id(self, coupon_object, cart_object, person_object):
        coupon_object.apply_coupon_to_cart_for_person_id(self.coupon_name, self.get_discount_amount(coupon_object), cart_object, person_object)

    def check_if_person_id_has_used_coupon(self, coupon_object, person_object):
        return coupon_object.check_if_person_id_has_used_coupon(self.coupon_name, person_object)


class ReferFriendCoupon(Strategy):
    def __init__(self):
        self.coupon_name = "Refer Friend"
    
    def get_discount_amount(self, coupon_object):
        return coupon_object.get_discount_amount_from_coupon_name(self.coupon_name)

    def apply_coupon_to_cart_for_person_id(self, coupon_object, cart_object, person_object):
        coupon_object.apply_coupon_to_cart_for_person_id(self.coupon_name, cart_object, self.get_discount_amount(coupon_object), cart_object, person_object)

    def check_if_person_id_has_used_coupon(self, coupon_object, person_object):
        return coupon_object.check_if_person_id_has_used_coupon(self.coupon_name, person_object)


if __name__ == '__main__':
    # Coupon Database ORM
    coupon = Coupon()
    coupon.add_standard_coupon_types()
    coupon.print_coupon_table()

    # Instantiate coupon objects using Strategy Design Pattern
    new_user_coupon = NewUserCoupon()
    weekly_special_coupon = WeeklySpecialCoupon()
    refer_friend_coupon = ReferFriendCoupon()
    print(new_user_coupon.get_discount_amount(coupon))
    print(weekly_special_coupon.get_discount_amount(coupon))
    print(refer_friend_coupon.get_discount_amount(coupon))
    
