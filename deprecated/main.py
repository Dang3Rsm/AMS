from flask import Flask, render_template, jsonify
import yfinance as yf
import plotly.graph_objs as go
import plotly.io as pio
import pytz

app = Flask(__name__)

def get_candlestick_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="5m")
    ist = pytz.timezone('Asia/Kolkata')
    data.index = data.index.tz_convert(ist)
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    try:
        symbol = "ETH-USD"
        data = get_candlestick_data(symbol)
        
        # Extract current price
        current_price = data['Close'].iloc[-1]
        
        fig = go.Figure(data=[
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlesticks'
            ),
            go.Scatter(
                x=[data.index[0], data.index[-1]],
                y=[current_price, current_price],
                mode='lines',
                line=dict(color='green', width=1),
                name='Current Price'
            )
        ])
        
        fig.update_layout(
            title=f'Candlestick Chart for {symbol}',
            xaxis_title='Time',
            yaxis_title='Price'
        )
        
        graph_json = pio.to_json(fig)
        return jsonify({"data": graph_json, "current_price": current_price})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
