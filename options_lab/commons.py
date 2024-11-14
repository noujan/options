import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import date
import yfinance as yf
import pandas as pd
from IPython.display import HTML

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import date
import yfinance as yf
import pandas as pd
from IPython.display import HTML


"""
Information below are from te below link.
https://github.com/fanzhenya/options_lab/blob/main/options_lab.ipynb
"""
def get_days_to_expiracy(target: str):
  target = tuple(map(int, target.split('-')))
  # print(*ymd)
  today = date.today()
  target = date(*target)
  delta = target - today
  # print(today, target, delta)
  return delta.days + 1

# print(get_days_to_expiracy('2020-11-20'))

def annualize_return(return_to_principle: float, days: int) -> float:
    """Return the annualized return percentage given the holding return percentage and the number of months held.
    References:
        https://en.wikipedia.org/wiki/Holding_period_return
        https://www.wikihow.com/Calculate-Annualized-Portfolio-Return
        https://stackoverflow.com/a/52618808/
    """
    rate = 1 + return_to_principle
    years = days / 365
    anr = (rate**(1 / years)) - 1
    percent = anr * 100
    return percent

# print(annualize_return(0.38/30, 2))
# print(annualize_return(5.1/35, 30))
# print(annualize_return(0.01, 7))
# print(annualize_return(0.046, 7))
# print(annualize_return(0.061, 91))

def calc_put_anr(put, exp_date, trans_fee = 0.65/100):
  return_rate = (put.bid - trans_fee) / put.strike
  days = get_days_to_expiracy(exp_date)
  return annualize_return(return_rate, days)

def calc_put_breakeven(put):
  return put.strike - put.bid

def ticker_cur_price(ticker):
  return ticker.history().tail(1)['Close'].iloc[0]

def calc_call_anr(ticker_cur_price, call, exp_date, trans_fee = 0.65/100):
  return_rate = (call.bid - trans_fee) / ticker_cur_price
  days = get_days_to_expiracy(exp_date)
  return annualize_return(return_rate, days)

def calc_call_breakeven(call):
  return call.strike + call.bid