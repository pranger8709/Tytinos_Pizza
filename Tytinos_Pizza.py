from Coupon import *
from Person import * #Added standard users for Justin, April and Tyler


def main():
    customer = Customer()
    customer.add_customer('Some', 'Person', 'password!')
    customer.print_customer()
main()