import yfinance as yf
import pandas as pd
import ta  # Technical Analysis library

# Download HDFC Bank hourly data
ticker = "ICICIBANK.NS"
data = yf.download(ticker, interval="1h", period="1mo")

# Check column names in the downloaded data
print(data.columns)

# Ensure the data has the required columns ('High', 'Low', 'Close')
if 'High' in data.columns and 'Low' in data.columns and 'Close' in data.columns:
    # Remove timezone information from the index to prevent Excel writing issues
    data.index = data.index.tz_localize(None)

    data['parabolic_sar'] = ta.trend.PSARIndicator(data['High'], data['Low'], data['Close']).psar()
    data['stoch_rsi'] = ta.momentum.StochRSIIndicator(data['Close'], window=14).stochrsi_k()
    data['ema_21'] = ta.trend.EMAIndicator(data['Close'], window=21).ema_indicator()
    data['sma_50'] = ta.trend.SMAIndicator(data['Close'], window=50).sma_indicator()
    data['rsi'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
    
    # Smooth volume for oscillatory volume
    data['smoothed_volume'] = data['Volume'].rolling(window=9).mean()

    # Scoring system
    def calculate_score(row):
        score = 0

        # Parabolic SAR: Positive score if below close (bullish), negative if above (bearish)
        if row['parabolic_sar'] < row['Close']:
            score += 2
        else:
            score -= 2

        # Stochastic RSI: Positive score if oversold (<20), negative if overbought (>80)
        if row['stoch_rsi'] < 20:
            score += 2
        elif row['stoch_rsi'] > 80:
            score -= 1

        # Moving Averages: Positive if 21 EMA > 50 SMA (bullish crossover)
        if row['ema_21'] > row['sma_50']:
            score += 2
        elif row['ema_21'] < row['sma_50']:
            score -= 2

        # RSI: Positive if oversold (<30), negative if overbought (>70)
        if row['rsi'] < 30:
            score += 2
        elif row['rsi'] > 70:
            score -= 1

        return score

    # Apply the scoring system
    data['score'] = data.apply(calculate_score, axis=1)

    # Generate buy/sell signals based on threshold score
    data['signal'] = data['score'].apply(lambda x: 'BUY' if x >= 8 else ('SELL' if x <= 0 else 'HOLD'))

    # Backtest: Calculate profit/loss based on future price movement
    data['future_price'] = data['Close'].shift(-4)  # Check price 4 hours ahead
    data['profit'] = data['future_price'] - data['Close']  # Profit for buy signals
    data['sell_profit'] = data['Close'] - data['future_price']  # Profit for sell signals

    # Evaluate backtest results
    buy_signals = data[data['signal'] == 'BUY']
    sell_signals = data[data['signal'] == 'SELL']

    # Calculate performance for buy/sell signals
    buy_signals['profit_per_trade'] = buy_signals['profit']
    sell_signals['profit_per_trade'] = sell_signals['sell_profit']

    # Write to an Excel spreadsheet
    with pd.ExcelWriter('icici_bank_backtest_results.xlsx', engine='openpyxl') as writer:
        data.to_excel(writer, sheet_name='Raw_Data')
        buy_signals[['Close', 'future_price', 'profit_per_trade']].to_excel(writer, sheet_name='Buy_Signals')
        sell_signals[['Close', 'future_price', 'profit_per_trade']].to_excel(writer, sheet_name='Sell_Signals')

    print("Backtest results saved to hdfc_bank_backtest_results.xlsx")

else:
    print("Error: Data columns 'High', 'Low', or 'Close' not found.")
