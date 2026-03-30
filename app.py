import streamlit as st
import random
import string
import time
import pandas as pd

st.title("🔍 Kafka Fraud Detector - Dashboard")

def random_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def generate_transaction():
    return {
        "source": random_id(),
        "target": random_id(),
        "amount": round(random.uniform(10, 1000), 2),
        "currency": "EUR"
    }

def is_fraud(tx):
    return tx["amount"] >= 900

if "transactions" not in st.session_state:
    st.session_state.transactions = []
if "legit" not in st.session_state:
    st.session_state.legit = 0
if "fraud" not in st.session_state:
    st.session_state.fraud = 0
if "running" not in st.session_state:
    st.session_state.running = False

col1, col2, col3 = st.columns(3)
col1.metric("✅ Légitimes", st.session_state.legit)
col2.metric("🚨 Fraudes", st.session_state.fraud)
col3.metric("📊 Total", len(st.session_state.transactions))

colA, colB = st.columns(2)
if colA.button("▶️ Démarrer" if not st.session_state.running else "⏸️ Pause"):
    st.session_state.running = not st.session_state.running

if colB.button("🔄 Reset"):
    st.session_state.transactions = []
    st.session_state.legit = 0
    st.session_state.fraud = 0
    st.session_state.running = False
    st.rerun()

chart_placeholder = st.empty()
table_placeholder = st.empty()

if st.session_state.running:
    for _ in range(5):
        tx = generate_transaction()
        tx["status"] = "🚨 Fraude" if is_fraud(tx) else "✅ Légit"
        st.session_state.transactions.insert(0, tx)
        if is_fraud(tx):
            st.session_state.fraud += 1
        else:
            st.session_state.legit += 1

if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)

    st.subheader("📈 Montants en temps réel")
    chart_data = df[["amount", "status"]].head(50).copy()
    chart_data["color"] = chart_data["status"].apply(
        lambda x: 1 if "Fraude" in x else 0
    )
    chart_placeholder.line_chart(df["amount"].head(50))

    st.subheader("📋 Transactions")
    table_placeholder.dataframe(df.head(50))

if st.session_state.running:
    time.sleep(1)
    st.rerun()
