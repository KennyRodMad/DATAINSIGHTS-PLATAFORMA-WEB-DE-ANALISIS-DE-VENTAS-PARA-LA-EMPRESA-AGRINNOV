import pandas as pd

# Función de filtrado
def filter_data(info, ciudades, clientes, generos):
    data_filtered = info[
        info['City'].isin(ciudades) &
        info["Customer_type"].isin(clientes) &
        info["Gender"].isin(generos)
    ]
    
    ventas_por_productline = (
        data_filtered[["Product line", "Total"]]
        .groupby(by="Product line")
        .sum()
        .sort_values(by="Total", ascending=True)
        .reset_index()
    )
    
    ventas_por_hora = (
        data_filtered[["hour", "Total"]]
        .groupby(by="hour")
        .sum()
        .reset_index()
    )
    
    return data_filtered, ventas_por_productline, ventas_por_hora

# Función para generar recomendaciones
def generate_recommendations(data_filtered):
    recommendations = []
    
    ventas_por_productline = (
        data_filtered[["Product line", "Total"]]
        .groupby(by="Product line")
        .sum()
        .sort_values(by="Total", ascending=False)
        .reset_index()
    )
    
    if not ventas_por_productline.empty:
        top_product = ventas_por_productline.iloc[0]["Product line"]
        bottom_product = ventas_por_productline.iloc[-1]["Product line"]
        
        recommendations.append(f"El producto más vendido es {top_product}. Considere aumentar su stock o realizar promociones especiales para mantener el interés.")
        recommendations.append(f"El producto menos vendido es {bottom_product}. Evalúe su demanda, realice encuestas a clientes y considere ofertas o promociones específicas para este producto.")
    
    ventas_por_hora = (
        data_filtered.groupby('hour')['Total']
        .sum()
        .reset_index()
    )
    
    if not ventas_por_hora.empty:
        peak_hour = ventas_por_hora.loc[ventas_por_hora['Total'].idxmax()]['hour']
        off_peak_hour = ventas_por_hora.loc[ventas_por_hora['Total'].idxmin()]['hour']
        
        recommendations.append(f"La hora pico de ventas es a las {peak_hour}:00. Considere aumentar el personal, ofrecer descuentos flash o promociones especiales durante esta hora.")
        recommendations.append(f"La hora con menos ventas es a las {off_peak_hour}:00. Evalúe estrategias como promociones nocturnas, envíos gratuitos o eventos especiales para atraer clientes durante esta hora.")
    
    ventas_por_ciudad = (
        data_filtered.groupby('City')['Total']
        .sum()
        .reset_index()
        .sort_values(by='Total', ascending=False)
    )
    
    if not ventas_por_ciudad.empty:
        top_city = ventas_por_ciudad.iloc[0]["City"]
        bottom_city = ventas_por_ciudad.iloc[-1]["City"]
        
        recommendations.append(f"La ciudad con más ventas es {top_city}. Considere mantener o incrementar las actividades de marketing, realizar eventos locales y fortalecer la relación con los clientes en esta ciudad.")
        recommendations.append(f"La ciudad con menos ventas es {bottom_city}. Evalúe estrategias específicas como estudios de mercado para entender las necesidades locales, promociones especiales y colaboraciones con negocios locales para aumentar la presencia en esta ciudad.")
    
    return recommendations

# Función para formatear números
def to_text(value):
    return "{:,}".format(int(value))

