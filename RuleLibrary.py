# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-13

import math
import numpy
import scipy.special as ss
from functools import reduce
from Map import Map

class RuleError(RuntimeError):
  pass

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
    '''
  AR_TABLE = {
    'apple': [(3,x) for x in range(1,4)],
    'lemon': [(2,x) for x in range(1,4)],
    'orange': [(1,x) for x in range(1,4)],
    'pineapple': [(x, 1) for x in range(1,4)],
    'banana': [(x, 2) for x in range(1,4)],
    'strawberry': [(x, 3) for x in range(1,4)],
    'floor1': [(3,1), (2,1), (1,1), (1,2), (1,3)],
    'floor2': [(3,2), (2,2), (2,3)],
    'floor3': [(3,3)],
    'all': [(x,y) for x in range(1,4) for y in range(1,4)]
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
        'class': 'RC'(Row/Col), 'AFloor'(Absulote FLoor), 'Adjacent', 'RFloor'(Relative Floor)
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
            raise RuleError('RuleError: Possible grids for' + thisType +'not enough.')

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
        return {thisType: self.AR[thisType]}
      elif thisAmount < thisPossible: # UAR
        thisEntropy = ss.comb(thisPossible, thisAmount) * math.factorial(sum(remains) - thisAmount) / (reduce(lambda x, y: x * y, map(math.factorial, remains)) / math.factorial(thisAmount))
        if thisEntropy < entropy:
          entropy = thisEntropy
          finalResult = thisType    
      else: # Grids underflow
        raise RuleError('RuleError: Possible grids for' + thisType +'not enough.')
    
    return {finalResult: self.AR[finalResult]}
  
  def simplifyLib(self):
    pass

        

 
