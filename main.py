import streamlit as st
import pandas as pd
import mysql.connector as sql
from datetime import datetime
from sqlalchemy import create_engine 

# streamlit run D:\Dropbox\Empresa\PartyPlum\app_operaciones\reservation_form\main.py
# https://streamlit.io/
# pipreqs --encoding utf-8 "D:\Dropbox\Empresa\PartyPlum\app_operaciones\reservation_form"

st.set_page_config(layout="centered")

user     = st.secrets["user"]
password = st.secrets["password"]
host     = st.secrets["host"]
schema   = st.secrets["schema"]

@st.experimental_memo
def data_city():
    db_connection = sql.connect(user=user, password=password, host=host, database=schema)
    data          = pd.read_sql("SELECT id as id_city,ciudad FROM partyplum.city" , con=db_connection)
    return data

@st.experimental_memo
def data_plans():
    db_connection = sql.connect(user=user, password=password, host=host, database=schema)
    data          = pd.read_sql("SELECT * FROM partyplum.package WHERE available=1" , con=db_connection)
    return data

@st.experimental_memo
def data_event():
    db_connection = sql.connect(user=user, password=password, host=host, database=schema)
    data          = pd.read_sql("SELECT * FROM partyplum.events LIMIT 1" , con=db_connection)
    return data

package     = data_plans()
data_ciudad = data_city()

st.image('https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/partyplum_logosimbolo.png',width=300)
#st.markdown('<p style="color: #BA5778;text-align:center;"><strong>Formulario para reservar fecha de evento</strong><p>', unsafe_allow_html=True)
st.markdown('<p style="color: #BA5778"><strong>Formulario para reservar fecha de evento</strong><p>', unsafe_allow_html=True)
with st.form("my_form",clear_on_submit =True):
    
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input('Tu nombre y apellido',value='') 
        if cliente!='':
            cliente = cliente.title().strip()
    with col2:
        nombrefestejado = st.text_input('Nombre del festejado',value='') 
        if nombrefestejado!='':
            nombrefestejado = nombrefestejado.title().strip()
            
    col1, col2 = st.columns(2)
    with col1:
        ocacioncelebracion = st.selectbox('Ocasión de Celebración',options=['CUMPLEAÑOS','BAUTIZO','PRIMERA COMUNIÓN','GRADO','BABY SHOWER'])
    with col2:
        edadfestejado      = st.number_input('Edad festejado',min_value=0,value=0)

    col1, col2 = st.columns(2)
    with col1:
        tematica           = st.text_input('Temática',value='')
        if nombrefestejado!='':
            nombrefestejado = nombrefestejado.title().strip()
                    
    with col2:
        paquete_contratado = st.selectbox('Paquete contratado',options=[x.title() for x in package['package']])         
        
    col1, col2 = st.columns(2)
    with col1:
        ciudad             = st.selectbox('Ciudad del evento',options=data_ciudad['ciudad'].to_list())
        id_city            = data_ciudad[data_ciudad['ciudad']==ciudad]['id_city'].iloc[0]
    with col2:
        direccion          = st.text_input('Dirección del evento',value='')
        
    col1, col2 = st.columns(2)
    with col1:
        fecha              = st.date_input('Fecha de la celebracion')
    with col2:
        iniciocelebracion  = st.selectbox('Hora inicio celebración',options=["07:00 AM", "07:30 AM", "08:00 AM", "08:30 AM", "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "01:00 PM", "01:30 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM", "05:00 PM", "05:30 PM", "06:00 PM", "06:30 PM", "07:00 PM", "07:30 PM", "08:00 PM", "08:30 PM", "09:00 PM", "09:30 PM", "10:00 PM", "10:30 PM", "11:00 PM", "11:30 PM"],key=6)

    col1, col2 = st.columns(2)
    with col1:
        fecha_recogida     = st.date_input('Fecha de recogida',value=fecha)
    with col2:
        hora_recogida      = st.selectbox('Hora de recogida',options=["07:00 AM", "07:30 AM", "08:00 AM", "08:30 AM", "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "01:00 PM", "01:30 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM", "05:00 PM", "05:30 PM", "06:00 PM", "06:30 PM", "07:00 PM", "07:30 PM", "08:00 PM", "08:30 PM", "09:00 PM", "09:30 PM", "10:00 PM", "10:30 PM", "11:00 PM", "11:30 PM"],key=18)
                        
    st.write('---')
    st.write('Repostería')
    
    col1, col2 = st.columns(2)
    with col1:
        cantidadporcionesponque = st.number_input('Cantidad porciones de ponque (si aplica)',value=0)
    with col2:
        cantidadminipostres     = st.number_input('Cantidad Mini postres (si aplica)',value=0)

    st.write('---')
    st.write('Adicionales')
    
    adicionales = st.text_area('Adicionales q hayamos hablado?',value='')
    fotografo   = st.checkbox('Necesitas fotógrafo para tu fiesta?:',value=False)
    
    submitted = st.form_submit_button("Enviar")
    if submitted:
        clientdata = {
                      'date_insert':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      'city':ciudad,
                      'id_city':id_city,
                      'address':direccion,
                      'event_day':fecha,
                      'start_event':iniciocelebracion,
                      'theme':tematica.upper(),
                      'contracted_package':paquete_contratado,
                      'client':cliente.upper(),
                      'celebrated_name':nombrefestejado.upper(),
                      'celebrated_age':edadfestejado,
                      'occasion_celebration':ocacioncelebracion.upper(),
                      'date_pick_up':fecha_recogida,
                      'hour_pick_up':hora_recogida,
                      'origin':'client_form',
                      'aditional_info':[{'name':'Cantidad porciones de ponque (si aplica)' ,'value':cantidadporcionesponque},
                                        {'name':'Cantidad Mini postres (si aplica)','value':cantidadminipostres},
                                        {'name':'Adicionales q hayamos hablado?','value':adicionales},
                                        {'name':'Necesitas fotógrafo para tu fiesta?:','value':fotografo}]
                      } 
        
        dataevents = data_event()
        dataexport = pd.DataFrame([clientdata])
        dataexport.loc[0,'clientdata'] = pd.io.json.dumps(clientdata)
        for i in ['purchase_order','labour_order','transport_order','peajes_order','bakery_order','additional_order','other_expenses','pagos']:
            dataexport.loc[0,i] = pd.io.json.dumps([])
        variables  = [x for x in list(dataevents) if x in dataexport]
        dataexport = dataexport[variables]
        
        engine   = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
        dataexport.to_sql('events',engine,if_exists='append', index=False)
        
        db_connection = sql.connect(user=user, password=password, host=host, database=schema)
        lastid        = pd.read_sql("SELECT MAX(id) as id_event FROM partyplum.events" , con=db_connection)
        if lastid.empty is False:
            id_event = lastid['id_event'].iloc[0]
            dataexport['id_events'] = id_event
            
            engine   = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
            dataexport.to_sql('events_historic',engine,if_exists='append', index=False)

        st.success('Datos enviado con exito a partiplumco@gmail.com')
        