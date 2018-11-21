# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-14

# import networkx as nx
# from pprint import pprint as pt
# import matplotlib.pyplot as plt

from Map import Map
from RuleLibrary import RuleLib
from itertools import combinations
import copy
import misc
from random import choice
from queue import Queue
from ThinkingEnergyCost import TEC
import math


class StateNode(object):
	'''
	Property:
		id = [0, 1, 0, ...]:表示分支编码
		children = [], 子树节点, children[someone].id = self.id + index
		parent = None, 指向双亲结点
		map: Map
		ruleLib: RuleLib
		isPossible = True
		logger = [
		{'op': , 'size': , 'amount': }
		...
		]

	Funtion:
		__init__
		__str__: 用于输出解题结果
		由StateTree操作数据
	'''

	class logger(object):
		
		def __init__(self, base = 1):
			self.log = []
			self.base = base
		
		def addLog(self, logList):
			for l in logList:
				l['base'] = self.base
			self.log += logList
		pass



	def __init__(self, stateMap, ruleLib, stateLogger, stateID=[0], parent=None):
		self.map = stateMap
		self.ruleLib = ruleLib
		self.id = stateID
		self.children = []
		self.parent = parent
		self.logger = stateLogger
		self.solved = False

		self.map.logger = self.logger
		self.ruleLib.logger = self.logger


	def outputRusult(self, solutionOrder=0):
		print('-'*10 + 'Solution' + str(solutionOrder) + '-'*10)
		self.map.outputMap()
		print('Branch ID: ' + str(self.id))
		print('\nTEC: ' + "%.3f" % TEC.BaseTEC(self.logger.log))
		print('\n')


class StateTree(object):
	'''
	Property:
		root: StateNode(id = '')
	Function:
		__init__(self, root): 输入初始规则，建根
		addStateChilds(self, currentNode, toSelect, ARType): 新增状态分支
		implementRule(self, targetNode, ARType):  应用AR于具体分支（内部使用）
		implementRule(self, ARType): 应用AR（外部接口）
		solve(self)
	'''

	def __init__(self, root):
		self.root = root

	def addStateChilds(self, currentNode, toSelect, ARType, amount):
		'''
		Funtion: create new branch when UAR, and simplify each branch's rueLib, and pop the AR to implement
		Input: currentNode(applying UAR), toSelect(available & possibleSet), ARType(lead to UAR)
		**Attention**: Must be UAR
		'''

		# Genernate full-comb of branch subsets as [subset_1, ...]

		mustSelect = set(toSelect) # is a copy of toSelect
		for key in filter(lambda a: a!=ARType, currentNode.ruleLib.AR.keys()): # 过滤掉应当应用的AR
			mustSelect -= currentNode.ruleLib.AR[key]['possibleSet']
		toSelect -= mustSelect

		branchSets = list(combinations(toSelect, amount - len(mustSelect))) # is list of tuples
		for i in range(len(branchSets)):
			branchSets[i] += tuple(mustSelect)

		currentNode.logger.addLog([ 
			{'op': 'createBranch'},
			{'op': 'selectCombtoTry'}
			])

		for i in range(misc.comb(len(toSelect), amount - len(mustSelect))):  # C(available, need)
			sn = StateNode(
				stateMap = copy.deepcopy(currentNode.map), 
				ruleLib = copy.deepcopy(currentNode.ruleLib),
				stateID = currentNode.id + [i], 
				stateLogger = copy.deepcopy(currentNode.logger),
				parent = currentNode
				)  # 建节点，note：id里包含了次序, 子类logger自动迁移
			sn.logger.base *= math.sqrt(misc.comb(len(toSelect), amount)) # 假设以人的智慧，需要试探的次数期望为sqrt(可能情形)，可以用之后的每一步操作*能量倍数s近似估计耗费的能量

			implementSet = branchSets.pop()
			sn.ruleLib.AR[ARType]['possibleSet'] = set(implementSet) # 此时UAR变为CAR
			sn.ruleLib.simplifyLib(sn.map) # 此步是为了消除可能的组合选取产生的无解（AR弹出后无法再进行矛盾验证）

			sn.ruleLib.AR.pop(ARType) # 此时再删除AR
			sn.map.implement(ARType, implementSet)  # 写地图
			currentNode.children.append(sn)  # 加子节点



	def implementAR(self, targetNode, ARType):
		'''
		Funtion: Implement an AR to a state
		Input: targetNode: StateNode, ARType: string
		Output: Possible State(s), for CAR/ UAR
		'''

		applyingAR = targetNode.ruleLib.AR[ARType]
		toSelect = applyingAR['possibleSet'] & targetNode.map.getEmpty()
		targetNode.logger.addLog([{'op': 'getSizeofAR'}])
		applyingAmount = applyingAR['amount']

		if applyingAmount == len(toSelect):  # CAR
			targetNode.map.implement(ARType, toSelect)
			targetNode.logger.addLog([{
				'op': 'clearOccupiedGrids', 
				'size': len(toSelect), 
				'amount': len(targetNode.ruleLib.AR) - 1 # 减去自身
				}]) #提前叠加清除Occupied Grids的能量

			targetNode.ruleLib.AR.pop(ARType)  # 删除应用完的AR
			if targetNode.map.getEmpty() == set([]):  # 出现一个解
				targetNode.solved = True
			return [targetNode]

		elif applyingAmount < len(toSelect):  # UAR
			self.addStateChilds(targetNode, toSelect, ARType, applyingAmount)
			return targetNode.children
		else:  # Grids not enough <=> no solution
			return []

	def solve(self):
		possibleStateQueue = Queue()
		possibleStateQueue.put(self.root)
		solutionCount = 0

		while possibleStateQueue.empty() == False:
			thisState = possibleStateQueue.get()
			thisState.ruleLib.simplifyLib(thisState.map)
			ARTypeToImplement = thisState.ruleLib.chooseRule(thisState.map)

			nextNodes = self.implementAR(thisState, ARTypeToImplement)
			for node in nextNodes:
				if node.solved == True:
					solutionCount += 1
					node.outputRusult(solutionCount)
				else:
					possibleStateQueue.put(node)

		if solutionCount == 0:
			print('-'*5 + 'No solution' + '-'*5)
