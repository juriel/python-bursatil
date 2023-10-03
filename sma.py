import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# Definir el símbolo de la acción
TICKER_SYMBOL = "NVDA" 


DESIRED_WIN = 1.04
STOP_LOSS   = 0.9


DESIRED_LOSS = 0.96
STOP_SHORT   = 1.1


def simulate_buy(price,data):
    for index, row in data.iterrows():
        if row["Low"]  < price*STOP_LOSS :
            return row["Low"]/price
        if row["High"] > price* DESIRED_WIN:
            return   DESIRED_WIN

    last_row = data.iloc[-1]
    return last_row["Close"]/price


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

days  = long_sma
sma_long_colname = 'SMA_' + str(days)
data[sma_long_colname] = data['Close'].rolling(window=days).mean()
delta_sma_long_colname = "d_"+sma_long_colname
data[delta_sma_long_colname] = ((data[sma_long_colname] - data[sma_long_colname].shift(1)) / data[sma_long_colname]) * 100

dias  = short_sma
sma_short_colname = 'SMA_' + str(dias)
delta_sma_short_colname = "d_"+sma_short_colname
data[sma_short_colname] = data['Close'].rolling(window=dias).mean()
data[delta_sma_short_colname] = ((data[sma_short_colname] - data[sma_short_colname].shift(1)) / data[sma_short_colname]) * 100
data = data.dropna()


data = data.copy()
data['Recomendacion'] = 'Esperar'  # Valor predeterminado de "Esperar"
data.loc[ (data[delta_sma_long_colname] > 0) & (data[delta_sma_short_colname] > 0), 'Recomendacion' ] = 'Compra'
data.loc[ (data[delta_sma_long_colname] < 0) & (data[delta_sma_short_colname] < 0), 'Recomendacion' ] = 'Venta'




future_window = 20
future_high =  'high_'+str(future_window) +'next'
future_low  =  'low_'+str(future_window) +'next'
col = data['High'].rolling(future_window).max().shift(-1*future_window)
data[future_high] =  col
col = data['Low'].rolling(future_window).min().shift(-1*future_window)
data[future_low]  =  col




data['Backtest'] = 'Esperar'      # Valor predeterminado de "Esperar"
data.loc[ (data[future_high] >= data["Close"]*DESIRED_WIN) & (data[future_low]  >  data["Close"]*STOP_LOSS), 'Backtest' ] = 'Compra'
data.loc[ (data[future_low]  < data["Close"]*DESIRED_LOSS)  & (data[future_high] < data["Close"]*STOP_SHORT) ,'Backtest' ] = 'Venta'

data = data.copy()
data["simulate"] = 0
i = 0
num_rows = data.shape[0]



for index, row in data.iterrows():
    #print("HELLO------------------------------",index, row)
    simulation_rows = data.tail(num_rows-i-1).head(100)
    if (row["Recomendacion"] == "Compra") and simulation_rows.shape[0] > 0:
        data.at[index,"simulate"] = simulate_buy(row["Close"], simulation_rows)
    if (row["Recomendacion"] == "Venta") and simulation_rows.shape[0] > 0:
        data.at[index,"simulate"] = simulate_sell(row["Close"], simulation_rows)        
    i  = i+1


excel_filename = "DATA/"+TICKER_SYMBOL + "_historico_precios3.xlsx"
data.to_excel(excel_filename)
print(data)


print(data)

data = data.tail(360)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data.index, data[sma_short_colname], label=sma_short_colname, linestyle='-', linewidth=1, color="blue")
ax.plot(data.index, data[sma_long_colname], label=sma_long_colname, linestyle='-', linewidth=2, color="orange")
ax.plot(data.index, data['Close'], label='Close', linestyle='-', linewidth=1, color="darkgray")




for index, row in data.iterrows():
    color = "gray"
    if row['Recomendacion'] == 'Compra':
        color = "green"
    if row['Recomendacion'] == 'Venta':        
        color = "red"    
    if color != "gray":        
        ax.plot(index, row['Close'], marker='o', markersize=4, color=color)

for index, row in data.iterrows():
    color = "gray"
    if row['simulate'] > 1 :
        color = "green"

    if 0 < row['simulate'] and row['simulate'] < 1:        
        color = "red"        
    #if row['Backtest'] == 'Venta':        
    #    color = "red"    
    if color != "gray":        
        ax.plot(index, row['Close']*1.03, marker='+', markersize=7, color=color)



ax.set_title(f'Gráfico de SMA_{short_sma}, SMA_{long_sma} y Close para {TICKER_SYMBOL}')
ax.set_xlabel('Fecha')
ax.set_ylabel('Precio')
ax.legend()

# Mostrar el gráfico
plt.grid(True)
plt.xticks(rotation=45)  # Rotar las fechas e n el eje x para que sean más legibles
plt.tight_layout()

plt.show()





