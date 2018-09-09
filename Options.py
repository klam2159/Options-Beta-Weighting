'''
Option class take in the last price of the option's stock or index in order to evaluate its expire values
if expire price is the same as current price.

name = stock name
LPsp = Long Put strike price
SPsp = Short Put strike price
SCsp = Short Call strike price
LCsp = Long Call strike price
OP = Option price
contract = # of option contract

'''

from iexfinance import *

class Option(object):
    List = {}
    def __init__(self, name, LPsp, SPsp, SCsp, LCsp, OP, contract =1):
        stock = Stock(name)
        stock.get_open()
        self.name = name
        self.currentPrice = stock.get_price()
        self.LPsp = LPsp
        self.SPsp = SPsp
        self.SCsp = SCsp
        self.LCsp = LCsp
        self.OP = OP
        self.contract = contract
        # Everytime a new Option instance is created it will check to see if the instance name has already been used, if so
        # it will add that instance to the Option.List dict
        if name in Option.List:
            Option.List[name].append(self)
        else:
            Option.List[name] = [self,]
    def LP(self, currentPrice):
        if self.LPsp == 'na':
            return 0
        if currentPrice <= self.LPsp:
            return self.LPsp - currentPrice
        else:
            return 0

    def SP(self, currentPrice):
        if self.SPsp == 'na':
            return 0
        if currentPrice <= self.SPsp:
            return currentPrice - self.SPsp
        else:
            return 0

    def SC(self, currentPrice):
        if self.SCsp == 'na':
            return 0
        if currentPrice <= self.SCsp:
            return 0
        else:
            return self.SCsp - currentPrice

    def LC(self, currentPrice):
        if self.LCsp == 'na':
            return 0
        if currentPrice <= self.LCsp:
            return 0
        else:
            return currentPrice - self.LCsp

    def getValue(self, currentPrice = 0):
        if currentPrice == 0:
            currentPrice = self.currentPrice
        return round(100*self.contract*(self.OP + self.LP(currentPrice) + self.SP(currentPrice) + self.SC(currentPrice) + self.LC(currentPrice)), 2)

    def edit(self, OP, LP = 0, SP=0, SC=0, LC=0):
        if LP != 0:
            self.LPsp = LP
        if SP != 0:
            self.SPsp = SP
        if SC != 0:
            self.SCsp = SC
        if SC != 0:
            self.LCsp = LC
        self.OP += OP

        return print(self)

    def __str__(self):
        return '[' +self.name+' ' +str(self.LPsp)+'/'+str(self.SPsp)+'/'+str(self.SCsp)+'/'+str(self.LCsp)+ ' @'+str(self.OP)+']'