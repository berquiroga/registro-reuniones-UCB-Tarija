import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Registro de Tutorías UCB",
                   page_icon="⚙️",
                   layout="centered")

# Encabezado
st.title(body="Registro de Atención a Estudiantes")
st.subheader(body="M.Sc. Ing. Bernardo Quiroga Turdera")
st.caption(body="DCT - Ingeniería Mecatrónica - UCB Sede Tarija")
st.divider()

# Formulario de ingreso de datos
with st.form("registro_form"):
    st.write("### Por favor, ingresa tus datos:")

    nombre = st.text_input("Nombre y Apellidos del Estudiante")
    semestres = ["1ro", "2do", "3ro", "4to", "5to", "6to", "7mo", "8vo", "9no", "Proyecto de Grado"]
    semestre = st.selectbox(label="Semestre", options=semestres)
    atenciones = ["Atención regular (Mar-Jue 08:30 - 12:30)", "Tutoría de Grado", "Relatoría", "Tutoría de Prácticas Preprofesionales"]
    tipo_atencion = st.selectbox(label="Tipo de Atención", options=atenciones)

    tema = st.text_area(label="Tema Tratado o Avance de la Sesión")

    # Botón de envío
    submit_button = st.form_submit_button(label="Registra Asistencia",
                                          type="primary",
                                          )

# Lógica de guardado al presionar el botón
archivo_csv = "registro_mensual.csv"

if submit_button:
    if nombre and tema:
        # Crear el registro con la fecha y hora actual
        nuevo_registro = {
            "Fecha y Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Estudiante": nombre,
            "Semestre": semestre,
            "Tipo": tipo_atencion,
            "Tema/Avance": tema
        }

        df_nuevo = pd.DataFrame([nuevo_registro])

        # Guardar en CSV (crea el archivo si no existe, o añade la fila si existe)
        if not os.path.isfile(archivo_csv):
            df_nuevo.to_csv(archivo_csv, index=False)
        else:
            df_nuevo.to_csv(archivo_csv, mode="a", header=False, index=False)

        st.success(f"¡Registro guardado exitosamente, {nombre}! Puedes retirarte.")
    else:
        st.error("Por favor, completa tu nombre y el tema tratado antes de enviar.")

# Zona Exclusiva del Docente (Descarga del consolidado)
st.divider()
with st.expander("🔒 Zona del Docente (Descargar Reporte)"):
    st.write("Área restringida. Ingresa la contraseña para descargar el reporte.")
    
    # Campo de contraseña que oculta los caracteres
    password = st.text_input("Contraseña de acceso", type="password")
    
    # Aquí defines tu contraseña (puedes cambiar "MecaUCB2026" por la que desees)
    if password == "UCB.Meca2026":
        if os.path.isfile(archivo_csv):
            with open(archivo_csv, "rb") as f:
                st.download_button(
                    label="📥 Descargar Reporte en Excel (CSV)",
                    data=f,
                    file_name=f"Reporte_Tutorias_{datetime.now().strftime('%Y_%m')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("Aún no hay registros este mes.")
    elif password != "":
        st.error("Contraseña incorrecta. Acceso denegado.")