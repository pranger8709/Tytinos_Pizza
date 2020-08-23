from Coupon import *
from Person import * #Added standard users for Justin, April and Tyler
from Menu import *
from Cart import *
from Delivery import *


# Python application using the 6+ major classes demonstrating the core functionality - GUIs are NOT requiredelivery.
def main():
    # 6+ Major Classes
    customer = Customer()
    employee = Employee()
    justin_cart = Cart()
    menu = [Pizza(), Side(), Dessert()]
    delivery = Delivery()
    coupon = Coupon()

    # Demo Customer Class
    customer.Print_Person()
    customer.Remove_Person(2)
    customer.Remove_Person(3)
    print("\n########As you can see, Customer's 2 and 3 were deleted:")
    customer.Print_Person()
    
    # Demo Employee Class
    print("\n########Add 2 Test Employees \"Test_Two\" and \"Test_Three\" and then remove them:")
    employee.Add_Person("Test_Two", "Manager", "H@ll@")
    employee.Add_Person("Test_Three", "Manager", "H@ll@")
    employee.Print_Person()
    employee.Remove_Person(4)
    employee.Print_Person()

    print("\n########Here is our final Customer List:")
    customer = Customer()
    customer.Print_Person()

    # Declare a customer object. We will modify their account
    justin = customer.session.query(Person).filter(Person.id == 1)[0]

    # Demo the Cart class
    # Adding 1 Cheese Pizza Small to Justin's cart
    justin_cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Small", 
        1
    )
    
    # Adding 2 Meat Lover's Pizzas Large to Justin's cart
    justin_cart.print_price_without_tax()
    justin_cart.add_item_to_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[2], 
        justin,
        "Large", 
        2
    )

    print("\n########Here is Justin's Cart:")
    justin_cart.print_cart(justin)
    
    # Removing an item that doesn't exist
    justin_cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Veggie",
        5.99
    )

    # Removing an item that does exist
    justin_cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Cheese",
        5.99
    )
    
    # Removing an item that does exist but the price does not match the item (Does not remove item)
    justin_cart.remove_item_from_cart(
        menu[0].session.query(Menu).filter(Menu.itemType == 1).filter(Menu.active == 1).order_by(Menu.id)[0], 
        justin,
        "Meat Lovers",
        5.99
    )
    
    # Demo the Delivery class
    delivery.add_standard_delivery_types()

    print("\n########Here are all of the standard Delivery types:")
    delivery.print_delivery_types()
    delivery.remove_delivery_type("Door Dash", 3.99)

    # Declare a delivery type
    selected_delivery_type = delivery.get_delivery_price_from_delivery_type_name("Delivery")

    print("\n########Here we apple the Delivery charge to the total price in our cart:")
    print(selected_delivery_type)
    justin_cart.add_item_price_to_total_price(selected_delivery_type)
    justin_cart.print_cart(justin)

    # Demo Coupon
    print("\n########Here are our standard coupons with their discounts:")
    coupon.add_standard_coupon_types()
    coupon.print_coupon_table()

    # Instantiate coupon objects using Strategy Design Pattern
    new_user_coupon = NewUserCoupon()
    weekly_special_coupon = WeeklySpecialCoupon()
    refer_friend_coupon = ReferFriendCoupon()

    # Apply a coupon to a customer
    print("\n########Here we apply a coupon to Justin's Cart:")
    print("\n\n*******************************************\nNo Discount:")
    justin_cart.print_cart(justin)
    coupon.print_coupon_table()
    print("\n\n*******************************************\nDiscount Applied:")
    new_user_coupon.apply_coupon_to_cart_for_person_id(coupon, justin_cart, justin)
    coupon.print_coupon_table()
    justin_cart.print_cart(justin)
    print("*******************************************\n")

    # Check if coupon has been applied
    print("\n########Here we check to see if our Coupon has been applied:")
    print("Did Justin apply New User coupon? {}".format(new_user_coupon.check_if_person_id_has_used_coupon(coupon, justin)))
    print("Did Justin apply Refer Friend coupon? {}".format(refer_friend_coupon.check_if_person_id_has_used_coupon(coupon, justin)))
    
    
main()