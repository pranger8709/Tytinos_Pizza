from Coupon import *
from Person import * #Added standard users for Justin, April and Tyler


def main():
    customer = Customer()
    customer.print_customer()
    customer.remove_customer(2)
    print("")
    customer.print_customer()
    customer.remove_customer(1)
    print("")
    customer.print_customer()
    
main()