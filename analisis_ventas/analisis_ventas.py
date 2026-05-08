"""
Análisis exploratorio de ventas a partir de un CSV sintético.

-------------------------------------------------------------------------------
PROPÓSITO
-------------------------------------------------------------------------------
Este script lee un archivo de ventas con columnas fecha, producto, cantidad y
precio; calcula ingresos y agregaciones por mes y por producto; imprime un
resumen en consola y guarda dos gráficas PNG en el directorio de trabajo.

-------------------------------------------------------------------------------
ENTRADAS Y SALIDAS
-------------------------------------------------------------------------------
Entrada principal:
    ventas_sinteticas.csv  — debe existir junto al script o en la ruta actual;
                             columna 'fecha' parseable como fecha.

Salidas:
    Consola: conteos, tipos, nulos, rango temporal, totales mensuales,
             rankings de productos.
    ventas_mensuales.png — barras de ingresos por mes.
    top5_productos.png   — barras horizontales del top 5 por ingreso.

-------------------------------------------------------------------------------
DEPENDENCIAS
-------------------------------------------------------------------------------
pandas, matplotlib, seaborn (instalar con pip según el requirements del
proyecto). La ejecución interactiva abre ventanas con plt.show().
-------------------------------------------------------------------------------
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# CONFIGURACIÓN VISUAL (matplotlib / seaborn)
# =============================================================================
# Se unifica el estilo para que barras, rejillas y tipografía se vean
# coherentes en ambas figuras. figure.figsize por defecto reduce trabajo
# repetido en cada plt.figure, aunque algunos bloques vuelven a fijar tamaño.
# =============================================================================
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


# =============================================================================
# CARGA DE DATOS Y VALIDACIÓN INICIAL
# =============================================================================
# read_csv con parse_dates convierte 'fecha' a datetime64, necesario para
# agrupar por periodo mensual (.dt.to_period). El bloque print siguiente no
# solo informa al usuario: sirve como comprobación rápida de integridad
# (dimensiones, dtypes, nulos, rango temporal) antes de derivar columnas.
# =============================================================================
df = pd.read_csv('ventas_sinteticas.csv', parse_dates=['fecha'])

print("="*50)
print("📋 RESUMEN DE DATOS CARGADOS")
print("="*50)
print(f"Total de registros: {len(df)}")
print(f"\nPrimeras filas:\n{df.head()}")
print(f"\nTipos de datos:\n{df.dtypes}")
print(f"\nValores nulos:\n{df.isnull().sum()}")
print(f"\nRango de fechas: {df['fecha'].min()} a {df['fecha'].max()}")


# =============================================================================
# VARIABLES DERIVADAS Y SERIE TEMPORAL MENSUAL
# =============================================================================
# 'ingreso' = cantidad * precio por línea de venta (base para todo el análisis
# monetario). 'año_mes' es un Period[M] que permite groupby mensual sin
# redondear manualmente fechas. ventas_mensuales suma ingresos por ese periodo
# y ordena cronológicamente para series coherentes en texto y gráfico.
# =============================================================================
df['ingreso'] = df['cantidad'] * df['precio']

df['año_mes'] = df['fecha'].dt.to_period('M')

ventas_mensuales = df.groupby('año_mes')['ingreso'].sum().sort_index()

print("\n" + "="*50)
print("💰 VENTAS TOTALES POR MES")
print("="*50)
for mes, venta in ventas_mensuales.items():
    print(f"{mes}: €{venta:,.2f}")


# =============================================================================
# AGREGACIÓN POR PRODUCTO Y RANKINGS
# =============================================================================
# groupby('producto').agg resume unidades e ingresos totales por SKU/nombre.
# nlargest extrae el top 5 para cantidad e ingreso (ingreso suele ser la métrica
# de negocio principal). idxmax sobre las series agregadas identifica el
# producto líder absoluto en cada métrica (no solo entre el top 5 impreso).
# =============================================================================
analisis_productos = df.groupby('producto').agg({
    'cantidad': 'sum',
    'ingreso': 'sum'
}).round(2)

top_cantidad = analisis_productos.nlargest(5, 'cantidad')
top_ingresos = analisis_productos.nlargest(5, 'ingreso')

producto_mas_vendido = analisis_productos['cantidad'].idxmax()
producto_mayor_ingreso = analisis_productos['ingreso'].idxmax()

print("\n" + "="*50)
print("🏆 ANÁLISIS DE PRODUCTOS")
print("="*50)
print(f"\n✅ Producto MÁS VENDIDO (unidades):")
print(f"   {producto_mas_vendido}: {analisis_productos.loc[producto_mas_vendido, 'cantidad']:.0f} unidades")

print(f"\n💎 Producto con MAYORES INGRESOS:")
print(f"   {producto_mayor_ingreso}: €{analisis_productos.loc[producto_mayor_ingreso, 'ingreso']:,.2f}")

print(f"\n📊 TOP 5 POR INGRESOS:")
print(top_ingresos)


# =============================================================================
# FIGURA 1 — EVOLUCIÓN DE INGRESOS POR MES (barras verticales)
# =============================================================================
# El índice Period se convierte a string para etiquetas del eje X legibles.
# plot(kind='bar') sobre la Serie evita crear DataFrames auxiliares. Los textos
# sobre cada barra muestran el importe aproximado; tight_layout y bbox_inches
# mejoran el guardado a alta resolución (dpi=300) para informes.
# =============================================================================
plt.figure(figsize=(12, 6))

ventas_plot = ventas_mensuales.copy()
ventas_plot.index = ventas_plot.index.astype(str)

ax = ventas_plot.plot(kind='bar', color='steelblue', edgecolor='black')

plt.title('📈 Evolución de Ventas Mensuales', fontsize=16, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Ingresos (€)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

for i, v in enumerate(ventas_plot.values):
    ax.text(i, v, f'€{v:,.0f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('ventas_mensuales.png', dpi=300, bbox_inches='tight')
plt.show()


# =============================================================================
# FIGURA 2 — TOP 5 PRODUCTOS POR INGRESO (barras horizontales)
# =============================================================================
# barh facilita leer nombres largos de producto. La paleta viridis diferencia
# las cinco barras; las etiquetas al final del segmento muestran el importe.
# Misma política de exportación PNG que la figura anterior.
# =============================================================================
plt.figure(figsize=(12, 6))

colors = sns.color_palette("viridis", 5)
ax = top_ingresos['ingreso'].plot(kind='barh', color=colors, edgecolor='black')

plt.title('🏆 Top 5 Productos por Ingresos', fontsize=16, fontweight='bold')
plt.xlabel('Ingresos (€)', fontsize=12)
plt.ylabel('Producto', fontsize=12)
plt.grid(axis='x', alpha=0.3)

for i, v in enumerate(top_ingresos['ingreso'].values):
    ax.text(v, i, f' €{v:,.0f}', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('top5_productos.png', dpi=300, bbox_inches='tight')
plt.show()




