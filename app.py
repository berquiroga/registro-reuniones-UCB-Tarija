import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de la página
st.set_page_config(page_title="Registro de Tutorías UCB", page_icon="⚙️", layout="centered")

# 2. Encabezado personalizado
st.title("Registro de Atención a Estudiantes")
st.subheader("M.Sc. Ing. Bernardo Quiroga Turdera")
st.caption("Departamento de Ingeniería Mecatrónica - UCB Sede Tarija")
st.divider()

# 3. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Formulario de Ingreso de Datos
with st.form("registro_form"):
    st.write("### Por favor, ingresa tus datos:")
    
    nombre = st.text_input("Nombre y Apellido del Estudiante")
    semestre = st.selectbox("Semestre", ["1ro", "2do", "3ro", "4to", "5to", "6to", "7mo", "8vo", "9no", "Proyecto de Grado"])
    
    tipo_atencion = st.selectbox("Tipo de Atención", [
        "Atención regular (Mar-Jue 08:30 - 12:30)",
        "Tutoría de Grado",
        "Relatoría",
        "Tutoría de Pasantía"
    ])
    
    tema = st.text_area("Tema Tratado o Avance de la Sesión")
    
    submit_button = st.form_submit_button(label="Registrar Asistencia", type="primary")

# 5. Lógica de guardado en Google Sheets
if submit_button:
    if nombre and tema:
        # Hora de Bolivia (UTC-4)
        zona_horaria_bo = timezone(timedelta(hours=-4))
        hora_registro = datetime.now(zona_horaria_bo).strftime("%Y-%m-%d %H:%M:%S")
        
        # Crear el nuevo registro
        nuevo_registro = pd.DataFrame([{
            "Fecha y Hora": hora_registro,
            "Estudiante": nombre,
            "Semestre": semestre,
            "Tipo": tipo_atencion,
            "Tema/Avance": tema
        }])
        
        try:
            # Leer datos existentes (ignora el caché con ttl=0)
            df_existente = conn.read(usecols=[0, 1, 2, 3, 4], ttl=0)
            # Limpiar filas vacías que Google Sheets a veces genera
            df_existente = df_existente.dropna(how="all") 
            # Combinar lo viejo con lo nuevo
            df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
        except Exception:
            # Si la hoja está totalmente vacía o es la primera vez
            df_actualizado = nuevo_registro
            
        # Actualizar la hoja de cálculo en la nube
        conn.update(data=df_actualizado)
        st.success(f"¡Registro guardado exitosamente, {nombre}! Puedes retirarte.")
    else:
        st.error("Por favor, completa tu nombre y el tema tratado antes de enviar.")

# 6. Zona Exclusiva del Docente (Descarga del consolidado)
st.divider()
with st.expander("🔒 Zona del Docente (Descargar Reporte)"):
    st.write("Área restringida. Ingresa la contraseña para descargar el reporte.")
    password = st.text_input("Contraseña de acceso", type="password")
    
    if password == "UCB.Meca2026":
        try:
            # Traer los datos limpios desde Google Sheets
            df_descarga = conn.read(usecols=[0, 1, 2, 3, 4], ttl=0).dropna(how="all")
            csv = df_descarga.to_csv(index=False).encode('utf-8')
            
            zona_horaria_bo = timezone(timedelta(hours=-4))
            mes_actual = datetime.now(zona_horaria_bo).strftime('%Y_%m')
            
            st.download_button(
                label="📥 Descargar Reporte en Excel (CSV)",
                data=csv,
                file_name=f"Reporte_Tutorias_{mes_actual}.csv",
                mime="text/csv"
            )
            st.info("💡 Tip: Los datos ya están respaldados en tu cuenta de Google Drive.")
        except Exception as e:
            st.warning("Aún no hay registros o revisa la conexión a Google Sheets.")
    elif password != "":
        st.error("Contraseña incorrecta. Acceso denegado.")