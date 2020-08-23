from Coupon import *
from Person import * #Added standard users for Justin, April and Tyler
from Menu import *
from Cart import *
from Delivery import *


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
    
    # Justin Cart
    justin_cart = Cart()
    menu = [Pizza(), Side(), Dessert()]

    print("\n\n")
    customer = Customer()
    customer.Print_Person()
    justin = customer.session.query(Person).filter(Person.id == 1)[0]

    justin_cart.print_cart(justin)
    # Adding 1 Cheese Pizza Small to Justin's cart
    justin_cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Small", 
        1
    )
    justin_cart.print_cart(justin)
    # Adding 2 Meat Lover's Pizzas Large to Justin's cart
    justin_cart.print_price_without_tax()
    justin_cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[2], 
        justin,
        "Large", 
        2
    )
    justin_cart.print_cart(justin)
    # Removing an item that doesn't exist
    justin_cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Veggie",
        5.99
    )
    justin_cart.print_cart(justin)
    # Removing an item that does exist
    justin_cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Cheese",
        5.99
    )
    justin_cart.print_cart(justin)
    # Removing an item that does exist but the price does not match the item (Does not remove item)
    justin_cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Meat Lovers",
        5.99
    )
    justin_cart.print_cart(justin)
    d = Delivery()
    d.add_standard_delivery_types()
    print(d.does_delivery_type_exist("Delivery", 3.99))
    print(d.does_delivery_type_exist("Pick up", 0.00))
    print(d.does_delivery_type_exist("Door Dash", 3.99))
    d.print_delivery_types()
    d.remove_delivery_type("Door Dash", 3.99)
    d.print_delivery_types()
    selected_delivery_type = d.get_delivery_price_from_deliver_type_name("Delivery")
    print(selected_delivery_type)
    justin_cart.add_item_price_to_total_price(selected_delivery_type)
    justin_cart.print_cart(justin)

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

    # Apply a coupon to a customer
    print("\n\n*******************************************\nNo Discount:")
    justin_cart.print_cart(justin)
    coupon.print_coupon_table()
    print("\n\n*******************************************\nDiscount Applied:")
    new_user_coupon.apply_coupon_to_cart_for_person_id(coupon, justin_cart, justin)
    coupon.print_coupon_table()
    justin_cart.print_cart(justin)
    print("*******************************************\n")

    # Check if coupon has been applied
    print("Did Justin apply New User coupon? {}".format(new_user_coupon.check_if_person_id_has_used_coupon(coupon, justin)))
    print("Did Justin apply Refer Friend coupon? {}".format(refer_friend_coupon.check_if_person_id_has_used_coupon(coupon, justin)))
    
    
main()