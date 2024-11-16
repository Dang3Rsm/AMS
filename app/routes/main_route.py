from app.models.user_model import User
from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import request
import yfinance as yf
import plotly.graph_objs as go
import plotly.io as pio

main = Blueprint('main', __name__)

import yfinance as yf
import plotly.graph_objects as go
import plotly.io as pio
from flask import request

def plot_graph(symbol):
    # Get query parameters or default values
    symbol = request.args.get('symbol', symbol)

    try:
        # Fetch intraday market data for the given day
        data = yf.download(
            symbol,
            period='1d',
            interval='5m'  # 1-minute interval for intraday data
        )

        if data.empty:
            print(f"No intraday data available for {symbol}.")
            return -1

        # Create a candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=symbol
        )])

        # Enhance layout for better aesthetics
        fig.update_layout(
             
            title={
                'text': f"{symbol}",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis=dict(
                title='Time',
                showgrid=False,
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True
            ),
            yaxis=dict(
                title='Price in USD',
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=False,
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True
            ),
            template='plotly_white',
            margin=dict(l=40, r=20, t=60, b=40),
            plot_bgcolor='white',
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="black"
            ),
            xaxis_rangeslider_visible=False,
            dragmode=False
        )

        # Interactive toolbar configuration
        config = {
            'displayModeBar': False,
            'scrollZoom': False,
            'displaylogo': False,
            'dragMode':False,
        }

        # Convert to HTML for rendering
        graph_html = pio.to_html(fig, full_html=False, config=config)
        return graph_html

    except Exception as e:
        return f"An error occurred: {e}"


@main.route('/')
def index():
        MSFT_graph = plot_graph("MSFT")
        AAPL_graph = plot_graph("AAPL")
        comp_graph = plot_graph("^IXIC")
        graph_html = [comp_graph,MSFT_graph,AAPL_graph]
        return render_template('index.html', graph_html=graph_html,brand_name=current_app.config['BRAND_NAME'])
