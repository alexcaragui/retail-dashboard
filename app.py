import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analytics.predictions import get_sales_prediction

API = "http://127.0.0.1:8000/api"

def get(endpoint):
    try:
        response = requests.get(f"{API}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Serverul FastAPI nu este pornit! Pornește-l cu: uvicorn backend.main:app --reload")
        st.stop()
    except Exception as e:
        st.error(f"❌ Eroare: {e}")
        st.stop()

st.set_page_config(page_title="Retail Dashboard", page_icon="📊", layout="wide")
st.title("📊 Business Analytics Dashboard")

pagina = st.sidebar.selectbox("Navigare", [
    "🏠 Dashboard Principal",
    "👥 Analiza Clientilor",
    "📦 Management Stocuri",
    "📈 Predictii Vanzari"
])

# ── DASHBOARD PRINCIPAL ──────────────────────────────────────
if pagina == "🏠 Dashboard Principal":
    st.header("Dashboard Principal")

    total_data = get("sales/total")
    total_val = total_data["total"]

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Vanzari", f"{total_val:,.2f} RON")
    col2.metric("📦 Total Comenzi", "300")
    col3.metric("👥 Total Clienti", "20")

    st.subheader("Vanzari Lunare")
    df_lunar = pd.DataFrame(get("sales/monthly"))
    fig = px.bar(df_lunar, x='luna', y='vanzari',
                 color='vanzari', color_continuous_scale='Blues',
                 labels={'luna': 'Luna', 'vanzari': 'Vanzari (RON)'})
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 Produse")
        df_top = pd.DataFrame(get("sales/top-products"))
        fig2 = px.bar(df_top, x='venit', y='produs', orientation='h',
                      color='venit', color_continuous_scale='Greens',
                      labels={'venit': 'Venit (RON)', 'produs': 'Produs'})
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("Vanzari Ultimele 30 Zile")
        df_30 = pd.DataFrame(get("sales/daily-last-30"))
        if df_30.empty:
            st.info("Nu exista date pentru ultimele 30 de zile.")
        else:
            fig3 = px.line(df_30, x='zi', y='vanzari',
                           labels={'zi': 'Data', 'vanzari': 'Vanzari (RON)'})
            fig3.update_traces(line_color='#ff6b6b')
            st.plotly_chart(fig3, use_container_width=True)

# ── ANALIZA CLIENTILOR ───────────────────────────────────────
elif pagina == "👥 Analiza Clientilor":
    st.header("Analiza Clientilor")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Clienti Noi vs Recurenti")
        df_tip = pd.DataFrame(get("customers/new-vs-returning"))
        fig = px.pie(df_tip, values='numar', names='tip',
                     color_discrete_sequence=['#636EFA', '#EF553B'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Clienti dupa Oras")
        df_oras = pd.DataFrame(get("customers/by-city"))
        fig2 = px.bar(df_oras, x='oras', y='numar_clienti',
                      color='numar_clienti', color_continuous_scale='Purples',
                      labels={'oras': 'Oras', 'numar_clienti': 'Nr Clienti'})
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🏆 Top 10 Clienti dupa Vanzari")
    df_top = pd.DataFrame(get("customers/top"))
    fig3 = px.bar(df_top, x='total_cheltuit', y='client', orientation='h',
                  color='total_cheltuit', color_continuous_scale='Oranges',
                  labels={'total_cheltuit': 'Total Cheltuit (RON)', 'client': 'Client'})
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Tabel Detaliat")
    st.dataframe(df_top, use_container_width=True)

# ── MANAGEMENT STOCURI ───────────────────────────────────────
elif pagina == "📦 Management Stocuri":
    st.header("Management Stocuri")

    df_low = pd.DataFrame(get("inventory/low-stock"))
    if not df_low.empty:
        st.error(f"⚠️ {len(df_low)} produse necesita reaprovizionare!")
        st.dataframe(df_low, use_container_width=True)
    else:
        st.success("✅ Toate produsele au stoc suficient!")

    st.subheader("Toate Produsele")
    df_all = pd.DataFrame(get("inventory/all"))
    def coloreaza(val):
        if isinstance(val, (int, float)) and val <= 20:
            return 'background-color: #ffcccc'
        return ''
    st.dataframe(df_all.style.map(coloreaza, subset=['stoc_curent']),
                 use_container_width=True)

    st.subheader("Rotatia Stocului")
    df_rot = pd.DataFrame(get("inventory/rotation"))
    fig = px.bar(df_rot, x='produs', y=['stoc_curent', 'total_vandut'],
                 barmode='group',
                 labels={'value': 'Cantitate', 'produs': 'Produs', 'variable': 'Tip'})
    st.plotly_chart(fig, use_container_width=True)

# ── PREDICTII ────────────────────────────────────────────────
elif pagina == "📈 Predictii Vanzari":
    st.header("Predictii Vanzari")
    st.info("Predictie bazata pe regresie liniara pe datele istorice.")

    df_istoric, df_pred, coef = get_sales_prediction()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_istoric['zi'], y=df_istoric['vanzari'],
        name='Vanzari Istorice', line=dict(color='#636EFA')))
    fig.add_trace(go.Scatter(
        x=df_pred['zi'], y=df_pred['vanzari_prezise'],
        name='Predictie 30 zile', line=dict(color='#EF553B', dash='dash')))
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Vanzari (RON)',
        legend=dict(x=0, y=1))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Vanzari Estimate Urmatoarele 30 Zile")
    st.dataframe(df_pred.rename(columns={
        'zi': 'Data',
        'vanzari_prezise': 'Vanzari Estimate (RON)'
    }), use_container_width=True)

    trend = "crescator 📈" if coef[0] > 0 else "descrescator 📉"
    st.metric("Trend general", trend, f"{coef[0]:.2f} RON/zi")