import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re

st.title("Data-Driven Stock Analysis: Visualizing Market Trends")

def load_path(path, path2):
    rename_map = {
        'bhartiartl.csv': 'AIRTEL.csv',
        'ADANIENT.csv': 'ADANIGREEN.csv',
        'TATACONSUM.csv':'TATACONSUMER.csv'
    }

    for old_name, new_name in rename_map.items():
        old_path = os.path.join(path, old_name)
        new_path = os.path.join(path, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)


    volatile = {}
    cum_return = {}
    data = {}
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            a = pd.read_csv(os.path.join(path, filename), parse_dates=['date'])
            a.sort_values(by='date', inplace=True)
            symbol = filename.replace('.csv', '')
            data[symbol] = a
            a['daily_returns'] = a['close'].pct_change().fillna(0)
            a.to_csv(os.path.join(path2, filename), index=False)
            volatility = a.daily_returns.std()
            f_name = os.path.splitext(filename)[0]
            volatile[f_name] = volatility
            start_price = a['close'].iloc[0]
            end_price = a['close'].iloc[-1]
            cumulative_return = (end_price - start_price) / start_price
            cum_return[f_name] = cumulative_return
    return cum_return, volatile, data

cum_return, volatile, stock_data = load_path(
    path=r'C:\Users\Test\Downloads\Guvi project 2\file_sector',
    path2=r'C:\Users\Test\Downloads\Guvi project 2\Final data files1'
)

# Create DataFrame of cumulative return
cum_df = pd.DataFrame(list(cum_return.items()), columns=['Ticker', 'CumulativeReturn'])
cum_df.sort_values(by='CumulativeReturn', ascending=False, inplace=True)
cum_df.to_csv(r"C:\Users\Test\Downloads\Guvi project 2\cumul_return.csv", index=False)

# Create DataFrame of volatilities
final_volatilty = pd.DataFrame(list(volatile.items()), columns=['Ticker', 'Volatility'])
final_volatilty.to_csv(r"C:\Users\Test\Downloads\Guvi project 2\volatility.csv", index=False)

# Top 10 most volatile
top10 = final_volatilty.sort_values(by='Volatility', ascending=False).head(10)
top10.to_csv(r"C:\Users\Test\Downloads\Guvi project 2\top10_volatile.csv", index=False)

# === Sidebar Filters ===
st.sidebar.header("⚙️ Settings")
selected_stock = st.sidebar.selectbox("Choose Stock", list(stock_data.keys()))
selected_df = stock_data[selected_stock]

# === 1. Daily Returns & Volatility ===
st.subheader("📊 Daily Returns & Volatility")

selected_df["Daily Return"] = selected_df["close"].pct_change()
volatility = selected_df["Daily Return"].std()

st.metric("Volatility", f"{volatility:.2%}")

fig, ax = plt.subplots(figsize=(10, 3))
ax.bar(selected_df.date, selected_df["Daily Return"])
ax.set_title("Daily Return")
ax.set_xlabel("Date")
ax.set_ylabel("Return")
plt.xticks(rotation=45)
st.pyplot(fig)

# === 2. Cumulative Return ===
st.subheader("📈 Cumulative Return")

selected_df["Cumulative Return"] = (1 + selected_df["Daily Return"]).cumprod()

fig2, ax2 = plt.subplots()
selected_df.plot(x="date", y="Cumulative Return", ax=ax2, title="Cumulative Return Over Time")
ax2.set_xlabel("Date")
ax2.set_ylabel("Cumulative Return")
plt.xticks(rotation=45)
st.pyplot(fig2)

# === 3. Sector-Wise Performance ===
st.subheader("🏢 Sector-wise Yearly Return")

# Load and clean sector data
sector = pd.read_csv(r"C:\Users\Test\Downloads\Guvi project 2\Sector_data.csv")
sector['Ticker'] = sector['Symbol'].str.split(':').str[-1].str.strip().str.upper()

# Manually append missing ticker-sector pairs
manual_sectors = [{'Ticker': 'BRITANNIA', 'sector': 'FMCG'}]

manual_sector_df = pd.DataFrame(manual_sectors)
sector_df = pd.concat([sector[['Ticker', 'sector']], manual_sector_df], ignore_index=True)

# Calculate yearly return per stock
stock_returns = []
for ticker, df in stock_data.items():
    df["Return"] = df["close"].pct_change()
    yearly_return = (1 + df["Return"]).prod() - 1
    stock_returns.append({"Ticker": ticker, "Yearly Return": yearly_return})

returns_df = pd.DataFrame(stock_returns)

# Merge with sector data
merged = pd.merge(returns_df, sector_df, on="Ticker")
sector_perf = merged.groupby("sector")["Yearly Return"].mean().sort_values(ascending=False)

fig3, ax3 = plt.subplots()
sector_perf.plot(kind="bar", ax=ax3, title="Average Yearly Return by Sector")
st.pyplot(fig3)

# === 4. Correlation Matrix ===
st.subheader("🔗 Stock Correlation Heatmap")

all_closes = pd.DataFrame()
for ticker, df in stock_data.items():
    all_closes[ticker] = df["close"]

correlation = all_closes.pct_change().corr()

fig4, ax4 = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, cmap="coolwarm", ax=ax4)
st.pyplot(fig4)

# === 5. Top Gainers & Losers (Month-wise) ===
st.subheader("📅 Top 5 Gainers and Losers - Month-wise Breakdown")

# Combine all data into one DataFrame with 'Ticker'
combined_data = []
for ticker, df in stock_data.items():
    temp_df = df.copy()
    temp_df['Ticker'] = ticker
    combined_data.append(temp_df)

selected_df = pd.concat(combined_data)

selected_df['date'] = pd.to_datetime(selected_df['date'])
selected_df['YearMonth'] = selected_df['date'].dt.to_period('M')

monthly_return = selected_df.groupby(['Ticker', 'YearMonth'])['close'].apply(
    lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0] * 100
).reset_index().rename(columns={'close': 'Monthly Return'})

unique_months = sorted(monthly_return['YearMonth'].unique())

for month in unique_months:
    month_data = monthly_return[monthly_return['YearMonth'] == month]
    top_gainers = month_data.sort_values(by='Monthly Return', ascending=False).head(5)
    top_losers = month_data.sort_values(by='Monthly Return', ascending=True).head(5)

    st.markdown(f"### 📆 {month} - Top 5 Gainers and Losers")

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.barh(top_gainers['Ticker'], top_gainers['Monthly Return'], color='green')
        ax1.set_title(f"Gainers - {month}")
        ax1.set_xlabel('Monthly Return (%)')
        ax1.invert_yaxis()
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.barh(top_losers['Ticker'], top_losers['Monthly Return'], color='red')
        ax2.set_title(f"Losers - {month}")
        ax2.set_xlabel('Monthly Return (%)')
        ax2.invert_yaxis()
        st.pyplot(fig2)
