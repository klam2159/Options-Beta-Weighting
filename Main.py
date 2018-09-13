from Options import *
from pandas import *
from datetime import *
import matplotlib.pyplot as plt

def plot(Position):
    name = Position
    Position = Option.List[Position][0]
    ref = round(0.75 * Position.currentPrice, 2)
    xVal = []
    yVal = []
    while ref < round(1.25 * Position.currentPrice):
        xVal.append(ref)
        result = 0
        for option in Option.List[name]:
            result += option.getValue(ref)
        yVal.append(result)
        ref += 0.05
    plt.figure(Position.name)
    plt.plot(xVal, yVal)
    plt.axvline(x=Position.currentPrice,color = 'r', linestyle = '--' )
    plt.axhline(y = 0, color = 'g', linestyle = '-')

    plt.title(Position.name)
    plt.grid()
    plt.xlabel('Price')
    plt.ylabel('Expire Value')

class get_stats(object):
    def __init__(self, name, days=730):
        stock = Stock(name)
        stock.get_open()

        start = datetime.now() + timedelta(days = days*-1 )
        end = datetime.now()

        data = get_historical_data(name, start=start, end=end, output_format = 'pandas')
        diff = []
        for n in range(1, len(data['close'])):
            result = ((data['close'][n]/data['close'][n-1])-1)*100
            diff.append(result)
        hold = DataFrame({'Daily Return': diff})
        dailyReturn = hold['Daily Return']

        n = len(dailyReturn)
        mean = sum(dailyReturn)/n
        standardDeviation = (sum((dailyReturn - mean)**2)/n)**.5

        self.name = name
        self.currentPrice = stock.get_price()
        self.SD = standardDeviation
        self.DR = dailyReturn
        self.size = n
        self.mean = mean

    def get_price(self):
        return self.currentPrice

def Get_Beta(sample, index ):
    cov = sum((sample.DR - sample.mean)*(index.DR - index.mean))/(index.size-1)
    return cov/index.SD

def Beta_weight(OptionDict):
    INDEX = get_stats('SPY')
    SPYPrice = INDEX.get_price()
    ref = .92
    xVal = []
    yVal = []
    while ref < 1.08:
        price = SPYPrice * ref
        xVal.append(price)
        portfolioValue = 0
        for key in Option.List.keys():
            stock = get_stats(key)
            for position in Option.List[key]:
                stockprice = (Get_Beta(stock,INDEX)*(price/SPYPrice - 1)+1)*stock.currentPrice
                print(stockprice, price)
                currentValue = position.getValue(stockprice)
                portfolioValue += currentValue
        yVal.append(portfolioValue)
        ref += 0.005
    plt.figure('Beta Weighted')
    plt.plot(xVal, yVal)
    plt.axvline(x=SPYPrice, color='r', linestyle='--')
    plt.axhline(y=0, color='g', linestyle='-')

    plt.title('Beta Weight')
    plt.grid()
    plt.xlabel('Price')
    plt.ylabel('Expire Value')
    plt.show()

def Main():
    """
    Below is an example of how to create a Beta Weighted plot for your portfolio:
    1. Create your options contract by calling Option(Stock_Name, Long Put, Short Put, Short Call, Long Call, Option Value, # Contracts)
        Ex: If I want to sell a cover call for AMD at 30/35 for 0.87 credit, 10 contracts
        I would write it as AMD  = Option('AMD', 'na', 'na', 30, 35, .87, 10)

        If you have more than one option contracts for the same stock then simply create a new instance name:
        EX: AMD2 = Option('AMD', 27, 29, 29, 31, 1.5, 5)


    Call the Beta_weight(Option.List) method inorder to plot the Beta Weighted Portfolio.
    """
    AMD = Option('AMD', 28, 31, 32, 35, 2.28, 10)
    FXI = Option('FXI',34, 41, 41, 47, 2.38, 10)
    #VXX = Option('VXX', 'na', 'na', 35, 37, 0.31, 10)
    Beta_weight(Option.List)



Main()
