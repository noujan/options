import yfinance as yf
from datetime import datetime

class Stock:
    def __init__(self, symbol):
        # Choose a stock symbol
        # symbol = 'AAPL'
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.current_price = None
        self._fetch_current_price()

    def _fetch_current_price(self):
        """Fetch the last closing price of the stock."""
        try:
            self.current_price = self.ticker.history(period="id")['Close'][0]
        except IndexError:
            print("Error fetching current price.")
            self.current_price = None

    def analyze_closest_expiry_options(self):
        """ Analyze closest options for covered calls and cash-secured-puts."""
        if self.current_price is None:
            print("Current price not available.")
            return

        # Get the list of expiration dates and select the closest one.
        try:
            closest_expiry = self.ticker.options[0]
        except IndexError:
            print(f"No options available for {self.symbol}")
            return

        todays_options = self.ticker.option_chain(closest_expiry)

        calls = todays_options.calls
        puts = todays_options.puts

        # Filter for OTM calls and puts based on the current price
        otm_calls = calls[calls['strike'] > self.current_price]
        otm_puts = puts[puts['strike'] < self.current_price]

        # Display analysis (simple example)
        print(f"Closest Expiry OTM Calls for {self.symbol}:")
        print(otm_calls[['strike', 'lastPrice', 'impliedVolatility']])
        print(f"closest Expiry OTM Puts for {self.symbol}")
        print(otm_puts[['strike', 'lastPrice', 'impliedVolatility']])


# Example usage
aapl_stock = Stock("AAPL")
aapl_stock.analyze_closest_expiry_options()