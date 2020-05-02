# -*- coding: utf-8 -*-
"""
Created on Fri May  1 16:51:10 2020

@author: quent
"""


####################
#
#      Libraries                                  
#
###################################

import os
import numpy as np
import pandas as pd
import pickle
import quandl
from datetime import datetime
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
py.init_notebook_mode(connected=True)
from Functions import get_json_data, get_crypto_data, merge_dfs_on_column, df_scatter, correlation_heatmap

#notebook access
#http://localhost:8888/?token=8e6910dfe22171af99f728eab6c13af97471b35381251956

base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from the start of 2015
end_date = datetime.now() # up until today
pediod = 86400 # pull daily data (86,400 seconds per day)


# altcoin list 
altcoins = ['ETH','LTC','XRP','ETC','STR','DASH','SC','XMR','XEM']


# get data for each altcoin in the list
altcoin_data = {}
for altcoin in altcoins:
    coinpair = 'BTC_{}'.format(altcoin)
    crypto_price_df = get_crypto_data(coinpair)
    altcoin_data[altcoin] = crypto_price_df
    
# get data for BTC 
btc_usd_datasets = get_crypto_data('USDT_BTC')

for altcoin in altcoin_data.keys():
    altcoin_data[altcoin]['price_usd'] =  altcoin_data[altcoin]['weightedAverage'] * btc_usd_datasets['weightedAverage']

# Merge USD price of each altcoin into single dataframe 
combined_df = merge_dfs_on_column(list(altcoin_data.values()), list(altcoin_data.keys()), 'price_usd')
# Add BTC price to the dataframe
combined_df['BTC'] = btc_usd_datasets['weightedAverage']
print(combined_df.tail())

# Chart all of the altocoin prices
df_scatter(combined_df, 'Cryptocurrency Prices (USD)', seperate_y_axis=False, y_axis_label='Coin Value (USD)', scale='log')


combined_df_2016 = combined_df[combined_df.index.year == 2016]
combined_df_2016.pct_change().corr(method='pearson')
correlation_heatmap(combined_df_2016.pct_change(), "Cryptocurrency Correlations in 2016")


combined_df_2019 = combined_df[combined_df.index.year == 2019]
combined_df_2019.pct_change().corr(method='pearson')
correlation_heatmap(combined_df_2019.pct_change(), "Cryptocurrency Correlations in 2019")
    

