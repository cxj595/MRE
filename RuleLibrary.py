# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-13

import math
import misc
from functools import reduce
from Map import Map


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
    for rule in newRules:
      if rule['class'] == 'RC' or rule['class'] == 'AFloor':
        thisType = rule['types'][0]
        for param in rule['param']:
          if param[0] == '-':
            subset = set(RuleLib.AR_TABLE['all']) - set(RuleLib.AR_TABLE[param[1:]])
          else: #指定
            subset = set(RuleLib.AR_TABLE[param])
          
          if len(self.AR[thisType]['possibleSet'] & subset) >= self.AR[thisType]['amount']: # Possible grids enough
            self.AR[thisType]['possibleSet'] &= subset
          else: #Possible grids not enough
            raise RuntimeError('RuleError: Possible grids for' + thisType +'not enough.')

      elif rule['class'] == 'Adjacent' or rule['class'] == 'RFloor' or rule['class'] == 'SameRC':
        newRR = {}
        newRR['class'] = rule['class']
        newRR['typeA'] = rule['types'][0]
        newRR['typeB'] = rule['types'][1]
        if rule['class'] == 'RFloor':
          newRR['param'] = rule['param'] #相对高度 A-B
        else: # Adjacent or SameRC
          newRR['param'] = True if rule['param'] == 'positive' else False
        
        self.RR.append(newRR)


  def chooseRule(self, currentMap):
    entropy = math.inf
    remains = [i for i in self.AR.values()['amount']]

    for thisType, value in self.AR.items():
      thisAmount = value['amount']
      thisPossible = len(value['possibleSet'] & currentMap.getEmpty())

      if thisAmount == thisPossible: # CAR
        return thisType
      elif thisAmount < thisPossible: # UAR
        thisEntropy = misc.comb(thisPossible, thisAmount) * math.factorial(sum(remains) - thisAmount) / (reduce(lambda x, y: x * y, map(math.factorial, remains)) / math.factorial(thisAmount))
        if thisEntropy < entropy:
          entropy = thisEntropy
          finalResult = thisType

    return finalResult
  

  def removeOccupied(self, mapUpdated):
    emptySet = mapUpdated.getEmpty()
    for ar in self.AR.values():
      ar['possibleSet'] &= emptySet
  

  def simplifyLib(self, mapUpdated):
    self.removeOccupied(mapUpdated)
    for rr in self.RR:
      if rr['class'] == 'Adjacent':
        getAdjSet = lambda ij : \
        set(list(filter(lambda xy: 0<=xy[0] and xy[0]<=2 and 0<=xy[1] and xy[1]<=2, \
        [(ij[0]-1,ij[1]),(ij[0]+1, ij[1]), (ij[0],ij[1]-1), (ij[0],ij[1]+1)]))) # Get the Adjacent set of a point

        if rr['param'] == True: #Adjacent
          aAdj = bAdj = set()
          for pa in self.AR[rr['TypeA']]['possibleSet']:
            aAdj |= getAdjSet(pa)
          for pb in self.AR[rr['TypeB']]['possibleSet']:
            bAdj |= getAdjSet(pb)
          
          self.AR[rr['TypeA']]['possibleSet'] &= bAdj
          self.AR[rr['TypeB']]['possibleSet'] &= aAdj

        elif rr['param'] == False: #Not Adjacent
          aNAdj = bNAdj = set(self.AR_TABLE['all'])
          for pa in self.AR[rr['TypeA']]['possibleSet']:
            aNAdj -= getAdjSet(pa)
          bAdj = set()
          for pb in self.AR[rr['TypeB']]['possibleSet']:
            bNAdj -= getAdjSet(pb)

          self.AR[rr['TypeA']]['possibleSet'] &= bNAdj
          self.AR[rr['TypeB']]['possibleSet'] &= aNAdj
      
      elif rr['class'] == 'RFloor':
        if rr['param'] == 0: #SameFloor
          getFloor = lambda ij: set([3]) if (ij==(0,2)) else set([2]) if (ij==(0,1) or ij==(1,1) or ij==(1,2)) else set([1])
          getPossibleFLoors = lambda ARType: reduce((lambda s,f: s|f), [getFloor(p) for p in self.AR[ARType]['possibleFloors']])

          aFloors = getPossibleFLoors(rr['TypeA'])
          bFloors = getPossibleFLoors(rr['TypeB'])
          exceptFloor = set([1,2,3]) - (aFloors & bFloors)

          for f in exceptFloor:
            self.addRules([
              {'class': 'AFloor', 'types': [rr['TypeA']], 'param': '-floor' + f}, 
              {'class': 'AFloor', 'types': [rr['TypeB']], 'param': '-floor' + f},
            ])

        elif rr['param'] == 1: # A Higher than B
          self.addRules([
            {'class': 'AFloor', 'types': [rr['TypeA']], 'param': '-floor1'}, 
            {'class': 'AFloor', 'types': [rr['TypeB']], 'param': '-floor3'}, 
          ])
        
        else:
          raise(RuntimeError('Invalid Rule'))
      
      elif rr['class'] == 'SameRC':
        getRows = lambda dots: reduce(lambda acc,row: acc|row, [set([ij[0]]) for ij in dots])
        getCols = lambda dots: reduce(lambda acc,col: acc|col, [set([ij[1]]) for ij in dots])

        aRows = getRows(self.AR[rr['TypeA']['possibleSet']])
        bRows = getRows(self.AR[rr['TypeB']['possibleSet']])
        aCols = getCols(self.AR[rr['TypeA']['possibleSet']])
        bCols = getCols(self.AR[rr['TypeB']['possibleSet']])
        
        if rr['param'] == True: #SameRC
          commonRows = aRows & bRows
          commonCols = aCols & bCols

          for i in commonRows:
            self.addRules([
              {'class': 'RC', 'types': [rr['TypeA']], 'param': 'r'+ i},
              {'class': 'RC', 'types': [rr['TypeB']], 'param': 'r'+ i},
            ])
          
          for j in commonCols:
            self.addRules([
              {'class': 'RC', 'types': [rr['TypeA']], 'param': 'c'+ j},
              {'class': 'RC', 'types': [rr['TypeB']], 'param': 'c'+ j},
            ])
        
        else: #DiffRC
          if len(aRows) == 1 ^ len(bRows) == 1: # 当其中一个的行/列惟一，且另一个不唯一，可以将其从另一类中减去，下同；否则不能减去
            multiRowType = rr['TypeA'] if len(bRows) == 1 else rr['TypeB']
            oneRowNum = aRows.pop() if len(aRows) == 1 else bRows.pop()
            self.addRules(
              {'class': 'RC', 'types': [multiRowType], 'param': '-r'+ oneRowNum}
            )

          if len(aCols) == 1 ^ len(bCols) == 1:
            multiColType = rr['TypeA'] if len(bCols) == 1 else rr['TypeB']
            oneColNum = aCols.pop() if len(aRows) == 1 else bCols.pop()
            self.addRules(
              {'class': 'RC', 'types': [multiColType], 'param': '-c'+ oneColNum}
            )



        

 
