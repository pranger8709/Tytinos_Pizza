from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        Base = declarative_base()
        self.db_engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()

    def teardown(self):
        self.session.remove()

    def add_data(self, data_object):
        self.session.add(data_object)
        self.session.commit()

    def view_data(self, object):
        for instance in self.session.query(object).order_by(object.id):
            print("{}: {}".format(instance.type, instance.discount))


# if __name__ == '__main__':
#     db = Database()
#     db.add_data("New User", 20)
#     db.add_data("Weekly Special", 15)
#     db.add_data("Refer Friend", 25)
#     db.add_data("Monthly Special", 10)
#     db.view_data()
