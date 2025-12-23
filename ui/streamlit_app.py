import streamlit as st
import tempfile
from application.use_cases import obtener_sugerencias
from infrastructure.pdf_generator import generar_pdf
from domain.constants import min_value, defult_value

def main():
    st.set_page_config(
        page_title="Contador de Procesos",
        page_icon="📄"
    )
    
    st.title("📄 Generador de Registro de Procesos")

    inicio = st.number_input("Número inicial", min_value=min_value, value=defult_value)

    sugerencias = obtener_sugerencias(inicio)
    opcion = st.selectbox("Sugerencia automática", list(sugerencias.keys()))
    fin_sugerido = sugerencias[opcion]

    fin_manual = st.number_input(
        "Número final",
        min_value=inicio,
        value=fin_sugerido
    )

    usar_manual = st.checkbox("Usar valor manual")
    fin = fin_manual if usar_manual else fin_sugerido

    if st.button("Generar PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            generar_pdf(inicio, fin, tmp.name)

            with open(tmp.name, "rb") as f:
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=f,
                    file_name="registro_procesos.pdf",
                    mime="application/pdf"
                )
