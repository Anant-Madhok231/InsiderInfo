"""
Copyright (c) 2025 Anant Madhok. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying, modification,
distribution, or use of this software, via any medium, is strictly prohibited
without the express written permission of Anant Madhok.

For licensing inquiries: GitHub @Anant-Madhok231
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import yfinance as yf
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from datetime import datetime
import requests
import time
import os
import json
import csv
from collections import defaultdict
from flask import g

# Google Drive CSV file ID
CSV_FILE_ID = '1PiKyr4NVkuowATtiSSDLYWaEVrTFkK2F'
CSV_FILENAME = '2013-06-03options.csv'
CSV_DRIVE_URL = f'https://drive.google.com/uc?export=download&id={CSV_FILE_ID}'

def ensure_csv_file():
    """Download CSV file from Google Drive if it doesn't exist locally"""
    if not os.path.exists(CSV_FILENAME):
        print(f"CSV file not found. Downloading from Google Drive...")
        try:
            response = requests.get(CSV_DRIVE_URL, stream=True)
            response.raise_for_status()
            
            # Google Drive may return HTML for large files, handle that
            if 'text/html' in response.headers.get('Content-Type', ''):
                # Try alternative download method
                alt_url = f'https://drive.google.com/uc?export=download&confirm=t&id={CSV_FILE_ID}'
                response = requests.get(alt_url, stream=True)
                response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(CSV_FILENAME, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            if downloaded % (1024 * 1024) == 0:  # Print every MB
                                print(f"Downloaded {downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB ({percent:.1f}%)")
            
            print(f"Successfully downloaded {CSV_FILENAME}")
            return True
        except Exception as e:
            print(f"Error downloading CSV file: {str(e)}")
            return False
    else:
        print(f"CSV file found locally: {CSV_FILENAME}")
        return True

app = Flask(__name__)
app.config.from_object(Config)

# Simple in-memory storage (this will reset when server restarts)
users = {}
unverified_users = {}
verification_codes = {}

# List of 100 popular US stocks
STOCK_LIST = [
    'AMZN', 'TSLA', 'AAPL', 'MSFT', 'JPM', 'NVDA', 'META'
]

# Add these constants at the top of your file
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
POPULAR_STOCKS = [
    'AMZN', 'TSLA', 'AAPL', 'MSFT', 'JPM', 'NVDA', 'META'
]

# Add new constant for FMP API
FMP_API_KEY = app.config['FMP_API_KEY']  # Get from config instead of hardcoding
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

POLYGON_API_KEY = "eqZkr10laolNO4aKeFxmqkZpnS3Cxssc"

def generate_verification_code():
    # Generate a 6-digit verification code and ensure it's a string
    code = ''.join(random.choices(string.digits, k=6))
    print(f"Generated code: {code}")  # Debug print
    return code

def send_verification_email(to_email, verification_code):
    try:
        # Email content
        subject = 'Verify your email for Stock Market Analytics Platform'
        body = f"""
        <html>
        <body>
            <h2>Welcome to Stock Market Analytics Platform!</h2>
            <p>Your verification code is: <strong>{verification_code}</strong></p>
            <p>Enter this code on the verification page to complete your registration.</p>
            <p>If you didn't sign up for an account, please ignore this email.</p>
        </body>
        </html>
        """

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = to_email
        msg.attach(MIMEText(body, 'html'))

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        
        # Login using the application's Gmail account
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
        # Send email
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        # Get real-time data with timeout
        hist = stock.history(period='1d', timeout=10)
        if hist.empty:
            print(f"No historical data for {symbol}")
            return None
            
        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[0]
        change = current_price - open_price
        change_percent = (change / open_price) * 100 if open_price > 0 else 0
        
        try:
            info = stock.info
        except:
            info = {}
        
        return {
            'symbol': symbol,
            'name': info.get('shortName', symbol),
            'price': f"${current_price:.2f}",
            'raw_price': current_price,
            'change': f"{'+' if change >= 0 else ''}{change:.2f} ({change_percent:.2f}%)",
            'volume': info.get('volume', 0),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', None),
            'high_24h': hist['High'].iloc[-1],
            'low_24h': hist['Low'].iloc[-1],
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def get_real_time_stock_data(symbol):
    try:
        print(f"Fetching data for {symbol} using Alpha Vantage API...")
        # Get real-time quote
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": app.config['ALPHA_VANTAGE_API_KEY']
        }
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        # Check if response is valid JSON
        try:
            data = response.json()
        except ValueError as e:
            print(f"Invalid JSON response for {symbol}: {response.text[:200]}")
            return None
        
        if "Global Quote" not in data or not data.get("Global Quote"):
            print(f"No Global Quote data for {symbol}")
            return None
            
        quote = data["Global Quote"]
        
        # Get company overview for additional details
        params["function"] = "OVERVIEW"
        overview_response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        overview_response.raise_for_status()
        
        try:
            overview = overview_response.json()
        except ValueError:
            overview = {}
        
        return {
            'symbol': symbol,
            'name': overview.get('Name', symbol),
            'price': float(quote.get('05. price', 0)),
            'change': float(quote.get('09. change', 0)),
            'change_percent': quote.get('10. change percent', '0%'),
            'volume': int(quote.get('06. volume', 0)),
            'market_cap': float(overview.get('MarketCapitalization', 0)) if overview.get('MarketCapitalization') else 0,
            'pe_ratio': float(overview.get('PERatio', 0)) if overview.get('PERatio') else None,
            'high_24h': float(quote.get('03. high', 0)),
            'low_24h': float(quote.get('04. low', 0)),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except requests.exceptions.RequestException as e:
        print(f"Request error fetching data for {symbol}: {str(e)}")
        return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def get_all_stocks():
    api_key = app.config['ALPHA_VANTAGE_API_KEY']
    interval = '5min'
    stocks_data = {}
    symbols = STOCK_LIST  # All 7 stocks
    for symbol in symbols:
        try:
            # Fetch intraday data
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': symbol,
                'interval': interval,
                'apikey': api_key,
                'outputsize': 'compact',
                'datatype': 'json',
            }
            response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            # Check if response is valid JSON
            try:
                data = response.json()
            except ValueError as e:
                print(f"Invalid JSON response for {symbol}: {response.text[:200]}")
                continue
            
            time_series_key = f"Time Series ({interval})"
            bars = data.get(time_series_key, {})
            if not bars:
                print(f"No intraday data for {symbol}")
                continue
            latest_time = sorted(bars.keys(), reverse=True)[0]
            latest_bar = bars[latest_time]
            open_price = float(latest_bar['1. open'])
            high_price = float(latest_bar['2. high'])
            low_price = float(latest_bar['3. low'])
            close_price = float(latest_bar['4. close'])
            volume = int(latest_bar['5. volume'])
            # Fetch company overview
            overview_params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': api_key
            }
            overview_resp = requests.get(ALPHA_VANTAGE_BASE_URL, params=overview_params, timeout=10)
            overview_resp.raise_for_status()
            try:
                overview = overview_resp.json()
            except ValueError:
                overview = {}
            name = overview.get('Name', symbol)
            market_cap = float(overview.get('MarketCapitalization', 0))
            pe_ratio = float(overview.get('PERatio', 0)) if overview.get('PERatio') else None
            change = close_price - open_price
            change_percent = (change / open_price) * 100 if open_price else 0.0
            stocks_data[symbol] = {
                'symbol': symbol,
                'name': name,
                'price': close_price,
                'change': change,
                'change_percent': f"{change_percent:.2f}%",
                'volume': volume,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'high_24h': high_price,
                'low_24h': low_price,
                'itr': '',
                'last_updated': latest_time
            }
            time.sleep(13)  # Wait 13 seconds to avoid rate limit
        except requests.exceptions.RequestException as e:
            print(f"Request error fetching Alpha Vantage data for {symbol}: {str(e)}")
            continue
        except Exception as e:
            print(f"Error fetching Alpha Vantage data for {symbol}: {str(e)}")
            continue
    return stocks_data

