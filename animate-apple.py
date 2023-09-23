import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Configuración de yfinance para obtener datos de Apple
symbol = "PFGRUPSURA.CL"
start_date = "2022-01-01"
end_date = "2023-08-31"
data = yf.download(symbol, start=start_date, end=end_date)

# Crear función para animación
def animate(i):
    plt.clf()  # Limpiar el plot anterior
    
    # Seleccionar datos para el frame actual
    subset_data = data.iloc[:i+1+100]
    
    # Crear gráfica de precios
    plt.plot(subset_data.index, subset_data['Close'], label='Precio de cierre')
    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.title('Precio de '+symbol)
    plt.legend()
    
    # Guardar la imagen actual
    plt.savefig('temp_image.png')

# Crear animación
ani = FuncAnimation(plt.gcf(), animate, frames=len(data)-100, repeat=False)

# Guardar imágenes individuales en una carpeta temporal
os.makedirs('temp_frames-'+symbol, exist_ok=True)
ani.save("temp_frames-"+symbol+"/animation.gif", writer='pillow')

# Limpieza
plt.close()