from Coupon import *
from Person import * #Added standard users for Justin, April and Tyler
from Menu import *


def main():
    customer = Customer()
    customer.Print_Person()
    customer.Remove_Person(2)
    customer.Add_Person("Goodbye", "Hello", "test")
    print("")
    customer.Print_Person()
    customer.Remove_Person(1)
    print("")
    customer.Print_Person()
    
    employee = Employee()
    employee.Add_Person("Test_Two", "Manager", "H@ll@")
    employee.Add_Person("Test_Three", "Manager", "H@ll@")
    employee.Print_Person()
    employee.Remove_Person(4)
    employee.Print_Person()
    
    pizza = Pizza()
    pizza.Print_Pizza_Menu()
    print("")
    pizza.Add_Pizza("Meat Sauce", 30.00, 35.00, 40.00)
    pizza.Print_Pizza_Menu()
    pizza.Remove_Item("Meat Sauce")
    pizza.Print_Pizza_Menu()
    
    side = Side()
    side.Print_Side_Menu()
    print("")
    side.Add_Side("Sweet Sticks", 30.00, 35.00, 40.00)
    side.Print_Side_Menu()
    side.Remove_Item("Sweet Sticks")
    side.Print_Side_Menu()
    
    dessert = Dessert()
    dessert.Print_Dessert_Menu()
    print("")
    dessert.Add_Dessert("Sticks", 30.00)
    dessert.Print_Dessert_Menu()
    dessert.Remove_Item("Sticks")
    dessert.Print_Dessert_Menu()
    
    
    
main()