def get_historical_options_for_stocks():
    api_key = app.config['ALPHA_VANTAGE_API_KEY']
    base_url = ALPHA_VANTAGE_BASE_URL
    symbols = STOCK_LIST  # All 7 stocks
    all_options_data = {}
    for symbol in symbols:
        try:
            params = {
                'function': 'HISTORICAL_OPTIONS',
                'symbol': symbol,
                'apikey': api_key,
                'datatype': 'json',
            }
            response = requests.get(base_url, params=params)
            data = response.json()
            # The structure is: {'underlying': ..., 'option_chain': [ ... ]}
            option_chain = data.get('option_chain', [])
            parsed_options = []
            for option in option_chain:
                parsed_options.append({
                    'option_symbol': option.get('option_symbol'),
                    'type': option.get('type'),
                    'strike': option.get('strike'),
                    'expiration': option.get('expiration'),
                    'last_price': option.get('last_price'),
                    'volume': option.get('volume'),
                    'open_interest': option.get('open_interest'),
                    'implied_volatility': option.get('implied_volatility'),
                    'delta': option.get('delta'),
                    'gamma': option.get('gamma'),
                    'theta': option.get('theta'),
                    'vega': option.get('vega'),
                    'rho': option.get('rho'),
                })
            all_options_data[symbol] = parsed_options
            time.sleep(13)  # Avoid rate limit
        except Exception as e:
            print(f"Error fetching options for {symbol}: {e}")
            continue
    return all_options_data

