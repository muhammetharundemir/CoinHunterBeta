from binance.client import Client
import numpy as np
import talib as ta
import datetime

apiKey = '' # Your Binance API key
secretKey = ''  # Your Binance secret key
#
# Cüzdan Tanımlamaları
myWalletUSDTwithoutShort = 100
myWalletCoinwithoutShort = 0
shortWalletUSDT = 100
shortWalletCoin = 100
myWalletUSDT = 100
myWalletCoin = 0
#
# Değer Sorguları
programStreamPrice = 0
programStartPrice = 0
previousPrice = 0
currentPrice = 0
normalProfit = 0
shortValue = 0
#
# İzinler
telegramPrintPermission = False
printPermission = False
whilePermission = True
startingValue = True
coinStart = True
#
# Sayaçlar
simulationCounter = 0
#
# Tanımlar
currentProcess = 'START'
#
# Diziler
arrayCoinsNames = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "HOTUSDT", "XRPUSDT", "DOGEUSDT", "SHIBUSDT", "DOTUSDT", "GTCUSDT"]
arrayDayNumber = [15, 30, 60, 90, 120, 150, 180, 360, 720]
arrayValuesEMA = [100, 200]
#
for coinsNames in arrayCoinsNames:
    for dayNumberTemp in arrayDayNumber:
        dayNumber = dayNumberTemp + 60
        try:
            #
            # İzinler
            coinStart = True
            #
            client = Client(apiKey, secretKey)
            klines2 = client.get_historical_klines("%s" % coinsNames, Client.KLINE_INTERVAL_1HOUR,
                                                   "%s hour UTC" % (dayNumber * 24))
            #
            for valuesEMA in arrayValuesEMA:
                #
                # Cüzdan Tanımlamaları- cx

                myWalletUSDTwithoutShort = 100
                myWalletCoinwithoutShort = 0
                shortWalletUSDT = 100
                shortWalletCoin = 100
                myWalletUSDT = 100
                myWalletCoin = 0
                #
                # Değer Sorguları
                programStreamPrice = 0
                programStartPrice = 0
                previousPrice = 0
                currentPrice = 0
                normalProfit = 0
                shortValue = 0
                #
                # Sayaçlar
                simulationCounter = 0
                #
                # İzinler
                startingValue = True
                whilePermission = True
                #
                while whilePermission:
                    if simulationCounter < 1 * 24 * dayNumber - 1440:  # Bir saat içinde kaç defa var * 24 * Gün Sayısı - 1440
                        #
                        close2 = [float(entry[4]) for entry in klines2[simulationCounter:(1440 + simulationCounter)]]
                        time = [float(entry[0]) for entry in klines2[simulationCounter:(1440 + simulationCounter)]]
                        #
                        if startingValue:
                            programStartPrice = close2[-1]
                            startingValue = False
                            shortValue = close2[-1]
                            startTime = datetime.datetime.fromtimestamp(time[-1] / 1000)
                        #
                        currentPrice = close2[-1]  # currentPrice = close2[-1]
                        closeArray2 = np.asarray(close2)
                        #
                        long_ema = ta.EMA(closeArray2, timeperiod=valuesEMA)
                        #
                        if long_ema[-1] < currentPrice and myWalletCoin == 0:
                            myWalletUSDT = myWalletUSDT * (2 - (currentPrice / shortValue))
                            myWalletCoin = myWalletUSDT / (currentPrice * 1.00075)
                            myWalletUSDT = 0
                            previousPrice = currentPrice
                            printPermission = True
                            currentProcess = 'BUY'
                            #
                            shortWalletUSDT = shortWalletCoin * (2 - (currentPrice / shortValue))
                            shortWalletCoin = 0
                        #
                        elif long_ema[-1] > currentPrice and myWalletUSDT == 0:
                            myWalletUSDT = currentPrice * myWalletCoin * 0.99925
                            myWalletCoin = 0
                            previousPrice = currentPrice
                            #
                            shortValue = currentPrice
                            shortWalletCoin = shortWalletUSDT
                            shortWalletUSDT = 0
                            #
                            printPermission = True
                            currentProcess = 'SELL'
                        #
                        if long_ema[-1] < currentPrice and myWalletCoinwithoutShort == 0:
                            myWalletCoinwithoutShort = myWalletUSDTwithoutShort / (currentPrice * 1.00075)
                            myWalletUSDTwithoutShort = 0
                        #
                        elif long_ema[-1] > currentPrice and myWalletUSDTwithoutShort == 0:
                            myWalletUSDTwithoutShort = currentPrice * myWalletCoinwithoutShort * 0.99925
                            myWalletCoinwithoutShort = 0
                        #
                        programStreamPrice = currentPrice
                        normalProfit = programStreamPrice / programStartPrice
                        simulationCounter += 1
                    #
                    else:
                        stopTime = datetime.datetime.fromtimestamp(time[-1] / 1000)
                        if (coinStart):
                            print('\n' +
                                  '\n-----------------------------------------------------------------------------------------------------------------------------------------' +
                                  '\n\n\n%s' % coinsNames +
                                  '     Gün Sayısı : ' + str(dayNumber - 60) +
                                  '     Açılış Değeri : ' + str(programStartPrice) +
                                  '     Kapanış Değeri : ' + str(currentPrice) +
                                  '     ( ' + str(startTime) + ' - ' + str(stopTime) + ' )' +
                                  '\n\nNormal : ' + str(round(((normalProfit * 100) - 100), 2)) +
                                  ' %')
                            #
                            print('\nBoth : ' +
                                  str(round(((myWalletCoin * currentPrice + myWalletUSDT) - 100), 2)) + ' %' +
                                  '          Buy-Sell : ' +
                                  str(round(
                                      ((myWalletCoinwithoutShort * currentPrice + myWalletUSDTwithoutShort) - 100),
                                      2)) + ' %' +
                                  '          Short : ' +
                                  str(round(((shortWalletUSDT + shortWalletCoin) - 100), 2)) + ' %' +
                                  '          EMA : ' + str(valuesEMA))
                            coinStart = False
                        else:
                            print('Both : ' +
                                  str(round(((myWalletCoin * currentPrice + myWalletUSDT) - 100), 2)) + ' %' +
                                  '          Buy-Sell : ' +
                                  str(round(
                                      ((myWalletCoinwithoutShort * currentPrice + myWalletUSDTwithoutShort) - 100),
                                      2)) + ' %' +
                                  '          Short : ' +
                                  str(round(((shortWalletUSDT + shortWalletCoin) - 100), 2)) + ' %' +
                                  '          EMA : ' + str(valuesEMA))
                        whilePermission = False

        except:
            print('\nERROR - ' + coinsNames + ' - ' + str(dayNumber) + ' DAYS')
    #
    print('\n\n\n\n\n')
