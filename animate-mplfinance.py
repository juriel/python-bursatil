import yfinance as yf
import mplfinance as mpf
import os
import matplotlib.pyplot as plt


# Configuración de yfinance para obtener datos de Apple
symbol = "GOOGL"
start_date = "2020-01-01"
end_date = "2023-08-30"
data = yf.download(symbol, start=start_date, end=end_date)

# Crear un DataFrame con el formato necesario para mplfinance
ohlc_data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

# Crear una carpeta para guardar los frames de la animación
os.makedirs('candlestick_frames-'+symbol, exist_ok=True)
start = 100
# Crear y guardar cada frame de la animación como imagen
for i in range(start,len(ohlc_data)):
    subset_data = ohlc_data.iloc[:i+1]
    if subset_data.shape[0] > 200:
        subset_data = subset_data.tail(200)
    title = f'Gráfico de velas de {symbol} ({subset_data.index[-1].date()})'
    
    mpf.plot(subset_data, type='candle', style='yahoo', title=title, savefig=f'candlestick_frames-'+symbol+f'/frame_{i:03d}.png')
    plt.close()

# Usar ffmpeg para convertir las imágenes en un video
os.system('ffmpeg -r 10 -start_number '+str(start)+' -i candlestick_frames-'+symbol+'/frame_%03d.png -vf "setpts=0.5*PTS" -c:v libx264 animated_candlestick_video-'+symbol+'.mp4')

# Eliminar los frames individuales después de crear el video
for i in range(start,len(ohlc_data)):
    frame_filename = f'candlestick_frames-'+symbol+f'/frame_{i:03d}.png'
    os.remove(frame_filename)
os.rmdir('candlestick_frames-'+symbol)
