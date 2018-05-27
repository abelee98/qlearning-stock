# -------------------
# CS182 Final Project
# Q-Learning for Stock Trading
# Ming Ying and Abraham Lee
#
# Modeled after CS182 HW3 : qLearningAgent, CS188 Berkeley (http://ai.berkeley.edu/home.html)
# -------------------

import random, math, collections, sys, copy, datetime
import qTrader as qt

""" Training function """
def train(time_interval, cutoff, price_data, vol_data):
	qt.qvalues.clear()
	for i in range(50):
		for row in range(cutoff - 100, cutoff - 5):
			state = qt.getState(row, vol_data, price_data)
			_, action = qt.getNext(state)
			reward = qt.getReward(state, action, row, price_data, 4)
			nextState = qt.getState(row+1, vol_data, price_data)
			qt.update(state, action, nextState, reward)
	return qt.getBestStock(time_interval, cutoff)