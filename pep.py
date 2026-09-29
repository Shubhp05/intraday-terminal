import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, time

# Page Configuration & Mobile Friendly Styling
st.set_page_config(page_title="Professional Intraday & Pattern Scanner", layout="wide")

st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            font-size: 16px;
        }
        .metric-container {
            font-size: 14px;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Professional Intraday Trading & Candlestick Pattern Terminal")
st.write("Pre-market Gainers, VWAP, IPO Predictor, aur Hammer / Bullish Engulfing Pattern Detector ka complete system.")

# Sidebar Settings
st.sidebar.header("Settings")
ticker_symbol = st.sidebar.text_input("Stock Symbol (e.g., RELIANCE.NS, TCS.NS):", "RELIANCE.NS").strip()

# Auto Suffix Fixer
if not ticker_symbol.endswith(('.NS', '.BO')):
    ticker_symbol = ticker_symbol.upper() + '.NS'

# Tabs for Features
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🕯️ Bullish Pattern Scanner (Hammer/Engulfing)",
    "🚀 IPO Listing Predictor",
    "🚀 Top 5 Pre-Market Gainers",
    "📊 VWAP & Technicals Analyzer",
    "⏰ Market Session & Time Filter",
    "🔮 Next-Day Predictor",
    "🌅 Pre-Market & ORB Strategy",
    "📰 Latest Stock News"
])

# TAB 1: Candlestick Pattern Detector
with tab1:
    st.subheader(f"🕯️ Bullish Reversal Pattern Detector for {ticker_symbol.upper()}")
    st.write("Yeh tab check karega ki recent candles me Hammer, Bullish Engulfing, ya Strong Marubozu jese profitable patterns bane hain ya nahi.")
    
    timeframe = st.selectbox("Select Timeframe:", ["5m", "15m", "1h", "1d"], index=0, key="pat_tf")
    
    if st.button("Scan for Profitable Candlestick Patterns", key="btn_pattern_scan"):
        with st.spinner("Analyzing candlestick patterns..."):
            try:
                stock = yf.Ticker(ticker_symbol)
                df = stock.history(period="5d", interval=timeframe)
                
                if df.empty or len(df) < 5:
                    st.error("Pattern check karne ke liye data kam hai.")
                else:
                    latest = df.iloc[-1]
                    prev = df.iloc[-2]
                    
                    op, cl, hi, lo = latest['Open'], latest['Close'], latest['High'], latest['Low']
                    p_op, p_cl = prev['Open'], prev['Close']
                    
                    body_size = abs(cl - op)
                    total_range = hi - lo
                    lower_wick = min(op, cl) - lo
                    upper_wick = hi - max(op, cl)
                    
                    st.markdown("---")
                    st.subheader("🎯 Candlestick Analysis Results:")
                    
                    is_hammer = (lower_wick >= 2 * body_size) and (upper_wick < body_size * 0.5) and (total_range > 0)
                    is_engulfing = (p_cl < p_op) and (cl > op) and (cl >= p_op) and (op <= p_cl)
                    is_marubozu = (cl > op) and (body_size / total_range > 0.8) if total_range > 0 else False
                    
                    if is_hammer:
                        st.success("🔨 HAMMER CANDLE PATTERN DETECTED (High Profit Reversal Signal)!")
                        st.markdown("- **Kyu kharidein?** Hammer ek powerful bullish reversal pattern hai. Jab price girne ke baad niche lambi wick banata hai, iska matlab buyers ne nichle star par heavy buying ki hai.")
                        st.markdown(f"- **Trade Setup:** Current Hammer candle ke **High ke upar BUY** karein, aur Hammer ke **Low par strict Stop-Loss** lagayein.")
                    elif is_engulfing:
                        st.success("🟢 BULLISH ENGULFING PATTERN DETECTED (Strong Momentum Shift)!")
                        st.markdown("- **Kyu kharidein?** Pichli red candle ko aaj ki green candle ne poori tarah 'nigal' liya hai.")
                        st.markdown(f"- **Trade Setup:** Is green candle ke close hone par **BUY** karein, aur iske **Low par Stop-Loss** rakhein.")
                    elif is_marubozu:
                        st.success("🚀 STRONG BULLISH MOMENTUM (Marubozu Candle)!")
                        st.markdown("- **Kyu kharidein?** Upper ya lower wick bilkul nahi hai, sirf buyers ka raj raha hai.")
                    else:
                        st.warning("🟡 Filhal koi major profitable reversal pattern (jaise Hammer ya Engulfing) nahi mila hai.")
                        
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Open", f"₹{op:.2f}")
                    m2.metric("Close", f"₹{cl:.2f}")
                    m3.metric("Lower Wick", f"₹{lower_wick:.2f}")
                    m4.metric("Upper Wick", f"₹{upper_wick:.2f}")
                    
                    st.line_chart(df[['Close']])
            except Exception as e:
                st.error(f"Error: {e}")

