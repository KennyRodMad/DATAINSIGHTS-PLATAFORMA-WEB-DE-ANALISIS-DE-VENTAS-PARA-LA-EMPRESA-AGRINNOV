import streamlit as st
import pandas as pd
from controller.controller import process_data, handle_filters, to_text
from view.view import show_title, show_file_uploader, show_success_message, show_error_message, show_stats, show_sales_chart, show_product_line_chart, show_recommendations

def main():
    st.set_page_config(page_title="DataInsights - Agrinnov")  
    show_title()

    uploaded_file = show_file_uploader()

    if uploaded_file:
        try:
            info = pd.read_excel(
                io=uploaded_file,
                engine='openpyxl',
                sheet_name='Ventas',
                skiprows=3,
                usecols='B:R',
                nrows=1000,
            )
            info["hour"] = pd.to_datetime(info["Time"], format="%H:%M:%S").dt.hour
        except ValueError as e:
            if "Worksheet named 'Ventas' not found" in str(e):
                show_error_message("El archivo excel no contiene una hoja llamada 'Ventas' o no cumple con el formato de la empresa.")
            else:
                show_error_message(f"Error en el formato del archivo: {e}")
            return  # Detener la ejecución si hay un error

        ciudades = list(info['City'].unique())
        clientes = list(info['Customer_type'].unique())
        generos = list(info['Gender'].unique())

        show_success_message("Archivo cargado exitosamente. Ahora puede aplicar filtros.")
        
        selected_cities, selected_customers, selected_genders = handle_filters(ciudades, clientes, generos)

        if selected_cities and selected_customers and selected_genders:
            data_filtered, ventas_por_productline, ventas_por_hora, recommendations = process_data(
                uploaded_file, selected_cities, selected_customers, selected_genders
            )
            
            if data_filtered is not None:
                total_sales = to_text(data_filtered['Total'].sum())
                average_sales = to_text(data_filtered['Total'].mean())
                average_rating = round(data_filtered['Rating'].mean(), 1) if not data_filtered['Rating'].isnull().all() else 0

                show_stats(total_sales, average_sales, average_rating)
                show_sales_chart(ventas_por_hora)
                show_product_line_chart(ventas_por_productline)
                show_recommendations(recommendations)
            else:
                show_error_message("Error al procesar los datos. Por favor, verifica el archivo y los filtros seleccionados.")
        else:
            show_error_message("Por favor, selecciona al menos una opción en cada filtro.")
    
if __name__ == "__main__":
    main()