@app.route('/')
def index():
    stocks_data = {}
    # Get all 7 stocks for the ticker
    # Use yfinance which is more reliable than Alpha Vantage
    for symbol in STOCK_LIST:
        try:
            data = get_stock_data(symbol)
            if data:
                stocks_data[symbol] = data
        except Exception as e:
            print(f"Error processing {symbol} in index route: {str(e)}")
            continue
    
    # If no stocks loaded, return empty dict (page will still load)
    return render_template('index.html', stocks=stocks_data)

# Helper to aggregate all underlyings

def aggregate_underlyings(filename):
    # Ensure CSV file exists (download from Google Drive if needed)
    if filename == CSV_FILENAME:
        ensure_csv_file()
    
    data = defaultdict(list)
    columns = []
    try:
        with open(filename, newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            columns = [c for c in reader.fieldnames if c != 'bid_size']
            for row in reader:
                underlying = row['underlying'].strip()  # Strip whitespace
                data[underlying].append(row)
        print(f"Loaded underlyings: {list(data.keys())}")  # Debug print
        agg_data = []
        for underlying, rows in data.items():
            agg_row = {'underlying': underlying}
            count = len(rows)
            avg_cols = ['bid', 'ask', 'delta', 'gamma', 'theta', 'vega', 'implied_volatility']
            sum_cols = ['volume', 'open_interest']
            for col in columns:
                if col in ['underlying']:
                    continue
                if col in avg_cols:
                    vals = [float(r[col]) for r in rows if r[col] not in ('', None)]
                    agg_row[col] = sum(vals)/len(vals) if vals else ''
                elif col in sum_cols:
                    vals = [float(r[col]) for r in rows if r[col] not in ('', None)]
                    agg_row[col] = sum(vals) if vals else 0
                else:
                    agg_row[col] = rows[0][col]
            # Calculate Insider Trade Ratio (ITR)
            try:
                volume = float(agg_row.get('volume', 0))
                open_interest = float(agg_row.get('open_interest', 0))
                vega = abs(float(agg_row.get('vega', 0)))
                delta = abs(float(agg_row.get('delta', 0)))
                implied_volatility = float(agg_row.get('implied_volatility', 0))
                gamma = abs(float(agg_row.get('gamma', 0)))
                theta = abs(float(agg_row.get('theta', 0)))
                numerator = (volume + 1) * vega * delta * implied_volatility
                denominator = (open_interest + 1) * (gamma + theta + 1)
                if denominator != 0:
                    itr = numerator / denominator
                else:
                    itr = 0
                agg_row['insider_trade_ratio'] = round(itr, 3)
            except Exception as e:
                agg_row['insider_trade_ratio'] = ''
            agg_data.append(agg_row)
        show_columns = ['underlying'] + [c for c in columns if c != 'underlying'] + ['insider_trade_ratio']
        return agg_data, show_columns
    except Exception as e:
        print(f"Error reading/aggregating CSV: {e}")
        return [], []

@app.route('/search_underlying')
def search_underlying():
    filename = CSV_FILENAME
    query = request.args.get('query', '').strip().upper()
    agg_data, show_columns = aggregate_underlyings(filename)
    print(f"Searching for: {query}")  # Debug print
    print(f"Available underlyings: {[row['underlying'] for row in agg_data]}")  # Debug print
    for row in agg_data:
        if row['underlying'].upper() == query:
            return jsonify({'columns': show_columns, 'row': row})
    return jsonify({'error': 'Not found'}), 404

@app.route('/search')
def search():
    query = request.args.get('query', '').strip().upper()
    results = []
    
    if query:
        # Search in both symbol and company name within our 7 companies
        for symbol in STOCK_LIST:
            if query in symbol.upper():
                data = get_stock_data(symbol)
                if data:
                    results.append(data)
            else:
                # Try to get data and check company name
                data = get_stock_data(symbol)
                if data and query.lower() in data.get('name', '').lower():
                    results.append(data)
    
    return jsonify(results)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))

        if email in users or email in unverified_users:
            flash('Email already registered')
            return redirect(url_for('signup'))

        # Generate verification code
        verification_code = generate_verification_code()
        verification_codes[email] = verification_code

        # Send verification email
        if send_verification_email(email, verification_code):
            unverified_users[email] = {
                'username': username,
                'password': password
            }
            session['temp_email'] = email
            flash('Verification code sent to your email!')
            return redirect(url_for('verify_code'))
        else:
            flash('Error sending verification email. Please try again.')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    email = session.get('temp_email')
    if not email or email not in verification_codes:
        return redirect(url_for('signup'))

    if request.method == 'POST':
        user_code = request.form.get('verification_code').strip()
        stored_code = verification_codes.get(email)
        
        # Debug prints
        print(f"User entered code: '{user_code}', type: {type(user_code)}")
        print(f"Stored code: '{stored_code}', type: {type(stored_code)}")
        print(f"Are they equal? {user_code == stored_code}")
        print(f"Verification codes dict: {verification_codes}")
        
        if user_code == stored_code:
            # Move user from unverified to verified
            users[email] = unverified_users.pop(email)
            verification_codes.pop(email)
            session.pop('temp_email')
            flash('Email verified successfully! You can now login.')
            return redirect(url_for('login'))
        else:
            flash('Invalid verification code. Please try again.')
            print(f"Codes don't match. User: '{user_code}' vs Stored: '{stored_code}'")

    return render_template('verify_code.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in unverified_users:
            flash('Please verify your email before logging in.')
            session['temp_email'] = email
            return redirect(url_for('verify_code'))
        
        if email in users and users[email]['password'] == password:
            session['user_email'] = email
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('home'))

