# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-13

import math
import misc
from functools import reduce
from Map import Map
from ThinkingEnergyCost import TEC


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
            raise RuntimeError('RuleError: Possible grids for' + thisType +'not enough.')

      elif rule['class'] == 'Adjacent' or rule['class'] == 'RFloor' or rule['class'] == 'SameRC':
        self.logger.addLog([{'op': 'readRR'}])

        newRR = {}
        newRR['class'] = rule['class']
        newRR['typeA'] = rule['types'][0]
        newRR['typeB'] = rule['types'][1]

        if rule['class'] == 'RFloor':
          newRR['param'] = rule['param'] #相对高度 A-B
        else: # Adjacent or SameRC
          newRR['param'] = True if rule['param'] == 'positive' else False
        
        self.RR.append(newRR)
    
    return ARChanged


  def chooseRule(self, currentMap):
    self.logger.addLog([{'op': 'chooseAR', 'amount': len(self.AR)}])

    entropy = math.inf
    remains = [v['amount'] for v in self.AR.values()]

    for thisType, value in self.AR.items():
      thisAmount = value['amount']
      thisPossible = len(value['possibleSet'] & currentMap.getEmpty())

      if thisAmount == thisPossible: # CAR
        return thisType
      elif thisAmount < thisPossible: # UAR
        thisEntropy = misc.comb(thisPossible, thisAmount) * math.factorial(sum(remains) - thisAmount) \
                                 / (reduce(lambda x, y: x * y, map(math.factorial, remains)) / math.factorial(thisAmount))
        if thisEntropy < entropy:
          entropy = thisEntropy
          resultType = thisType

    return resultType
  

  def removeOccupied(self, mapUpdated):
    #清理所需的能量在StateTree.implement()中提前加过, 因为该能量与待使用AR的格子数有关，此时已经删除
    emptySet = mapUpdated.getEmpty()
    for ar in self.AR.values():
      ar['possibleSet'] &= emptySet
  

  def simplifyLib(self, mapUpdated): # 本函数中与AR有关的能量消耗，在addRules()中计算，此处只计算与RR相关的能量
    self.removeOccupied(mapUpdated)
    
    ARChanged = False
    firstRound = True
    
    while ARChanged  or firstRound:
      ARChanged = False
      firstRound = False

      for rr in self.RR:
        self.logger.addLog([  
          {'op': 'readRR'}, 
          {'op': 'get2AnimalsOfRR'}
          ] + 2 * [ # 有两个RR，故乘以2
          {'op': 'findARFromRR', 'amount': len(self.AR)},
          {'op': 'getARArea'}
          ]) # 共同预处理
        
        if rr['typeA'] not in self.AR.keys() or rr['typeB'] not in self.AR.keys(): #一方已经确定并从AR中一出 -> 另一方AR已经当前最简，RR也没有必要存在
          self.RR.remove(rr)
          continue

        if rr['class'] == 'Adjacent':
          getAdjSet = lambda ij : \
          set(list(filter(lambda xy: 0<=xy[0] and xy[0]<=2 and 0<=xy[1] and xy[1]<=2, \
          [(ij[0]-1,ij[1]),(ij[0]+1, ij[1]), (ij[0],ij[1]-1), (ij[0],ij[1]+1)]))) # Get the Adjacent set of a point

          if rr['param'] == True: #Adjacent
            aPossibleAdj = bPossibleAdj = set()
            for pa in self.AR[rr['typeA']]['possibleSet']:
              aPossibleAdj |= getAdjSet(pa)
            for pb in self.AR[rr['typeB']]['possibleSet']:
              bPossibleAdj |= getAdjSet(pb)
            
            if self.AR[rr['typeA']]['possibleSet'] > bPossibleAdj or self.AR[rr['typeB']]['possibleSet'] > aPossibleAdj:
              ARChanged = True
            self.AR[rr['typeA']]['possibleSet'] &= bPossibleAdj
            self.AR[rr['typeB']]['possibleSet'] &= aPossibleAdj

            self.logger.addLog([
              {'op': 'getPossileAdj', 'size': math.sqrt(len(self.AR[rr['typeA']]['possibleSet']))},
              {'op': 'getPossileAdj', 'size': math.sqrt(len(self.AR[rr['typeB']]['possibleSet']))},
            ])

          elif rr['param'] == False: #Not Adjacent
            aCommonAdj = bCommonAdj = set(self.AR_TABLE['all'])
            for pa in self.AR[rr['typeA']]['possibleSet']:
              aCommonAdj &= getAdjSet(pa)
            for pb in self.AR[rr['typeB']]['possibleSet']:
              bCommonAdj &= getAdjSet(pb)

            if self.AR[rr['typeA']]['possibleSet'] > (set(self.AR_TABLE['all']) - aCommonAdj) or self.AR[rr['typeB']]['possibleSet'] > (set(self.AR_TABLE['all']) - bCommonAdj):
              ARChanged = True
            self.AR[rr['typeA']]['possibleSet'] &= (set(self.AR_TABLE['all']) - aCommonAdj)
            self.AR[rr['typeB']]['possibleSet'] &= (set(self.AR_TABLE['all']) - bCommonAdj)

            self.logger.addLog([
              {'op': 'getCommonAdj', 'size': len(self.AR[rr['typeA']]['possibleSet'])},
              {'op': 'getComplement'},
              {'op': 'getCommonAdj', 'size': len(self.AR[rr['typeB']]['possibleSet'])},
              {'op': 'getComplement'},
            ])

        
        elif rr['class'] == 'RFloor':
          if rr['param'] == [0]: #SameFloor
            getFloor = lambda ij: set([3]) if (ij==(0,2)) else set([2]) if (ij==(0,1) or ij==(1,1) or ij==(1,2)) else set([1])
            getPossibleFLoors = lambda ARType: reduce((lambda s,f: s|f), [getFloor(p) for p in self.AR[ARType]['possibleFloors']])

            aFloors = getPossibleFLoors(rr['typeA'])
            bFloors = getPossibleFLoors(rr['typeB'])
            exceptFloors = set([1,2,3]) - (aFloors & bFloors)
            self.logger.addLog([{'op': 'getFloor'}] * 2)

            for f in exceptFloors:
              ARChanged |= self.addRules([
                {'class': 'AFloor', 'types': [rr['typeA']], 'param': ['-floor' + f]}, 
                {'class': 'AFloor', 'types': [rr['typeB']], 'param': ['-floor' + f]},
              ])

          elif rr['param'] == [1]: # A Higher than B
            ARChanged |= self.addRules([
              {'class': 'AFloor', 'types': [rr['typeA']], 'param': ['-floor1']}, 
              {'class': 'AFloor', 'types': [rr['typeB']], 'param': ['-floor3']}, 
            ])
          
          else:
            raise(RuntimeError('Invalid Rule'))
        
        elif rr['class'] == 'SameRC':
          getRows = lambda dots: reduce(lambda acc,row: acc|row, [set([ij[0]]) for ij in dots])
          getCols = lambda dots: reduce(lambda acc,col: acc|col, [set([ij[1]]) for ij in dots])

          aRows = getRows(self.AR[rr['typeA']['possibleSet']])
          bRows = getRows(self.AR[rr['typeB']['possibleSet']])
          aCols = getCols(self.AR[rr['typeA']['possibleSet']])
          bCols = getCols(self.AR[rr['typeB']['possibleSet']])
          self.logger.addLog([{'op': 'getRC'}] * 4)
          
          if rr['param'] == True: #SameRC
            commonRows = aRows & bRows
            commonCols = aCols & bCols
            self.logger.addLog([{'op': 'getCommonRC'}] * 2)

            for i in commonRows:
              ARChanged |= self.addRules([
                {'class': 'RC', 'types': [rr['typeA']], 'param': ['r'+ i]},
                {'class': 'RC', 'types': [rr['typeB']], 'param': ['r'+ i]},
              ])
            
            for j in commonCols:
              ARChanged |= self.addRules([
                {'class': 'RC', 'types': [rr['typeA']], 'param': ['c'+ j]},
                {'class': 'RC', 'types': [rr['typeB']], 'param': ['c'+ j]},
              ])
          
          else: #DiffRC
            if len(aRows) == 1 ^ len(bRows) == 1: # 当其中一个的行/列惟一，且另一个不唯一，可以将其从另一类中减去，下同；否则不能减去
              multiRowType = rr['typeA'] if len(bRows) == 1 else rr['typeB']
              oneRowNum = aRows.pop() if len(aRows) == 1 else bRows.pop()
              ARChanged |= self.addRules(
                {'class': 'RC', 'types': [multiRowType], 'param': ['-r'+ oneRowNum]}
              )

            if len(aCols) == 1 ^ len(bCols) == 1:
              multiColType = rr['typeA'] if len(bCols) == 1 else rr['typeB']
              oneColNum = aCols.pop() if len(aRows) == 1 else bCols.pop()
              ARChanged |= self.addRules(
                {'class': 'RC', 'types': [multiColType], 'param': ['-c'+ oneColNum]}
              )
            
            self.logger.addLog([{'op': 'checkSingleMultiRC'}] * 2)
