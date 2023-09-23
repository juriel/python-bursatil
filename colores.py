import pandas as pd
import matplotlib.pyplot as plt

# Crear un DataFrame de ejemplo (reemplaza esto con tu DataFrame real)
data = {
    'SMA_5': [100, 110, 120, 130, 140],
    'SMA_30': [90, 100, 110, 120, 130],
    'Close': [110, 105, 125, 135, 120],
    'Recomendacion': ['Compra', 'Venta', 'Compra', 'Esperar', 'Compra']
}

df = pd.DataFrame(data)

# Crear un diccionario para mapear colores a recomendaciones
colors = {'Compra': 'green', 'Venta': 'red', 'Esperar': 'gray'}

# Crear una figura y ejes para el gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar las columnas SMA_5 y SMA_30
ax.plot(df.index, df['SMA_5'], label='SMA_5', linestyle='-', linewidth=2)
ax.plot(df.index, df['SMA_30'], label='SMA_30', linestyle='-', linewidth=2)

# Colorear el gráfico de la columna Close según la recomendación
for i, row in df.iterrows():
    color = colors.get(row['Recomendacion'], 'gray')
    ax.plot(i, row['Close'], marker='o', color=color, markersize=8)

# Configurar título y etiquetas de los ejes
ax.set_title('Gráfico de SMA_5, SMA_30 y Close con Colores de Recomendación')
ax.set_xlabel('Días')
ax.set_ylabel('Valor')
ax.legend()

# Mostrar el gráfico
plt.grid(True)
plt.tight_layout()
plt.show()
