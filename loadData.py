# -------------------
# CS182 Final Project
# Q-Learning for Stock Trading
# Ming Ying and Abraham Lee
#
# Modeled after CS182 HW3 : qLearningAgent, CS188 Berkeley (http://ai.berkeley.edu/home.html)
# -------------------

import numpy as np
from pandas_datareader import data, wb
import random, math, collections, sys, copy, datetime

""" Queries Yahoo for csv files """
def fetchData(ticker):
	start_date = datetime.datetime(2012, 11, 27)
	dat = data.DataReader(ticker, 'yahoo', start_date, datetime.datetime.today())
	dat.to_csv('data/historical.csv', mode='w', header=True)


""" Formats the csv files """
def loadData(file):
	infile = np.genfromtxt(file, delimiter=',', skip_header=1,
			skip_footer=1, names=['date', 'open', 'high', 'low', 'close', 'adj', 'vol'])
	data = [infile['close'], infile['vol']] 
	return data