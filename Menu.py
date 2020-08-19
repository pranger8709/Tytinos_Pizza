from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy import func

debug = True
Base = declarative_base()

class Menu(Base):
    def __init__(self, name, smallPrice, mediumPrice, largePrice, itemType, active):
        self.name = name
        self.smallPrice = smallPrice
        self.mediumPrice = mediumPrice
        self.largePrice = largePrice
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
            print("{0}: {1} Small: ${2:.2f} Medium: ${3:.2f} Large: ${4:.2f}".format(k, i.name, i.smallPrice, i.mediumPrice, i.largePrice))
        k = 0
        print("Sides")
        for i in self.session.query(Menu).filter(Menu.itemType == 2).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Small: ${2:.2f} Medium: ${3:.2f} Large: ${4:.2f}".format(k, i.name, i.smallPrice, i.mediumPrice, i.largePrice))
        k = 0
        print("Deserts")
        for i in self.session.query(Menu).filter(Menu.itemType == 3).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Price: ${2:.2f}".format(k, i.name, i.smallPrice))
        
    __tablename__ = "menu"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    smallPrice = Column(Integer)
    mediumPrice = Column(Integer)
    largePrice = Column(Integer)
    itemType = Column(Integer)
    active = Column(Integer)
        
class Pizza(Menu):
    def __init__(self):
        engine = create_engine('sqlite:///memory:', echo = False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if session.query(Menu).filter(Menu.itemType == 1).count() == 0:
            self.Add_Pizza_Standard_Item()
        
    
    def Add_Pizza_Standard_Item(self):
        self.session.add_all([Menu(name = 'Cheese', smallPrice = 5.99, mediumPrice = 7.99, largePrice = 9.99, itemType = 1, active = 1),
                             Menu(name = 'Hawaiian', smallPrice = 11.99, mediumPrice = 13.99, largePrice = 15.99, itemType = 1, active = 1),
                             Menu(name = 'Meat Lovers', smallPrice = 11.99, mediumPrice = 13.99, largePrice = 15.99, itemType = 1, active = 1),
                             Menu(name = 'Veggie', smallPrice = 11.99, mediumPrice = 13.99, largePrice = 15.99, itemType = 1, active = 1),
                             Menu(name = 'Buffalo Chicken', smallPrice = 11.99, mediumPrice = 13.99, largePrice = 15.99, itemType = 1, active = 1)])
        self.session.query(Menu)
        self.session.commit()
    
    def Add_Pizza(self, pizza_name, pizza_price):
        self.session.add(Menu(name = pizza_name, price = pizza_price, itemType = 1, active = 1))
        self.session.query(Menu)
        self.session.commit()
    
    def Print_Pizza_Menu(self):
        k = 0
        print("Pizza")
        for i in self.session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Small: ${2:.2f} Medium: ${3:.2f} Large: ${4:.2f}".format(k, i.name, i.smallPrice, i.mediumPrice, i.largePrice))
            
class Side(Menu):
    def __init__(self):
        engine = create_engine('sqlite:///memory:', echo = False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if session.query(Menu).filter(Menu.itemType == 2).count() == 0:
            self.Add_Side_Standard_Item()
        
    
    def Add_Side_Standard_Item(self):
        self.session.add_all([Menu(name = 'Wings', smallPrice = 6.49, mediumPrice = 10.99, largePrice = 25.99, itemType = 2, active = 1),
                             Menu(name = 'Boness Chicken', smallPrice = 5.99, mediumPrice = 9.99, largePrice = 25.99, itemType = 2, active = 1),
                             Menu(name = 'Bread Bites', smallPrice = 2.99, mediumPrice = 5.00, largePrice = 8.99, itemType = 2, active = 1)])
        self.session.query(Menu)
        self.session.commit()
    
    def Add_Side(self, side_name, side_price):
        self.session.add(Menu(name = side_name, price = side_price, itemType = 2, active = 1))
        self.session.query(Menu)
        self.session.commit()
    
    def Print_Side_Menu(self):
        k = 0
        print("Sides")
        for i in self.session.query(Menu).filter(Menu.itemType == 2).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Small: ${2:.2f} Medium: ${3:.2f} Large: ${4:.2f}".format(k, i.name, i.smallPrice, i.mediumPrice, i.largePrice))
        

class Dessert(Menu):
    def __init__(self):
        engine = create_engine('sqlite:///memory:', echo = False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if session.query(Menu).filter(Menu.itemType == 3).count() == 0:
            self.Add_Dessert_Standard_Item()
        
    
    def Add_Dessert_Standard_Item(self):
        self.session.add_all([Menu(name = 'Chocolate Lava Crunch Cake', smallPrice = 4.99, mediumPrice = None, largePrice = None, itemType = 3, active = 1),
                             Menu(name = 'Marbled Cookie Brownie', smallPrice = 6.49, mediumPrice = None, largePrice = None, itemType = 3, active = 1),
                             Menu(name = 'Cinna Stix', smallPrice = 4.99, mediumPrice = None, largePrice = None, itemType = 3, active = 1)])
        self.session.query(Menu)
        self.session.commit()
    
    def Add_Dessert(self, side_name, side_price):
        self.session.add(Menu(name = side_name, price = side_price, itemType = 3, active = 1))
        self.session.query(Menu)
        self.session.commit()
    
    def Print_Dessert_Menu(self):
        k = 0
        print("Deserts")
        for i in self.session.query(Menu).filter(Menu.itemType == 3).filter(Menu.active == 1).order_by(Menu.id):
            k += 1
            print("{0}: {1} Price: ${2:.2f}".format(k, i.name, i.smallPrice))

if __name__ == '__main__':
    engine = create_engine('sqlite:///memory:', echo = False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    pizza = Pizza()
    dessert = Dessert()
    side = Side()
