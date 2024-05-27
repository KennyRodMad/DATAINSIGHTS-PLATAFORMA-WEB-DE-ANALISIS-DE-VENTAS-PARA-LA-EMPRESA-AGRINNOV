import streamlit as st

def show_title():
    st.markdown("<h1 style='text-align: center; margin-top: -50px;'>💲Panel de Ventas</h1>", unsafe_allow_html=True)

def show_file_uploader():
    return st.file_uploader("Subir archivo Excel", type="xlsx")

def show_success_message(message):
    st.success(message)

def show_error_message(message):
    st.error(message)

def show_filters(ciudades, clientes, generos):
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_cities = st.multiselect("Selecciona ciudad", ciudades)
    with col2:
        selected_customers = st.multiselect("Selecciona el tipo de cliente", clientes)
    with col3:
        selected_genders = st.multiselect("Selecciona el género", generos)
    
    return selected_cities, selected_customers, selected_genders

def show_stats(total_sales, average_sales, average_rating):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<h3 style='text-align: center;'>Total de ventas</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>COP$ {total_sales}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='text-align: center;'>Promedio de Ventas</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>COP$ {average_sales}</p>", unsafe_allow_html=True)

    with col3:
        st.markdown("<h3 style='text-align: center;'>Promedio de Rating</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{average_rating} {'⭐' * int(average_rating)}</p>", unsafe_allow_html=True)

def show_sales_chart(data):
    st.subheader("Ventas por hora")
    st.bar_chart(data.set_index("hour"))

def show_product_line_chart(data):
    st.subheader("Ventas por Producto en línea")
    st.bar_chart(data.set_index("Product line"))

def show_recommendations(recommendations):
    st.subheader("Recomendaciones")
    for rec in recommendations:
        st.write("- " + rec)


