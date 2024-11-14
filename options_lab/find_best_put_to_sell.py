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

from commons import *

def find_best_put_to_sell(ticker_name, max_breakeven, min_volume = 10, min_last_price = 0.01, top_k = 10):
  """
  Input a ticker and the max breakeven price, output the top cash covered put options to sell that 
  yields highest Annualized Return Rate for the cash collateral.
  """
  ticker = yf.Ticker(ticker_name)
  print("ticker", ticker.info["symbol"])
  all_puts = pd.DataFrame()

  for exp_date in ticker.options:
    opts = ticker.option_chain(exp_date)
  
    puts = opts.puts
    
    puts['expDate'] = exp_date

    # filter by max breakeven
    puts['breakeven'] = puts.apply(calc_put_breakeven, axis=1)
    puts = puts[puts['breakeven'] < max_breakeven]

    # filter by volume
    puts = puts[puts['volume'] > min_volume]

    # filter garbage bid prices
    puts = puts[puts['bid'] > min_last_price]

    if puts.empty:
      continue;

    puts['sellPutARR'] = puts.apply(lambda put: calc_put_anr(put, exp_date) , axis=1)
    to_add = puts[['expDate', 'strike', 'bid', 'impliedVolatility', 'volume', 'breakeven', 'sellPutARR']]
    # all_puts = all_puts.append(to_add, ignore_index=True)
    all_puts = pd.concat([all_puts, pd.DataFrame(to_add)], ignore_index=True)

  all_puts = all_puts.sort_values(['sellPutARR', 'volume', 'breakeven'], ascending=[0, 0, 1])

  # print
  all_puts.index = ['']*len(all_puts)
  # print(all_puts.head(top_k))
  return all_puts.head(top_k)


  # find_best_put_to_sell('NIO', max_breakeven = 40)
# find_best_put_to_sell('XPEV', max_breakeven = 40)
# find_best_put_to_sell('TSLA', max_breakeven = 440)
# find_best_put_to_sell('BABA', max_breakeven = 260)
# find_best_put_to_sell('QQQ', max_breakeven = 270)
# find_best_put_to_sell('VOO', max_breakeven = 300)
# find_best_put_to_sell('UVXY', max_breakeven = 9.5)

find_best_put_to_sell('LI', max_breakeven = 34)