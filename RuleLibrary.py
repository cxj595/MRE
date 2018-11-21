# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-13

import math
import misc
from functools import reduce
from Map import Map
from ThinkingEnergyCost import TEC
from itertools import combinations
from random import choice


class RuleLib(object):
  '''
    Rule Table Sample:
    AR = {
      'animal': {'amount': int, 'possibleSet': set()},
      ...
    }
    RR = [
      {        
        'class' : 'Adjacent'(True/False), 'RFloor' (A-B), 'SameRC'(True/False),
        'typeA':
        'typeB':
        'param' : (optional) A-B
      }
    ]
    logger = StateNode.logger

    Funtions:
    __init__()
    addRules() -> Garantee AR与animal一对一
    chooseRule()
    removeOccupiedGrids()
    simplifyLib()
    '''


  AR_TABLE = {
    'apple': [(0,j) for j in range(3)],
    'lemon': [(1,j) for j in range(3)],
    'orange': [(2,j) for j in range(3)],
    'pineapple': [(i, 0) for i in range(3)],
    'banana': [(i, 1) for i in range(3)],
    'strawberry': [(i, 2) for i in range(3)],
    'floor1': [(0,0), (1,0), (2,0), (2,1), (2,2)],
    'floor2': [(0,1), (1,1), (1,2)],
    'floor3': [(0,2)],

    'r0': [(0,j) for j in range(3)],
    'r1': [(1,j) for j in range(3)],
    'r2': [(2,j) for j in range(3)],
    'c0': [(i, 0) for i in range(3)],
    'c1': [(i, 1) for i in range(3)],
    'c2': [(i, 2) for i in range(3)],
    'all': [(i,j) for i in range(3) for j in range(3)]
  }


  def __init__(self, Animals):
    '''
    Function: create init AR wih full grids
    Input: Animal list[
      {'type': , 'amount': } <- Please GARANTEE sum of amount = 9
      ...
    ]
    '''
    self.AR = {}
    self.RR = []
    for a in Animals:
      self.AR[a['type']] = {}
      self.AR[a['type']]['amount'] = a['amount']
      self.AR[a['type']]['possibleSet'] = set(RuleLib.AR_TABLE['all']) # Full grids
    self.logger = None # 与节点链接后由节点提供
   

  def addRules(self, newRules):
    '''
    Function: Parse & Add AR/RR
    Input: newRules[
      {
        'class': 'RC'(Row/Col), 'SameRC', 'AFloor'(Absulote FLoor), 'Adjacent', 'RFloor'(Relative Floor)
        'types': [], 1 or 2 animals
        'param': [], defined by class
      }
    ]
    Return: AR changed? True/ False
    '''

    ARChanged = False

    for rule in newRules:
      if rule['class'] == 'RC' or rule['class'] == 'AFloor':
        self.logger.addLog([{'op': 'readAR'}])

        thisType = rule['types'][0]
        for param in rule['param']:
          if param[0] == '-': #排除
            subset = set(RuleLib.AR_TABLE['all']) - set(RuleLib.AR_TABLE[param[1:]])
            self.logger.addLog([{'op': 'readNFruit' if rule['class'] == 'RC' else 'readNFloor'}])

          else: #指定
            subset = set(RuleLib.AR_TABLE[param])
            self.logger.addLog([{'op': 'readFruit' if rule['class'] == 'RC' else 'readFloor'}])

          if len(self.AR[thisType]['possibleSet'] & subset) >= self.AR[thisType]['amount']: # Possible grids enough
            if self.AR[thisType]['possibleSet'] > subset: # 交集能够使AR缩减
              ARChanged = True

            self.AR[thisType]['possibleSet'] &= subset
            self.logger.addLog([{'op': 'intersectAR', 'size': len(subset)}]) # 公共AR操作
          else: #Possible grids not enough
            raise RuntimeError('RuleError: Possible grids for ' + thisType +' not enough.')

      elif rule['class'] == 'Adjacent' or rule['class'] == 'RFloor' or rule['class'] == 'SameRC':
        self.logger.addLog([{'op': 'readRR'}])

        newRR = {}
        newRR['class'] = rule['class']
        newRR['typeA'] = rule['types'][0]
        newRR['typeB'] = rule['types'][1]
        newRR['param'] = rule['param']

        
        self.RR.append(newRR)
      
      else:
        raise RuntimeError("Rule Error: cannot recognize this rule.")
    
    return ARChanged


  def chooseRule(self, currentMap):
    self.logger.addLog([{'op': 'chooseAR', 'amount': len(self.AR)}])

    entropy = math.inf
    remains = [v['amount'] for v in self.AR.values()]
    resultTypes = []

    for thisType, value in self.AR.items():
      thisAmount = value['amount']
      thisPossible = len(value['possibleSet'] & currentMap.getEmpty())

      if thisAmount == thisPossible: # CAR
        return thisType

      elif thisAmount < thisPossible: # UAR
        thisEntropy = misc.comb(thisPossible, thisAmount) * math.factorial(sum(remains) - thisAmount) \
                                 / (reduce(lambda x, y: x * y, map(math.factorial, remains)) / math.factorial(thisAmount))
        if thisEntropy < entropy: # 当前唯一最优UAR选择
          entropy = thisEntropy
          resultTypes = [thisType]
        elif thisEntropy == entropy: # 最优UAR选择之一
          resultTypes.append(thisType)

      else: #thisAmount > thisPossible，本状态出现无解，应当返回该种类，在 StateTree.implementAR() 里尽早剪枝
        return thisType

    return choice(resultTypes) # 没有无解的种类 <=> 本状态有解 <=> 返回解（之一）
  

  def removeOccupied(self, mapUpdated):
    #清理所需的能量在StateTree.implement()中提前加过, 因为该能量与待使用AR的格子数有关，此时已经删除
    emptySet = mapUpdated.getEmpty()
    for ar in self.AR.values():
      ar['possibleSet'] &= emptySet
  

  def simplifyLib(self, mapUpdated): # 本函数中与AR有关的能量消耗，在addRules()中计算，此处只计算与RR相关的能量
    self.removeOccupied(mapUpdated)

    getRelativeRRIndexs = lambda thisType: set(filter(lambda x: self.RR[x]['typeA'] == thisType or self.RR[x]['typeB'] == thisType, \
                                                      [i for i in range(len(self.RR))]))
    toSimplifyIndexs = set([i for i in range(len(self.RR))])

    while toSimplifyIndexs != set():
      rr = self.RR[toSimplifyIndexs.pop()]
      
      self.logger.addLog([  
        {'op': 'readRR'}, 
        {'op': 'get2AnimalsOfRR'}
        ] + 2 * [ # 有两个RR，故乘以2
        {'op': 'findARFromRR', 'amount': len(self.AR)},
        {'op': 'getARArea'}
        ]) # 共同预处理
      
      if rr['typeA'] not in self.AR.keys() or rr['typeB'] not in self.AR.keys(): #一方已经确定并从AR中一出 -> 另一方AR已经当前最简，RR也没有必要存在
        removedIndex = self.RR.index(rr)
        self.RR.remove(rr)
        toSimplifyIndexs = set(map(lambda i: i-1 if i>removedIndex else i, toSimplifyIndexs))
        continue

      if rr['class'] == 'Adjacent':
        availableGrids = mapUpdated.getEmpty()
        getAvailableAdjSet = lambda ij : \
        set(list(filter(lambda xy: 0<=xy[0] and xy[0]<=2 and 0<=xy[1] and xy[1]<=2 and (xy[0], xy[1]) in availableGrids, \
        [(ij[0]-1,ij[1]),(ij[0]+1, ij[1]), (ij[0],ij[1]-1), (ij[0],ij[1]+1)]))) # Get the Adjacent set of a point

        if rr['param'] == 'positive': #Adjacent
          aPossibleAdj = set()
          bPossibleAdj = set()

          for thisType in ['typeA', 'typeB']:
            possibleAdj = aPossibleAdj if thisType == 'typeA' else bPossibleAdj
            for possibleComb in combinations(self.AR[rr[thisType]]['possibleSet'], self.AR[rr[thisType]]['amount']): #对于每一个可能的AR组合
              combCommonAdj = set(self.AR_TABLE['all'])
              for p in possibleComb:
                combCommonAdj &= getAvailableAdjSet(p)
              possibleAdj |= combCommonAdj
          
          if self.AR[rr['typeA']]['possibleSet'] > bPossibleAdj:
            toSimplifyIndexs |= getRelativeRRIndexs(rr['typeA'])
          if self.AR[rr['typeB']]['possibleSet'] > aPossibleAdj:
            toSimplifyIndexs |= getRelativeRRIndexs(rr['typeB'])

          self.AR[rr['typeA']]['possibleSet'] &= bPossibleAdj
          self.AR[rr['typeB']]['possibleSet'] &= aPossibleAdj

          self.logger.addLog([
            {'op': 'getPossileAdj', 'size': math.sqrt(len(self.AR[rr['typeA']]['possibleSet']))},
            {'op': 'getPossileAdj', 'size': math.sqrt(len(self.AR[rr['typeB']]['possibleSet']))},
          ])

        elif rr['param'] == 'negative': #Not Adjacent
          aPossibleNAdj = set()
          bPossibleNAdj = set()

          for thisType in ['typeA', 'typeB']:
            possibleNAdj = aPossibleNAdj if thisType == 'typeA' else bPossibleNAdj
            for possibleComb in combinations(self.AR[rr[thisType]]['possibleSet'], self.AR[rr[thisType]]['amount']): #对于每一个可能的AR组合
              combCommonNAdj = set(self.AR_TABLE['all'])
              for p in possibleComb:
                combCommonNAdj &= (self.AR_TABLE['all'] - getAvailableAdjSet(p))
              possibleNAdj |= combCommonNAdj

          if self.AR[rr['typeA']]['possibleSet'] > bPossibleNAdj:
            toSimplifyIndexs |= getRelativeRRIndexs(rr['typeA'])
            toSimplifyIndexs |= getRelativeRRIndexs(rr['typeB'])

          self.AR[rr['typeA']]['possibleSet'] &= bPossibleAdj
          self.AR[rr['typeB']]['possibleSet'] &= aPossibleAdj

          self.logger.addLog([
            {'op': 'getPossileNAdj', 'size': len(self.AR[rr['typeA']]['possibleSet'])},
            {'op': 'getComplement'},
            {'op': 'getPossileNAdj', 'size': len(self.AR[rr['typeB']]['possibleSet'])},
            {'op': 'getComplement'},
          ])

        else: # 参数分支
          raise(RuntimeError('Invalid Rule'))

      
      elif rr['class'] == 'RFloor':
        if rr['param'] == 'same': #SameFloor
          getFloor = lambda ij: set([3]) if (ij==(0,2)) else set([2]) if (ij==(0,1) or ij==(1,1) or ij==(1,2)) else set([1])
          getPossibleFLoors = lambda ARType: reduce((lambda s,f: s|f), [getFloor(p) for p in self.AR[ARType]['possibleFloors']])

          aFloors = getPossibleFLoors(rr['typeA'])
          bFloors = getPossibleFLoors(rr['typeB'])
          exceptFloors = set([1,2,3]) - (aFloors & bFloors)
          self.logger.addLog([{'op': 'getFloor'}] * 2)

          for f in exceptFloors:
            if self.addRules([{'class': 'AFloor', 'types': [rr['typeA']], 'param': ['-floor' + f]}]) == True: 
              toSimplifyIndexs |= getRelativeRRIndexs(rr['typeA'])
            if self.addRules([{'class': 'AFloor', 'types': [rr['typeB']], 'param': ['-floor' + f]}]) == True:
              toSimplifyIndexs |= getRelativeRRIndexs(rr['typeB'])

        elif rr['param'] == 'higher': # A Higher than B
          if self.addRules([{'class': 'AFloor', 'types': [rr['typeA']], 'param': ['-floor1']}]) == True:
            toSimplifyIndexs |= getRelativeRRIndexs(rr['typeA'])
          if self.addRules([{'class': 'AFloor', 'types': [rr['typeB']], 'param': ['-floor3']}]) == True:
            toSimplifyIndexs |= getRelativeRRIndexs(rr['typeB'])
        
        else: # 参数分支
          raise(RuntimeError('Invalid Rule'))
      
      elif rr['class'] == 'SameRC':
        getRows = lambda dots: reduce(lambda acc,row: acc|row, [set([ij[0]]) for ij in dots])
        getCols = lambda dots: reduce(lambda acc,col: acc|col, [set([ij[1]]) for ij in dots])

        aRows = getRows(self.AR[rr['typeA']['possibleSet']])
        bRows = getRows(self.AR[rr['typeB']['possibleSet']])
        aCols = getCols(self.AR[rr['typeA']['possibleSet']])
        bCols = getCols(self.AR[rr['typeB']['possibleSet']])
        self.logger.addLog([{'op': 'getRC'}] * 4)
        
        if rr['param'] == 'positive': #SameRC
          commonRows = aRows & bRows
          commonCols = aCols & bCols
          self.logger.addLog([{'op': 'getCommonRC'}] * 2)

          for i in commonRows:
            if self.addRules([{'class': 'RC', 'types': [rr['typeA']], 'param': ['r'+ i]}]) == True:
              toSimplifyIndexs |= getRelativeRRIndexs(rr['typeA'])
            if self.addRules([{'class': 'RC', 'types': [rr['typeB']], 'param': ['r'+ i]}]) == True:
              toSimplifyIndexs |= getRelativeRRIndexs(rr['typeB'])
          
          for j in commonCols:
            if self.addRules([{'class': 'RC', 'types': [rr['typeA']], 'param': ['c'+ j]}]) == True:
              toSimplifyIndexs |= getRelativeRRIndexs(rr['typeA'])
            if self.addRules([{'class': 'RC', 'types': [rr['typeB']], 'param': ['c'+ j]}]) == True:
              toSimplifyIndexs |= getRelativeRRIndexs(rr['typeB'])

        
        elif rr['param'] == 'negative': #DiffRC
          if len(aRows) == 1 ^ len(bRows) == 1: # 当其中一个的行/列惟一，且另一个不唯一，可以将其从另一类中减去，下同；否则不能减去
            multiRowType = rr['typeA'] if len(bRows) == 1 else rr['typeB']
            oneRowNum = aRows.pop() if len(aRows) == 1 else bRows.pop()
            if self.addRules([{'class': 'RC', 'types': [multiRowType], 'param': ['-r'+ oneRowNum]}]) == True:
              toSimplifyIndexs |= getRelativeRRIndexs(multiRowType)


          if len(aCols) == 1 ^ len(bCols) == 1:
            multiColType = rr['typeA'] if len(bCols) == 1 else rr['typeB']
            oneColNum = aCols.pop() if len(aRows) == 1 else bCols.pop()
            if self.addRules([{'class': 'RC', 'types': [multiColType], 'param': ['-c'+ oneColNum]}]) == True:
              toSimplifyIndexs |= getRelativeRRIndexs(rr[multiColType])

          self.logger.addLog([{'op': 'checkSingleMultiRC'}] * 2)
        
        else: #参数分支
          raise(RuntimeError('Invalid Rule'))

      else: #种类分支
        raise(RuntimeError('Invalid Rule'))
