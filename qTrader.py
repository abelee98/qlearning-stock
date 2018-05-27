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

ALPHA = 0.2
DISCOUNT = 0.9
SHORT_TERM = int(7)
MID_TERM = int(14)
LONG_TERM = int(180)

""" Dictionary to hold all Q-Values """
qvalues = collections.Counter()

""" Initialization of VPT value """
VPT = 0

""" Plots data points to a graph """
def plotGraphs(price_data):
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	ax1.plot(range(len(price_data)), price_data, color='r', label='Stock Price')
	plt.show()


""" Returns the best action for stock """
def getBestStock(time_interval, cutoff):
	global qvalues
	difference = float("inf")
	bestact = 'sell'
	q_list = []
	# print "Q Values: ", qvalues
	temp = 0
	if VPT != 0:
		if VPT > 0:	
			temp = int(math.log(VPT))
		elif VPT < 0:
			temp = -1 * (int(math.log(-1 * VPT)))
	for key, value in qvalues.iteritems():
		state, _ = key
		if abs(temp - state) <= difference:
			q_list.append(key)
			difference = abs(temp - state)
	if len(q_list) == 1:
		return q_list[0][1]
	else: 
		count = -float("inf")
		for action in getLegalActions():
			if qvalues[(temp, action)] > count:
				count = qvalues[(temp, action)]
				bestact = action
		return bestact

""" Gets the state (VPT) """
def getState(time, vol_data, price_data):
	global VPT
	VPT += ((price_data[time] - price_data[time - 1])/price_data[time - 1]) * vol_data[time]
	if VPT != 0:
		if VPT > 0:	
			return int(math.log(VPT))
		elif VPT < 0:
			return -1 * (int(math.log(-1 * VPT)))
	return 0

""" Updates Q-Values for stock """
def update(state, action, nextState, reward):
	curval = qvalues[(state, action)]
	nextval =  (DISCOUNT * getNext(nextState)[0])
	qvalues[(state, action)] = ((1 - ALPHA) * curval) + (ALPHA * (reward + nextval))

""" Returns the Q-Value for stock """
def getQValue(state, action):
	return qvalues[(state, action)]

""" Returns the best State, Action pair """
def getNext(state):
	bestact = 'sell'
	bestval = -float("inf")
	for action in getLegalActions():
	  val = getQValue(state, action)
	  if val > bestval:
		bestact = action
		bestval = val
	if flipCoin(0.05):
		bestact = random.choice(getLegalActions())
	return [bestval, bestact]


""" Returns reward at state for action """
def getReward(state, action, time, data, time_interval):
	if action == 'buy':
		return data[time + time_interval] - data[time]
	else:
		return -1 * (data[time + time_interval] - data[time])

""" Used to introduce some randomization """
def flipCoin( p ):
    r = random.random()
    return r < p

""" Returns all possible legal actions """
def getLegalActions():
	return ['buy', 'sell']

