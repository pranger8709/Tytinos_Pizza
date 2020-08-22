from Coupon import *
from Person import * #Added standard users for Justin, April and Tyler
from Menu import *
from Cart import *


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
    
    cart = Cart()
    menu = [Pizza(), Side(), Dessert()]

    print("\n\n")
    customer = Customer()
    customer.Print_Person()
    justin = customer.session.query(Person).filter(Person.id == 1)[0]

    cart.print_cart(justin)
    # Adding 1 Cheese Pizza Small to Justin's cart
    cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Small", 
        1
    )
    cart.print_cart(justin)
    # Adding 2 Meat Lover's Pizzas Large to Justin's cart
    cart.print_price_without_tax()
    cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[2], 
        justin,
        "Large", 
        2
    )
    cart.print_cart(justin)
    # Removing an item that doesn't exist
    cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Veggie",
        5.99
    )
    cart.print_cart(justin)
    # Removing an item that does exist
    cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Cheese",
        5.99
    )
    cart.print_cart(justin)
    # Removing an item that does exist but the price does not match the item (Does not remove item)
    cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Meat Lovers",
        5.99
    )
    cart.print_cart(justin)
    
    
main()