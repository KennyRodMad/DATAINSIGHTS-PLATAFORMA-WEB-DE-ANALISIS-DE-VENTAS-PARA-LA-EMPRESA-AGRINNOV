import pandas as pd
from model.model import filter_data, generate_recommendations, to_text
from view.view import show_filters, show_stats, show_sales_chart, show_product_line_chart, show_recommendations, show_error_message

def process_data(uploaded_file, selected_cities, selected_customers, selected_genders):
    try:
        info = pd.read_excel(
            io=uploaded_file,
            engine='openpyxl',
            sheet_name='Ventas',
            skiprows=3,
            usecols='B:R',
            nrows=1000,
        )
    except ValueError as e:
        if "Worksheet named 'Ventas' not found" in str(e):
            show_error_message("Error: El archivo Excel no contiene una hoja llamada 'Ventas'.")
        else:
            show_error_message(f"Error en el formato del archivo: {e}")
        return None, None, None, None

    info["hour"] = pd.to_datetime(info["Time"], format="%H:%M:%S").dt.hour
    
    data_filtered, ventas_por_productline, ventas_por_hora = filter_data(
        info, selected_cities, selected_customers, selected_genders
    )
    recommendations = generate_recommendations(data_filtered)

    return data_filtered, ventas_por_productline, ventas_por_hora, recommendations

def handle_filters(ciudades, clientes, generos):
    selected_cities, selected_customers, selected_genders = show_filters(ciudades, clientes, generos)
    return selected_cities, selected_customers, selected_genders