@app.route('/update-stock-prices')
def update_stock_prices():
    symbols = request.args.get('symbols', '').split(',')
    updated_data = {}
    
    for symbol in symbols:
        if symbol in STOCK_LIST:
            data = get_real_time_stock_data(symbol)
            if data:
                updated_data[symbol] = data
            time.sleep(0.1)
    
    return jsonify(updated_data)

@app.route('/underlying/<underlying_name>')
def underlying_detail(underlying_name):
    filename = CSV_FILENAME
    agg_data, show_columns = aggregate_underlyings(filename)
    # Find the row for the given underlying
    row = next((r for r in agg_data if r['underlying'].upper() == underlying_name.upper()), None)
    if not row:
        return render_template('underlying.html', not_found=True, underlying=underlying_name)
    return render_template('underlying.html', not_found=False, underlying=underlying_name, columns=show_columns, row=row)

# In-memory storage for portfolio and watchlist (per session)
def get_user_portfolio():
    if 'portfolio' not in session:
        session['portfolio'] = []
    return session['portfolio']

def get_user_watchlist():
    if 'watchlist' not in session:
        session['watchlist'] = []
    return session['watchlist']

@app.route('/portfolio')
def portfolio():
    portfolio = get_user_portfolio()
    stocks = []
    agg_data, _ = aggregate_underlyings(CSV_FILENAME)
    for symbol in portfolio:
        data = get_stock_data(symbol)
        row = next((r for r in agg_data if r['underlying'].upper() == symbol.upper()), None)
        itr = row['insider_trade_ratio'] if row else ''
        if data:
            data['itr'] = itr
            stocks.append(data)
        else:
            # Show at least the symbol and ITR if no yfinance data
            stocks.append({
                'symbol': symbol,
                'name': symbol,
                'price': 'N/A',
                'change': 'N/A',
                'itr': itr
            })
    return render_template('portfolio.html', stocks=stocks)

@app.route('/watchlist')
def watchlist():
    watchlist = get_user_watchlist()
    stocks = []
    agg_data, _ = aggregate_underlyings(CSV_FILENAME)
    for symbol in watchlist:
        data = get_stock_data(symbol)
        row = next((r for r in agg_data if r['underlying'].upper() == symbol.upper()), None)
        itr = row['insider_trade_ratio'] if row else ''
        if data:
            data['itr'] = itr
            stocks.append(data)
        else:
            stocks.append({
                'symbol': symbol,
                'name': symbol,
                'price': 'N/A',
                'change': 'N/A',
                'itr': itr
            })
    return render_template('watchlist.html', stocks=stocks)

@app.route('/add_to_portfolio/<symbol>')
def add_to_portfolio(symbol):
    symbol = symbol.upper()
    portfolio = get_user_portfolio()
    if symbol not in portfolio:
        portfolio.append(symbol)
        session['portfolio'] = portfolio
    return redirect(url_for('portfolio'))

@app.route('/add_to_watchlist/<symbol>')
def add_to_watchlist(symbol):
    symbol = symbol.upper()
    watchlist = get_user_watchlist()
    if symbol not in watchlist:
        watchlist.append(symbol)
        session['watchlist'] = watchlist
    return redirect(url_for('watchlist'))

@app.route('/remove_from_portfolio/<symbol>')
def remove_from_portfolio(symbol):
    symbol = symbol.upper()
    portfolio = get_user_portfolio()
    if symbol in portfolio:
        portfolio.remove(symbol)
        session['portfolio'] = portfolio
    return redirect(url_for('portfolio'))

@app.route('/remove_from_watchlist/<symbol>')
def remove_from_watchlist(symbol):
    symbol = symbol.upper()
    watchlist = get_user_watchlist()
    if symbol in watchlist:
        watchlist.remove(symbol)
        session['watchlist'] = watchlist
    return redirect(url_for('watchlist'))

if __name__ == '__main__':
    # Ensure CSV file is available before starting the app
    ensure_csv_file()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 