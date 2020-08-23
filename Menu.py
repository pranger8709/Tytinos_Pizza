from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy import func

debug = True
Base = declarative_base()

class Menu(Base):
    def __init__(self, name, priceOne, priceTwo, priceThree, itemType, active):
        self.name = name
        self.priceOne = priceOne
        self.priceTwo = priceTwo
        self.priceThree = priceThree
        self.itemType = itemType
        self.active = active
    
    def Remove_Item(self, name):
        self.session.query(Menu).filter(Menu.name == name).update({Menu.active: 0}, synchronize_session='evaluate')
        self.session.commit()
    
    def Print_Menu(self):
        k = 0
        print("Pizza")
        for i in self.session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Small: ${2:.2f} Medium: ${3:.2f} Large: ${4:.2f}".format(k, i.name, i.priceOne, i.priceTwo, i.priceThree))
        k = 0
        print("Sides")
        for i in self.session.query(Menu).filter(Menu.itemType == 2).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Small: ${2:.2f} Medium: ${3:.2f} Large: ${4:.2f}".format(k, i.name, i.priceOne, i.priceTwo, i.priceThree))
        k = 0
        print("Deserts")
        for i in self.session.query(Menu).filter(Menu.itemType == 3).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Price: ${2:.2f}".format(k, i.name, i.priceOne))
        
    __tablename__ = "menu"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    priceOne = Column(Integer)
    priceTwo = Column(Integer)
    priceThree = Column(Integer)
    itemType = Column(Integer)
    active = Column(Integer)
        
class Pizza(Menu):
    def __init__(self):
        engine = create_engine('sqlite:///:memory:', echo = False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if self.session.query(Menu).filter(Menu.itemType == 1).count() == 0:
            self.Add_Pizza_Standard_Item()
        
    
    def Add_Pizza_Standard_Item(self):
        self.session.add_all([Menu(name = 'Cheese', priceOne = 5.99, priceTwo = 7.99, priceThree = 9.99, itemType = 1, active = 1),
                             Menu(name = 'Hawaiian', priceOne = 11.99, priceTwo = 13.99, priceThree = 15.99, itemType = 1, active = 1),
                             Menu(name = 'Meat Lovers', priceOne = 11.99, priceTwo = 13.99, priceThree = 15.99, itemType = 1, active = 1),
                             Menu(name = 'Veggie', priceOne = 11.99, priceTwo = 13.99, priceThree = 15.99, itemType = 1, active = 1),
                             Menu(name = 'Buffalo Chicken', priceOne = 11.99, priceTwo = 13.99, priceThree = 15.99, itemType = 1, active = 1)])
        self.session.query(Menu)
        self.session.commit()
    
    def Add_Pizza(self, pizza_name, price_one, price_two, price_three):
        self.session.add(Menu(name = pizza_name, priceOne = price_one, priceTwo = price_two, priceThree =  price_three, itemType = 1, active = 1))
        self.session.query(Menu)
        self.session.commit()
    
    def Print_Pizza_Menu(self):
        k = 0
        print("Pizza")
        for i in self.session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Small: ${2:.2f} Medium: ${3:.2f} Large: ${4:.2f}".format(k, i.name, i.priceOne, i.priceTwo, i.priceThree))
            
class Side(Menu):
    def __init__(self):
        engine = create_engine('sqlite:///:memory:', echo = False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if self.session.query(Menu).filter(Menu.itemType == 2).count() == 0:
            self.Add_Side_Standard_Item()
        
    
    def Add_Side_Standard_Item(self):
        self.session.add_all([Menu(name = 'Wings', priceOne = 6.49, priceTwo = 10.99, priceThree = 25.99, itemType = 2, active = 1),
                             Menu(name = 'Boness Chicken', priceOne = 5.99, priceTwo = 9.99, priceThree = 25.99, itemType = 2, active = 1),
                             Menu(name = 'Bread Bites', priceOne = 2.99, priceTwo = 5.00, priceThree = 8.99, itemType = 2, active = 1)])
        self.session.query(Menu)
        self.session.commit()
    
    def Add_Side(self, side_name, price_one, price_two, price_three):
        self.session.add(Menu(name = side_name, priceOne = price_one, priceTwo = price_two, priceThree = price_three, itemType = 2, active = 1))
        self.session.query(Menu)
        self.session.commit()
    
    def Print_Side_Menu(self):
        k = 0
        print("Sides")
        for i in self.session.query(Menu).filter(Menu.itemType == 2).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Small: ${2:.2f} Medium: ${3:.2f} Large: ${4:.2f}".format(k, i.name, i.priceOne, i.priceTwo, i.priceThree))
        

class Dessert(Menu):
    def __init__(self):
        engine = create_engine('sqlite:///:memory:', echo = False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if self.session.query(Menu).filter(Menu.itemType == 3).count() == 0:
            self.Add_Dessert_Standard_Item()
        
    
    def Add_Dessert_Standard_Item(self):
        self.session.add_all([Menu(name = 'Chocolate Lava Crunch Cake', priceOne = 4.99, priceTwo = None, priceThree = None, itemType = 3, active = 1),
                             Menu(name = 'Marbled Cookie Brownie', priceOne = 6.49, priceTwo = None, priceThree = None, itemType = 3, active = 1),
                             Menu(name = 'Cinna Stix', priceOne = 4.99, priceTwo = None, priceThree = None, itemType = 3, active = 1)])
        self.session.query(Menu)
        self.session.commit()
    
    def Add_Dessert(self, side_name, dessert_price):
        self.session.add(Menu(name = side_name, priceOne = dessert_price, priceTwo = None, priceThree = None, itemType = 3, active = 1))
        self.session.query(Menu)
        self.session.commit()
    
    def Print_Dessert_Menu(self):
        k = 0
        print("Deserts")
        for i in self.session.query(Menu).filter(Menu.itemType == 3).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Price: ${2:.2f}".format(k, i.name, i.priceOne))

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo = False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    pizza = Pizza()
    dessert = Dessert()
    side = Side()
