import streamlit as st
import pandas as pd
import json
from confluent_kafka import Consumer

st.title("Dashboard de dados do Kafka")

df_null = pd.DataFrame()
chart = st.bar_chart(df_null)

if 'msg_recived' not in st.session_state:
    st.session_state['msg_recived'] = False

if not st.session_state['msg_recived']:
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'streamlit252-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe(['scraping'])

while not st.session_state['msg_recived']:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    elif msg.error():
        st.write(f"Error: {msg.error()}")
        continue
    else:
        record = json.loads(msg.value().decode('utf-8'))
        df = pd.DataFrame(record)
        df_highest_population = df.sort_values(by='populationCountry', ascending=False).head(10)
        df_highest_population["Densidade demográfica"] = df_highest_population['populationCountry'] / \
                                                         df_highest_population['areaCountry']
        df_highest_population.rename(
            columns={'nameCountry': 'País', 'populationCountry': 'População', 'areaCountry': 'Área'}, inplace=True)
        #menu = st.selectbox("Escolha uma visualização:", ["Tabela Completa", "Top 10 Países por População"])
        col1, col2 = st.columns(2)
        with col1:
            print("Tabela Completa")
            st.write(df)
        with col2:
            print("Top 10 Países por População")
            chart.bar_chart(df_highest_population, y='Densidade demográfica', x='País', width=1000, height=700)
        consumer.close()
        st.session_state['msg_recived'] = True
    break