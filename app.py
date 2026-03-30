import streamlit as st
import random
import string
import time

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

col1, col2 = st.columns(2)
col1.metric("✅ Légitimes", st.session_state.legit)
col2.metric("🚨 Fraudes", st.session_state.fraud)

if st.button("▶️ Générer 10 transactions"):
    for _ in range(10):
        tx = generate_transaction()
        tx["status"] = "🚨 Fraude" if is_fraud(tx) else "✅ Légit"
        st.session_state.transactions.insert(0, tx)
        if is_fraud(tx):
            st.session_state.fraud += 1
        else:
            st.session_state.legit += 1
    st.rerun()

if st.button("🔄 Reset"):
    st.session_state.transactions = []
    st.session_state.legit = 0
    st.session_state.fraud = 0
    st.rerun()

if st.session_state.transactions:
    st.subheader("📋 Transactions en temps réel")
    st.dataframe(st.session_state.transactions[:50])
else:
    st.info("Cliquez sur 'Générer 10 transactions' pour démarrer !")
