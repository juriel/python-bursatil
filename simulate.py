import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt


# Definir el símbolo de la acción
TICKER_SYMBOL = "AAPL" 


DESIRED_WIN = 0.06
STOP_LOSS   = 0.10
TRAILING_STOP_LOSS = 0.06 


DESIRED_LOSS = 0.96
STOP_SHORT   = 1.1


def simulate_buy(price,data):
    print("------------------SIMULATE = ",price)

    print("Price",price)
    print("next days",data)
    stop_loss_price = price * (1.0 - STOP_LOSS)
    take_profit = price * (1.0 + DESIRED_WIN)
    status = "LOSER"
    for index, row in data.iterrows():
        if status == "LOSER":
            if row["Low"] <= stop_loss_price:
                print("STOP LOSS ",stop_loss_price," ", row["Low"] /price)
                return row["Low"] /price
            elif  row["High"] >= take_profit:
                print("WINNER ",take_profit,"  ",row["Close"]/price)
                status = "WINNER"
                trailing_stop_loss = row["Close"] * (1.0-TRAILING_STOP_LOSS)
        elif status == "WINNER":
            if row["Low"] <= trailing_stop_loss:
                print("TRAILING STOP LOSS ",trailing_stop_loss, " ",row["Close"]/price)
                return row["Low"] /price
            if trailing_stop_loss <  row["Close"] * (1.0-TRAILING_STOP_LOSS):
                trailing_stop_loss = row["Close"] * (1.0-TRAILING_STOP_LOSS)

        print(index, "Price ",row["Close"],(((row["Close"]/price) -1.0)*100.0), "%")  
        
    last_row = data.iloc[-1]
    print("EXIT BY TIME ", last_row["Close"])
    return last_row["Close"] /price



   


def simulate_sell(price,data):
    for index, row in data.iterrows():
        if row["High"]  > price*STOP_SHORT :
            return price/row["High"]
        if row["Low"] <  price* DESIRED_LOSS:
            return   1.0/DESIRED_LOSS
    try:
        last_row = data.iloc[-1]
        return last_row["Close"]/price
    except:
        return -1


# Calcular las fechas hace dos años y la fecha actual
end_date   = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=3650)).strftime('%Y-%m-%d')  

#En la variable va a quedar el histórico
data = yf.download(TICKER_SYMBOL, start=start_date)

long_sma = 40
short_sma = 10

#Calculamos SMA corto
dias  = short_sma
sma_short_colname = 'SMA_' + str(dias)
delta_sma_short_colname = "d_"+sma_short_colname
data[sma_short_colname] = data['Close'].rolling(window=dias).mean()
data[delta_sma_short_colname] = ((data[sma_short_colname] - data[sma_short_colname].shift(1)) / data[sma_short_colname]) * 100

#Calculamos SMA largo
days  = long_sma
sma_long_colname = 'SMA_' + str(days)
data[sma_long_colname] = data['Close'].rolling(window=days).mean()
delta_sma_long_colname = "d_"+sma_long_colname
data[delta_sma_long_colname] = ((data[sma_long_colname] - data[sma_long_colname].shift(1)) / data[sma_long_colname]) * 100


data = data.dropna()


excel_filename = "DATA/"+TICKER_SYMBOL + "_historico_precios3.xlsx"
data.to_excel(excel_filename)
print(data)

num_rows = data.shape[0]
count_win = 0 
count_loss = 0 
sum_profit = 0
iterations = 1000
count =0 
for i in range(0,iterations):
    random_index = random.randint(0, num_rows -10)
    #print("random_index",random_index)
    selected_row = data.iloc[random_index]

    #print("selected_rows",selected_row)

    is_time_to_buy = selected_row["d_SMA_40"]  > 0.5 and selected_row["d_SMA_10"] > 0.1
    print("is_time_to_buy",is_time_to_buy)

    if is_time_to_buy :
        count = count+1
        tail_size = num_rows - random_index -1
        subset = data.tail(tail_size)
        profit  = simulate_buy(selected_row["Close"],subset.head(100))
        sum_profit = sum_profit+profit
        print(profit)
        if profit > 1.0:
            count_win =  count_win +1
        else:
            count_loss =  count_loss +1


print("count win",count_win, "count loss",count_loss )
print("RATIO ",(count_win/count_loss))
print("PROFIT AVG",(sum_profit/count))