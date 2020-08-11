from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# GLOBALS
Base = declarative_base()
debug = False


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

    """ TODO: MOVE. I believe this will go into the Cart or Menu class. """
    def apply_discount(self):
        return self._coupon_type.apply_discount(self._order_total)

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


if __name__ == '__main__':
    db = Database()
    if debug:
        db.test()
    db.add_data("New User", 20)
    db.add_data("Weekly Special", 15)
    db.add_data("Refer Friend", 25)
    db.add_data("Monthly Special", 10)
    db.view_data()
