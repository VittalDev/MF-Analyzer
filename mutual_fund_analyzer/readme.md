📈 Mutual Fund Analytics Dashboard

A Streamlit-based Mutual Fund Analytics Dashboard that allows users to analyze Indian mutual funds using real-time NAV data and compare performance against the NIFTY 50 benchmark.

This dashboard provides:

📊 Fund vs Benchmark comparison

📈 NAV with Moving Averages

📉 Drawdown analysis

📌 Key performance metrics (CAGR, Volatility, Max Drawdown)

⏳ Custom time filtering (1M to Max)

🚀 Features
🔎 Fund Search

Dynamically loads mutual fund schemes from MFAPI

Search and select any available Indian mutual fund

⏳ Time Filters

Choose analysis period:

1 Month

6 Months

1 Year

3 Years

5 Years

Max (Full History)

📊 Performance Metrics

CAGR (Compound Annual Growth Rate)

Annualized Volatility

Maximum Drawdown

📈 Visual Analytics

Fund vs NIFTY 50 (Normalized Growth Chart)

Shows relative growth comparison

Indexed to 100 for fair comparison

NAV with Moving Averages

50-Day Moving Average

200-Day Moving Average

Drawdown Chart

Visualizes downside risk

Helps understand historical loss periods

🛠️ Tech Stack

Streamlit – Web app framework

Pandas – Data processing

NumPy – Numerical computations

Plotly – Interactive charts

Requests – API calls

yFinance – Benchmark data (NIFTY 50)

MFAPI – Mutual fund NAV data
