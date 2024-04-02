import yfinance as yf
from datetime import datetime
import pandas as pd

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

    def get_historical_volatility(self, period='1y'):
        """Calculate historical volatility (standard deviation of daily return) for the specified period."""
        hist = self.ticker.history(period=period)
        daily_returns = hist['Close'].pct_change()
        hv = daily_returns.std() * (252**0.5) ## Annualize the standard deviation
        return hv

    def evaluate_options(self):
        """Evaluate options baed on comparison of IV and HV."""
        hv = self.get_historical_volatility()
        exp_dates = self.ticker.options

        evaluations = []

        for data in exp_dates:
            option_chain = self.ticker.option_chain(data)
            calls = option_chain.calls
            puts = option_chain.puts

            # Concatenate calls and puts for simplicity
            options = pd.concat([calls, puts])

            # Filter options to include only neccessary data
            options = options[['strike', 'lastPrice', 'impliedVolatility']]

            # Grade options based on IV and HV
            options['HV'] = hv
            options['Evaluation'] = options.apply(
                lambda x: 'Overvalued' if x['impliedVolatility'] > hv else 'Undervalues', axis=1
            )

            evaluations.append(options)
        
        return evaluations

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
# aapl_stock.analyze_closest_expiry_options()
option_evaluations = aapl_stock.evaluate_options()

# Print evaluations for the first time expiration date as an example
print(option_evaluations[0])