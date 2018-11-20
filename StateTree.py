# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-14

# import networkx as nx
# from pprint import pprint as pt
# import matplotlib.pyplot as plt

from Map import Map
from itertools import combinations
import copy
import misc
from random import choice
from queue import Queue
from ThinkingEnergyCost import TEC


class StateNode(object):
<<<<<<< HEAD
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

	def __init__(self, stateMap, ruleLib, stateID=[], logger=[], parent=None):
		self.map = stateMap
		self.ruleLib = ruleLib
		self.id = stateID
		self.children = []
		self.parent = parent
		self.logger = logger
		self.solved = False

		self.map.logger = self.logger
		self.ruleLib.logger = self.logger

			

	def outputRusult(self, solutionOrder=0):
		print('-'*5 + 'Solution' + str(solutionOrder) + '-'*5)
		print()
		print('TEC: ' + TEC.BaseTEC(self.logger))
		self.map.outputMap()
		print('\n\n')


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
		Funtion: create new branch when UAR
		Input: currentNode(applying UAR), toSelect(available & possibleSet), ARType(lead to UAR)
		**Attention**: Must be UAR
		'''

		# Genernate full-comb of branch subsets as [subset_1, ...]
		branchSets = list(combinations(toSelect, amount))
		currentNode.logger += [
			{'op': 'createBranch'},
			{'op': 'selectCombtoTry'}
			]

		for i in range(misc.comb(len(toSelect), amount)):  # C(available, need)
			sn = StateNode(
				stateMap = copy.deepcopy(currentNode.map), 
				ruleLib = copy.deepcopy(currentNode.ruleLib),
				stateID = currentNode.id.append(i), 
				logger = copy.deepcopy(currentNode.logger),
				parent = currentNode
				)  # 建节点，note：id里包含了次序, 子类logger自动迁移

		sn.map.implement(ARType, branchSets.pop())  # 写地图
		currentNode.children.append(sn)  # 加子节点

	def implementAR(self, targetNode, ARType):
		'''
		Funtion: Implement an AR to a state
		Input: targetNode: StateNode, ARType: string
		Output: Possible State(s), for CAR/ UAR
		'''

		applyingAR = targetNode.ruleLib.AR[ARType]
		toSelect = applyingAR['possibleSet'] & targetNode.map.getEmpty()
		targetNode.logger += [{'op': 'getSizeofAR'}]

		if applyingAR['possibleSet'] == toSelect:  # CAR
			targetNode.map.implement(ARType, toSelect)
			targetNode.loggger += [{
				'op': 'clearOccupiedGrids', 
				'size': len(toSelect), 
				'amount': len(targetNode.ruleLib.AR) - 1 # 减去自身
				}] #提前叠加清除Occupied Grids的能量

			targetNode.ruleLib.AR.pop(ARType)  # 删除应用完的AR
			if targetNode.map.getEmpty() == set([]):  # 出现一个解
				targetNode.solved = True
			return [targetNode]

		elif applyingAR['possibleSet'] < toSelect:  # UAR
			animalAmount = applyingAR['amount']
			self.addStateChilds(targetNode, toSelect, ARType, animalAmount)
			return targetNode.children
		else:  # Grids not enough <=> no solution
			targetNode.state = None

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
=======
    '''
    Property:
        id = '':表示分支编码
        children = [], 子树节点, children[someone].id = self.id + index
        parent = None, 指向双亲结点
        state = {'map': Map, 'rules': RuleLib: }
        isPossible = True
    Funtion:
        __init__
        __str__: 用于输出解题结果
        由StateTree操作数据
    '''

    def __init__(self, state, id=[], energy=0, parent=None):
        self.state = state
        self.id = []
        self.children = []
        self.parent = None
        self.energy = energy
        self.solved = False

    def outputRusult(self, solutionOrder=0):
        print('-'*5 + 'Solution' + str(solutionOrder) + '-'*5)
        print()
        print('TEC: ' + str(self.energy))
        self.state['map'].outputMap()
        print('\n\n')


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
        Funtion: create new branch when UAR
        Input: currentNode(applying UAR), toSelect(available & possibleSet), ARType(lead to UAR)
        **Attention**: Must be UAR
        '''

        # Genernate full-comb of branch subsets as [subset_1, ...]
        branchSets = list(combinations(toSelect, amount))
        for i in range(misc.comb(len(toSelect), amount)):  # C(available, need)
            newState = copy.deepcopy(currentNode.state)
            newState['map'].implement(ARType, branchSets.pop())  # 写地图
            sn = StateNode(newState, currentNode.id.append(
                i), currentNode.energy, currentNode)  # 建节点，note：id里包含了次序
            currentNode.children.append(sn)  # 加子节点

    def implementAR(self, targetNode, ARType):
        '''
        Funtion: Implement an AR to a state
        Input: targetNode: StateNode, ARType: string
        Output: Possible State(s), for CAR/ UAR
        '''

        applyingAR = targetNode.state['rules'].AR[ARType]
        thisMap = targetNode.state['map']
        toSelect = applyingAR['possibleSet'] & thisMap.getEmpty()

        if applyingAR['possibleSet'] == toSelect:  # CAR

            targetNode.energy += TEC.BaseTEC([
                {'op': 'clearOccupiedGrids',
                 'size': len(applyingAR['possibleSet']),
                 'ARAmout': len(targetNode.state['rules'].AR) - 1}
            ])  # 叠加写地图、清格子的能量（提前）

            targetNode.state['map'].implement(ARType, toSelect)
            if targetNode.state['map'].getEmpty() == set([]):  # 出现一个解
                targetNode.solved = True

            targetNode.state['rules'].AR.pop(ARType)  # 删除应用完的AR
            return [targetNode]
        elif applyingAR['possibleSet'] < toSelect:  # UAR
            animalAmount = applyingAR['amount']
            targetNode.state['rules'].AR.pop(ARType)  # 删除应用完的AR
            self.addStateChilds(targetNode, toSelect, ARType, animalAmount)
            return targetNode.children
        else:  # Grids not enough <=> no solution
            targetNode.state = None

    def solve(self):
        possibleStateQueue = Queue()
        possibleStateQueue.put(self.root)
        solutionCount = 0

        while possibleStateQueue.empty() == False:
            thisState = possibleStateQueue.get()
            thisState.state['rules'].simplifyLib(thisState.state['map'])
            ARTypeToImplement = thisState.state['rules'].chooseRule(thisState.state['map'])
            nextNodes = self.implementAR(thisState, ARTypeToImplement)
            
            for node in nextNodes:
                if node.solved == True:
                    solutionCount += 1
                    node.outputRusult(solutionCount)
                else:
                    possibleStateQueue.put(node)

        if solutionCount == 0:
            print('-'*5 + 'No solution' + '-'*5)
>>>>>>> 424cbd69c565f8452d47fba27c18bb9c4b8013c8
