import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np
import yfinance as yf

st.set_page_config(page_title="MF NAV Analytics", layout="wide")

st.title("📈 Mutual Fund Analytics Dashboard")

# ----------------------------------
# Load Mutual Fund List
# ----------------------------------
@st.cache_data
def load_fund_list():
    url = "https://api.mfapi.in/mf"
    return pd.DataFrame(requests.get(url).json())

fund_df = load_fund_list()

selected_fund = st.selectbox(
    "Search Mutual Fund",
    fund_df['schemeName']
)

# ----------------------------------
# Time Filter
# ----------------------------------
time_filter = st.radio(
    "Select Time Period",
    ["1M", "6M", "1Y", "3Y", "5Y", "Max"],
    horizontal=True
)

if selected_fund:

    scheme_code = fund_df.loc[
        fund_df['schemeName'] == selected_fund,
        'schemeCode'
    ].values[0]

    nav_url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(nav_url)

    if response.status_code == 200:

        data = response.json()
        df = pd.DataFrame(data['data'])

        df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y")
        df['nav'] = df['nav'].astype(float)
        df = df.sort_values('date')

        # ----------------------------------
        # Apply Time Filter
        # ----------------------------------
        if time_filter != "Max":
            today = df['date'].max()

            if time_filter == "1M":
                df = df[df['date'] >= today - pd.DateOffset(months=1)]
            elif time_filter == "6M":
                df = df[df['date'] >= today - pd.DateOffset(months=6)]
            elif time_filter == "1Y":
                df = df[df['date'] >= today - pd.DateOffset(years=1)]
            elif time_filter == "3Y":
                df = df[df['date'] >= today - pd.DateOffset(years=3)]
            elif time_filter == "5Y":
                df = df[df['date'] >= today - pd.DateOffset(years=5)]

        df = df.reset_index(drop=True)

        # ----------------------------------
        # Moving Averages
        # ----------------------------------
        df['MA50'] = df['nav'].rolling(50).mean()
        df['MA200'] = df['nav'].rolling(200).mean()

        # ----------------------------------
        # Performance Metrics
        # ----------------------------------
        latest_nav = df['nav'].iloc[-1]
        first_nav = df['nav'].iloc[0]

        years = (df['date'].iloc[-1] - df['date'].iloc[0]).days / 365
        cagr = ((latest_nav / first_nav) ** (1 / years) - 1) * 100 if years > 0 else 0

        returns = df['nav'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) * 100

        rolling_max = df['nav'].cummax()
        drawdown = (df['nav'] - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("CAGR", f"{cagr:.2f}%")
        col2.metric("Volatility (Annualized)", f"{volatility:.2f}%")
        col3.metric("Max Drawdown", f"{max_drawdown:.2f}%")

        # ----------------------------------
        # Fetch Benchmark (NIFTY 50)
        # ----------------------------------
        benchmark = yf.download(
            "^NSEI",
            start=df['date'].min(),
            end=df['date'].max(),
            progress=False
        )

        benchmark = benchmark.reset_index()[['Date', 'Close']]
        benchmark.columns = ['date', 'benchmark']
        benchmark['date'] = pd.to_datetime(benchmark['date'])

        # ----------------------------------
        # Normalize for Comparison
        # ----------------------------------
        df['normalized_nav'] = df['nav'] / df['nav'].iloc[0] * 100
        benchmark['normalized_benchmark'] = (
            benchmark['benchmark'] / benchmark['benchmark'].iloc[0] * 100
        )

        merged = pd.merge(df, benchmark, on='date', how='inner')

        # ----------------------------------
        # Main Chart (Fund vs Benchmark)
        # ----------------------------------
        st.subheader("📊 Fund vs Benchmark (Normalized Growth)")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=merged['date'],
            y=merged['normalized_nav'],
            name='Fund'
        ))

        fig.add_trace(go.Scatter(
            x=merged['date'],
            y=merged['normalized_benchmark'],
            name='NIFTY 50'
        ))

        fig.update_layout(template="plotly_white")

        st.plotly_chart(fig, width="stretch")

        # ----------------------------------
        # NAV + Moving Average Chart
        # ----------------------------------
        st.subheader("📈 NAV with Moving Averages")

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=df['date'],
            y=df['nav'],
            name='NAV'
        ))

        fig2.add_trace(go.Scatter(
            x=df['date'],
            y=df['MA50'],
            name='50D MA'
        ))

        fig2.add_trace(go.Scatter(
            x=df['date'],
            y=df['MA200'],
            name='200D MA'
        ))

        fig2.update_layout(template="plotly_white")

        st.plotly_chart(fig2, width="stretch")

        # ----------------------------------
        # Drawdown Chart
        # ----------------------------------
        st.subheader("📉 Drawdown Chart")

        fig_dd = go.Figure()

        fig_dd.add_trace(go.Scatter(
            x=df['date'],
            y=drawdown * 100,
            fill='tozeroy',
            name="Drawdown (%)"
        ))

        fig_dd.update_layout(template="plotly_white")

        st.plotly_chart(fig_dd, width="stretch")

    else:
        st.error("NAV data not available")