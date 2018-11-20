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
        print('-'*5 + 'Solution' +
              solutionOrder if solutionOrder != 0 else '' + '-'*5)
        print()
        print('TEC: ' + self.energy)
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
            if targetNode.state['map'].getEmpty == set():  # 出现一个解
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
            thisState['rules'].simplifyRules()
            ARTypeToImplement = thisState['rules'].chooseRule()
            nextNodes = self.implementAR(thisState, ARTypeToImplement)

            thisState.energy += thisState['rules'].TECAcc # 规则化简 + 选择规则 + 规则应用的能量
            thisState['rules'].TECAcc = 0 
            
            for node in nextNodes:
                if node.solved == True:
                    solutionCount += 1
                    node.outputRusult(solutionCount)
                else:
                    possibleStateQueue.put(node)

        if solutionCount == 0:
            print('-'*5 + 'No solution' + '-'*5)
