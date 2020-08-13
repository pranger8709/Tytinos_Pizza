from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update


debug = True
Base = declarative_base()

class Person(Base):
    def __init__(self, firstName, lastName, password, personType, active):
        self.firstName = firstName
        self.lastName = lastName
        self.personType = personType
        self.password = password
        self.active = active
    
    __tablename__ = "person"
    
    id = Column(Integer, primary_key = True)
    firstName = Column(String)
    lastName = Column(String)
    password = Column(String)
    personType = Column(Integer)
    active = Column(Integer)

class Customer(Person):
    def __init__(self):
        engine = create_engine('sqlite:///memory:', echo=False)
        if engine.dialect.has_table(engine, 'person') == True:
            Person.__table__.drop(engine)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.add_standard_customers()
        
    def add_customer(self, first_name, last_name, pass_word):
        self.session.add(Person(firstName = first_name, lastName = last_name, password = pass_word, personType = 1, active = 1))
        self.session.query(Person)
        self.session.commit()
        
    def remove_customer(self, id):
        self.session.query(Person).filter(Person.id == id).update({Person.active: 0}, synchronize_session='evaluate')
        self.session.commit()
        
    def add_standard_customers(self):
        self.session.add_all([Person(firstName = 'Justin', lastName = 'Conway', password = 'P@ssw@rd', personType = 1, active = 1),
                             Person(firstName = 'Tyler', lastName = 'Pranger', password = 'P@ssw@rd', personType = 1, active = 1),
                             Person(firstName = 'April', lastName = 'Adams', password = 'P@ssw@rd', personType = 1, active = 1)])
        self.session.query(Person)
        self.session.commit()
    
    def print_customer(self):
        for i in self.session.query(Person).filter(Person.personType == 1).filter(Person.active == 1).order_by(Person.id):
            print(i.firstName, i.lastName)

class Employee(Person):
    def __init__(self):
        engine = create_engine('sqlite:///memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def add_employee(self, first_name, last_name, pass_word):
        self.session.add(Person(firstName = first_name, lastName = last_name, password = pass_word, personType = 2))
        self.session.query(Person)
        self.session.commit()
    
    def print_employee(self):
        for i in self.session.query(Person).filter(Person.personType == 2).filter(Person.active == 1).order_by(Person.id):
            print(i.firstName, i.lastName, "employee")

# class Drop_Person_Table(Person):
#     def __init__(self):
#         engine = create_engine('sqlite:///memory:', echo=False)
#         Base.metadata.create_all(engine)
#         if engine.dialect.has_table(engine, 'person') == True:
#             Person.__table__.drop(engine)
        
# def main():
# customer = Customer()
#     customer.add_standard_customers()
# if debug == True:
#         customer.print_customer()
# main()
        