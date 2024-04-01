import yfinance as yf

# Choose a stock symbol
symbol = 'AAPL'

# Fetch the stock data
stock = yf.Ticker(symbol)

# Get options expiration dates.
options_dates = stock.options

# Get expiration data for the first available option
opts = stock.option_chain(options_dates[0])

# options contains two dataframes: calls and puts
calls = opts.calls # DataFrame of call options
puts = opts.puts # DataFrame of put options

# Display the first row of call options
print(calls)