# 📊 Data-Driven Stock Analysis Dashboard

A **Streamlit web app** that analyzes and visualizes stock market data using Nifty 50 stocks. It provides key insights into stock performance, volatility, sector trends, and more.

---

## 🚀 Features

- 📈 **Daily Returns & Volatility**
- 📉 **Cumulative Returns Over Time**
- 🏢 **Sector-wise Yearly Performance**
- 🔗 **Correlation Heatmap Across Stocks**
- 📅 **Top Monthly Gainers & Losers**
- ✅ **Manual Sector Mapping for Incomplete Tickers**

---

## 🧾 Technologies Used

- **Python**
- **Pandas**, **NumPy**
- **Matplotlib**, **Seaborn**
- **Streamlit**

---

## 📁 Project Structure

📦 stock-analysis-app/
├── app.py # Main Streamlit app that loads data, processes stocks, and displays charts
├── requirements.txt # List of Python libraries needed to run the app
├── README.md # Project description and usage instructions
├── .gitignore # Files and folders to exclude from version control
├── /data/ # (Optional) Folder to store raw stock CSV files
├── Sector_data.csv # CSV containing ticker-to-sector mappings
├── cumul_return.csv # Output file with cumulative return per stock
├── volatility.csv # Output file with calculated volatilities
├── top10_volatile.csv # Output file showing top 10 most volatile stocks
├── Final data files1/ # Processed stock CSV files with added columns


> If you're not uploading output files like `volatility.csv`, you can generate them by running the app.

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
    git clone https://github.com/your-username/stock-analysis-app.git
    cd stock-analysis-app

2.Install Dependencies

    pip install -r requirements.txt

3.Run the Streamlit App

    Run the Streamlit App

4. Data Sources

    Stock CSV files with columns like: date, open, high, low, close, volume

    Sector mapping from Sector_data.csv

You must place stock data files in a directory and provide its path in the app.


Deploying on Streamlit Cloud (Optional)
Want to make your app accessible on the web? Here’s how:

Push your code to GitHub

Go to https://streamlit.io/cloud

Sign in with your GitHub account

Click "New App" and select your repository

Set app.py as the main file

Click Deploy

Your app will be live within a few seconds!

Author
Jayaganesh Sekar
[jayaganeshs89@gmail.com]
www.linkedin.com/in/jayaganesh-sekar-27139121a


📃 License
This project is licensed under the MIT License – feel free to use and modify.
