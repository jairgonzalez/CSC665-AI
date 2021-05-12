# shopSmart.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""
from __future__ import print_function
import shop


def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """
    "*** YOUR CODE HERE ***"
    # delcaring our best shop variable that I will use to return
    Cheapshop = None
    # using two varaibles to compare prices, the current cost 
    # and the previous cost, I have to set previous cost to 0.0
    # because I can't compare none with a floating point
    Currentcost = None
    Previouscost = 0.0
    # I iterate through the shops each time gettting the cost of
    # the total price of our order 
    for shop in fruitShops:
        Currentcost = shop.getPriceOfOrder(orderList)
    # if statement checks if out previous cost was cheaper than our 
    # current cost, if so we set out previous to our current 
    # and continue iterating through the shops
        if Currentcost > Previouscost and Previouscost != 0.0:
            Previouscost = Currentcost
       # our else statement is if the current cost is the best
       # so we set our previous to the current and the current shop 
       # that we are on is our best shop
        else:
                Previouscost = Currentcost
                Cheapshop = shop

    return Cheapshop


if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orders = [('apples', 1.0), ('oranges', 3.0)]
    dir1 = {'apples': 2.0, 'oranges': 1.0}
    shop1 = shop.FruitShop('shop1', dir1)
    dir2 = {'apples': 1.0, 'oranges': 5.0}
    shop2 = shop.FruitShop('shop2', dir2)
    shops = [shop1, shop2]
    print("For orders ", orders, ", the best shop is",
          shopSmart(orders, shops).getName())
    orders = [('apples', 3.0)]
    print("For orders: ", orders, ", the best shop is",
          shopSmart(orders, shops).getName())
