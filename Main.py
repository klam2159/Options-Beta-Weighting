from Options import *
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

def test():
    AMD1 = Option('AMD', 'na', 'na', 24, 24.5, 0.41)
    AMD2 = Option('AMD', 26, 27, 28, 29, 0.78)
    APPL = Option('AMD', 26, 28, 28, 29, 1.26)
    plot('AMD')
    plt.show()




test()