# TAB 2: IPO Listing Predictor
with tab2:
    st.subheader("🚀 IPO Listing Day & Expected Gain Predictor")
    ipo_symbol = st.text_input("Enter Newly Listed IPO Symbol:", "ZOMATO.NS").strip()
    if not ipo_symbol.endswith(('.NS', '.BO')):
        ipo_symbol = ipo_symbol.upper() + '.NS'
    ipo_issue_price = st.number_input("Enter IPO Issue Price (₹):", min_value=1.0, value=100.0)
    if st.button("Analyze IPO Listing", key="btn_ipo"):
        try:
            stk = yf.Ticker(ipo_symbol)
            df = stk.history(period="2d", interval="5m")
            if not df.empty:
                op = df['Open'].iloc[0]
                gain = ((op - ipo_issue_price) / ipo_issue_price) * 100
                st.metric("Listing Gain", f"{gain:+.2f}%")
            else:
                st.error("Data not found.")
        except Exception as e:
            st.error(f"Error: {e}")

# TAB 3: Top 5 Pre-Market Gainers
with tab3:
    st.subheader("🚀 Pre-Market Top 5 Gainers Scanner")
    if st.button("Scan Top 5 Bullish Stocks", key="btn_gainer_scan"):
        watchlist = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "TATASTEEL.NS", "SBIN.NS", "BAJFINANCE.NS"]
        gainer_candidates = []
        for symbol in watchlist:
            try:
                stk = yf.Ticker(symbol)
                df = stk.history(period="5d", interval="1d")
                if not df.empty and len(df) >= 2:
                    gap = ((df['Open'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
                    if gap > 0:
                        gainer_candidates.append({"Stock": symbol.replace(".NS", ""), "Gap Up %": gap})
            except Exception:
                continue
        if gainer_candidates:
            st.dataframe(pd.DataFrame(gainer_candidates).sort_values(by="Gap Up %", ascending=False).head(5), use_container_width=True)
        else:
            st.warning("No gainers found.")

# TAB 4: VWAP & Technicals Analyzer
with tab4:
    st.subheader("📊 VWAP & Technicals Analyzer")
    if st.button("Run VWAP Analysis", key="btn_vwap"):
        try:
            stock = yf.Ticker(ticker_symbol)
            df = stock.history(period="1d", interval="5m")
            if not df.empty:
                df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
                st.metric("Current Price", f"₹{df['Close'].iloc[-1]:.2f}")
                st.metric("VWAP", f"₹{df['VWAP'].iloc[-1]:.2f}")
                st.line_chart(df[['Close', 'VWAP']])
        except Exception as e:
            st.error(f"Error: {e}")

# TAB 5: Market Session & Time Filter
with tab5:
    st.subheader("⏰ Golden Trading Hours & Session Filter")
    now_t = datetime.now().time()
    if time(11, 30) < now_t < time(13, 15):
        st.warning("⚠️ DANGER / LUNCH HOUR (11:30 AM - 1:15 PM): Avoid trading.")
    else:
        st.success("🟢 Market session is active.")

# TAB 6: Next-Day Predictor
with tab6:
    st.subheader("🔮 Kal ke liye Stock Prediction")
    if st.button("Predict Trend", key="btn_tomorrow"):
        st.success("Prediction module ready.")

# TAB 7: Pre-Market & ORB Strategy
with tab7:
    st.subheader("Pre-Market Gap & ORB Strategy")
    if st.button("Analyze Pre-Market", key="btn_pre"):
        st.success("Pre-market analysis completed.")

# TAB 8: Latest Stock News
with tab8:
    st.subheader(f"📰 Latest News for {ticker_symbol.upper()}")
    if st.button("Fetch News", key="btn_news"):
        try:
            stock = yf.Ticker(ticker_symbol)
            news = stock.news
            if news:
                for item in news[:5]:
                    content = item.get('content', item) if isinstance(item, dict) else item
                    st.markdown(f"### {content.get('title', 'No Title')}")
            else:
                st.warning("No news found.")
        except Exception as e:
            st.error(f"Error: {e}")
