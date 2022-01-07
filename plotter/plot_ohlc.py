import plotly.graph_objects as go

import pandas as pd
import plotly.subplots

PARAM__SYMBOL = "1INCHUSDT"
PARAM__INTERVAL = "1h"

PARAM__FILE_ID = "20220103.csv"

ingestion_data_path = f"data/ingestion/binance/{PARAM__SYMBOL}/{PARAM__INTERVAL}/{PARAM__FILE_ID}"

def plot_ohlc():
    df = pd.read_csv(ingestion_data_path)
    df['timestamp'] = pd.to_datetime(df['OpenTime'], unit='ms', utc=True)

    fig = go.Figure(data=[
        go.Candlestick(
            x=df['timestamp'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']
        )
    ])

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()


if __name__ == '__main__':
    df = pd.read_csv(ingestion_data_path)
    df['timestamp'] = pd.to_datetime(df['OpenTime'], unit='ms', utc=True)

    fig = plotly.subplots.make_subplots(rows=2, cols=1)

    fig.add_trace(go.Scatter(
        name='Close Price',
        x=df['timestamp'],
        y=df['Close'],
        fill='tozeroy'
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        name='Volume',
        x=df['timestamp'],
        y=df['Volume']
    ), row=2, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()
