from abc import abstractmethod


class Coupon(object):
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

    # New User Coupon
    coupon = NewUserCoupon()
    cost = Coupon(coupon, total_price)
    print("New User Coupon Total: {}".format(cost.apply_discount()))

    # Weekly Special Coupon
    coupon = WeeklySpecialCoupon()
    cost = Coupon(coupon, total_price)
    print("Weekly Special Coupon Total: {}".format(cost.apply_discount()))

    # Refer a Friend Coupon
    coupon = ReferFriendCoupon()
    cost = Coupon(coupon, total_price)
    print("Refer a Friend Coupon Total: {}".format(cost.apply_discount()))