import streamlit as st
import pandas as pd
import json
from confluent_kafka import Consumer


def kafka_config():
    return {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'streamlit111-group',
        'auto.offset.reset': 'earliest'
    }


def consume_message(consumer):
    msg = consumer.poll(1.0)
    if msg is None:
        return None, False
    elif msg.error():
        st.write(f"Error: {msg.error()}")
        return None, False
    else:
        return json.loads(msg.value().decode('utf-8')), True


def process_dataframe(record):
    df = pd.DataFrame(record)
    df["Densidade demográfica"] = df['populationCountry'] / df['areaCountry']
    df.rename(columns={'nameCountry': 'País', 'populationCountry': 'População', 'areaCountry': 'Área'}, inplace=True)
    return df.sort_values(by='População', ascending=False).head(10), df


def main():
    st.title("Dashboard de dados do Kafka")
    df_null = pd.DataFrame()
    st.write("Top 10 Países por Densidade Demográfica")
    chart = st.bar_chart(df_null)

    if 'msg_recived' not in st.session_state:
        st.session_state['msg_recived'] = False

    if not st.session_state['msg_recived']:
        consumer = Consumer(kafka_config())
        consumer.subscribe(['scraping'])

    while not st.session_state['msg_recived']:
        record, is_msg_received = consume_message(consumer)
        if is_msg_received:
            df_highest_population, df = process_dataframe(record)
            col1, col2 = st.columns(2)
            with col1:
                st.write("Tabela Completa")
                st.write(df)
            with col2:
                chart.bar_chart(df_highest_population, y='Densidade demográfica', x='País', width=1000, height=700)

            consumer.close()
            st.session_state['msg_recived'] = True


if __name__ == "__main__":
    main()
