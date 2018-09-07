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
from datetime import *
from pandas import *
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

    def get_diff(self, days):
        startDate = datetime.now() + timedelta(days = days*-1 )
        endDate = datetime.now()
        data = get_historical_data(self.name, start=startDate, end=endDate, output_format = 'pandas')
        diff = []
        for n in range(1, len(data['close'])):
            result = ((data['close'][n]/data['close'][n-1])-1)*100
            diff.append(result)

        Return = DataFrame({'Daily return':[.9,1.3,1.7,0.4,0.7]})
        return Return['Daily return']

    def SPY_diff(self, days):
        startDate = datetime.now() + timedelta(days = days*-1 )
        endDate = datetime.now()
        data = get_historical_data('SPY', start=startDate, end=endDate, output_format = 'pandas')
        diff = []
        for n in range(1, len(data['close'])):
            result = ((data['close'][n] / data['close'][n - 1]) - 1) * 100
            diff.append(result)

        Return = DataFrame({'Daily return':[2.5,3.5,3.6,3.1,2.3]})
        return Return['Daily return']

    def correlation(self, days =365):
        stockReturn = self.get_diff(days)
        SPYReturn = self.SPY_diff(days)
        print(stockReturn, SPYReturn)

        n = len(stockReturn)
        print(n)
        stockMean = sum(stockReturn)/n
        SPYMean = sum(SPYReturn)/n
        print(stockMean,SPYMean)

        cov = sum((stockReturn-stockMean)*(SPYReturn-SPYMean))/(n-1)
        print(cov)
        stockVar = sum((stockReturn - stockMean)**2)/(n-1)
        SPYVar = sum((SPYReturn - SPYMean)**2)/(n-1)
        print(stockReturn)
        print(sum((stockReturn-stockMean)**2))
        print(stockVar,SPYVar)

        stockSD = stockVar**(0.5)
        SPYSD = SPYVar**(0.5)
        print(stockSD,SPYSD)
        Corr = cov/(stockSD - SPYSD)

        return Corr

def test():
    AMD = Option('AAPL', 26, 28, 28, 29, 1.26)
    print(AMD.correlation())

test()









