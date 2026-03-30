import streamlit as st
import json
from kafka import KafkaConsumer
import os

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', 'localhost:9092')
LEGIT_TOPIC = 'streaming.transactions.legit'
FRAUD_TOPIC = 'streaming.transactions.fraud'

st.title("🔍 Kafka Fraud Detector - Dashboard")

col1, col2 = st.columns(2)
legit_count = col1.empty()
fraud_count = col2.empty()

st.subheader("📋 Transactions en temps réel")
table = st.empty()

transactions = []
legit = 0
fraud = 0

consumer = KafkaConsumer(
    LEGIT_TOPIC,
    FRAUD_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    value_deserializer=lambda v: json.loads(v),
    auto_offset_reset='latest'
)

for message in consumer:
    topic = message.topic
    tx = message.value
    tx['status'] = '✅ Légit' if topic == LEGIT_TOPIC else '🚨 Fraude'

    if topic == LEGIT_TOPIC:
        legit += 1
    else:
        fraud += 1

    transactions.insert(0, tx)
    transactions = transactions[:50]  # garder les 50 dernières

    legit_count.metric("✅ Légitimes", legit)
    fraud_count.metric("🚨 Fraudes", fraud)
    table.dataframe(transactions)
