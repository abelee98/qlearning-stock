# -------------------
# CS182 Final Project
# Q-Learning for Stock Trading
# Ming Ying and Abraham Lee
#
# Modeled after CS182 HW3 : qLearningAgent, CS188 Berkeley (http://ai.berkeley.edu/home.html)
# -------------------


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections  as mc
from pandas_datareader import data, wb
import random, math, collections, sys, copy, datetime
import qTrader as qt
import train as tr
import loadData as ld

CSV = 'data/historical.csv'
ALPHA = 0.2
DISCOUNT = 0.9
SHORT_TERM = 7
MID_TERM = 30
LONG_TERM = 180

def main():
	stock = ''
	try:
		stock = raw_input("Enter stock ticker: ")
		build_model(stock)
	except:
		stock = raw_input("Enter a stock ticker: ")
		build_model(stock)

def build_model(stock):
	print "Running...this may take a few minutes."
	print "Initializing regression on 5-year historical data..."
	ld.fetchData(str(stock))
	price_data, vol_data = ld.loadData(CSV)
	total = 0
	plot_total = []
	prev_action = 'sell'
	count = 100
	while prev_action == 'sell':
		prev_action = tr.train(MID_TERM, count, price_data, vol_data)
		prev_amt = price_data[count]
		count += 1
	plot_total.append((price_data[count-1], prev_action))	
	for i in range(count, len(price_data)-MID_TERM, 30):
		action = tr.train(MID_TERM, i, price_data, vol_data)
		if action == 'buy':
			if action == prev_action:
				total += price_data[i] - prev_amt
				plot_total.append((price_data[i], 'hold'))
			else:
				plot_total.append((price_data[i], action))
			prev_amt = price_data[i]											
			prev_action = action
		elif action == 'sell':
			if action != prev_action:
				total += price_data[i] - prev_amt 
				plot_total.append((price_data[i], action))		
			else:
				plot_total.append((price_data[i], 'hold'))	
			prev_action = action
		# print "Action at time " + str(i) + " : " + action
	print "*********************"
	print "Total return: ", total
	print "Best action now: ", qt.getBestStock(MID_TERM, len(price_data))
	count = 0
	plt.clf()
	plt.plot()
	for point in plot_total:
		t, a = point
		plt.plot(count, t, get_color(a), zorder = 1)
		count += 1
	plt.plot(range(len(plot_total)), [x[0] for x in plot_total], 'b--', zorder = 2, label='Price')
	plt.suptitle(stock)
	plt.legend(loc='upper left')
	plt.show()

def get_color(act):
	if act == 'buy':
		return 'g^'
	elif act == 'hold':
		return ','
	return 'rs'

if __name__ == "__main__":
	main()