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
    
    def Add_Person(self, first_name, last_name, pass_word):
        pass
    
    def Remove_Person(self, id):
        self.session.query(Person).filter(Person.id == id).update({Person.active: 0}, synchronize_session='evaluate')
        self.session.query(Person)
        self.session.commit()
    
    def Print_Person(self):
        pass
    
    __tablename__ = "person"
    
    id = Column(Integer, primary_key = True)
    firstName = Column(String)
    lastName = Column(String)
    password = Column(String)
    personType = Column(Integer)
    active = Column(Integer)

class Customer(Person):
    def __init__(self):
        engine = create_engine('sqlite:///:memory:', echo = False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if self.session.query(Person).filter(Person.personType == 1).count() == 0:
            self.Add_Standard_Customers()
        
    def Add_Person(self, first_name, last_name, pass_word):
        self.session.add(Person(firstName = first_name, lastName = last_name, password = pass_word, personType = 1, active = 1))
        self.session.query(Person)
        self.session.commit()
          
    def Add_Standard_Customers(self):
        self.session.add_all([Person(firstName = 'Justin', lastName = 'Conway', password = 'P@ssw@rd', personType = 1, active = 1),
                             Person(firstName = 'Tyler', lastName = 'Pranger', password = 'P@ssw@rd', personType = 1, active = 1),
                             Person(firstName = 'April', lastName = 'Adams', password = 'P@ssw@rd', personType = 1, active = 1)])
        self.session.query(Person)
        self.session.commit()
    
    def Print_Person(self):
        for i in self.session.query(Person).filter(Person.personType == 1).filter(Person.active == 1).order_by(Person.id):
            print("First Name: {0} Last Name: {1} Customer ID: {2}".format(i.firstName, i.lastName, i.id))

class Employee(Person):
    def __init__(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def Add_Person(self, first_name, last_name, pass_word):
        self.session.add(Person(firstName = first_name, lastName = last_name, password = pass_word, personType = 2, active = 1))
        self.session.query(Person)
        self.session.commit()
    
    def Print_Person(self):
        for i in self.session.query(Person).filter(Person.personType == 2).filter(Person.active == 1).order_by(Person.id):
            print("First Name: {0} Last Name: {1} Employee ID: {2}".format(i.firstName, i.lastName, i.id))
        