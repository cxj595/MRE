# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-14

# import networkx as nx
# from pprint import pprint as pt
# import matplotlib.pyplot as plt

from Map import Map
import itertools

class StateNode(object):
    '''
    Property:
        id = '':表示分支编码
        children = [], 子树节点, children[someone].id = self.id + index
        parent = None, 指向双亲结点
        state = {'map': , 'AR': , 'RR': }
        isPossible = True
    Funtion:
        __init__
        由StateTree操作数据
    '''

    def __init__(self, state):
        self.state = state
        self.id = ''
        self.children = []
        self.parent = None
        self.isPossible = True

class StateTree(object):
    '''
    Property:
        root: StateNode(id = '')
    Function:
        branch(self, parent, child): 新增状态分支
        try(self, node): 尝试解题
    '''
    def __init__(self, root):
        self.root = root

    def branch(self, currentNode, ARType):
        '''
        Funtion: create new branch when UAR
        Input: currentNode(applying UAR), ARType(lead to UAR)
        **Attention**: Must be UAR
        '''

        applyingAR = currentNode.state['AR'][ARType]
        thisMap = currentNode.state['map']
        toSelect = applyingAR['possibleSet'] & thisMap.getEmpty()
        toSelectAmount = len(toSelect)
        animalAmount = applyingAR['amount']






        

    


