# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-14

import math

class TEC(object):
  kDict = {
    #AR
    'readAR':         1.2,
    'readFloor':      5.0,
    'readNFloor':     6.8,
    'readFruit':      6.5,
    'readNFruit':     9.0,
    'intersectAR':    3.0,
    #Choosing
    'chooseAR':       25.3,
    #Inplement
    'getAnimalAmount':1.0,
    'getSizeofAR':    1.8,
    'writeMap':       8.5,
    'clearOccupiedGrids': 3.5,
    'createBranch':   30.0,
    'selectCombtoTry':4.7,
    'traceBack':      20.0,
    #RR
    'readRR':         1.5,
    'get2AnimalsOfRR':2.5,
    'findARFromRR':   2.0,
    'getARArea':      5.7,
    'getFloor':       6.8,
    'getPossileAdj':  6.5,
    'getCommonAdj':   9.5,
    'getComplement':  4.3,
    'getRC':          5.8,
    'getCommonRC':    1.9,
    'checkSingleMultiRC':12.3, 
  }
  TECFunDict = {
    #AR
    'readAR':         lambda k, s, a: k,
    'readFloor':      lambda k, s, a: k,
    'readNFloor':     lambda k, s, a: k,
    'readFruit':      lambda k, s, a: k,
    'readNFruit':     lambda k, s, a: k,
    'intersectAR':    lambda k, s, a: k * s,
    #Choosing
    'chooseAR':       lambda k, s, a: k * a ** 2,
    #Inplement
    'getAnimalAmount':lambda k, s, a: k,
    'getSizeofAR':    lambda k, s, a: k * math.sqrt(s),
    'writeMap':       lambda k, s, a: k * s,
    'clearOccupiedGrids': lambda k, s, a: k * s * a,
    'createBranch':   lambda k, s, a: k,
    'selectCombtoTry':lambda k, s, a: k,
    'traceBack':      lambda k, s, a: k * s,
    #RR
    'readRR':         lambda k, s, a: k,
    'get2AnimalsOfRR':lambda k, s, a: k,
    'findARFromRR':   lambda k, s, a: k * math.sqrt(a),
    'getARArea':      lambda k, s, a: k,
    'getFloor':       lambda k, s, a: k,
    'getPossileAdj':  lambda k, s, a: k * math.sqrt(s),
    'getCommonAdj':   lambda k, s, a: k * s,
    'getComplement':  lambda k, s, a: k,
    'getRC':          lambda k, s, a: k,
    'getCommonRC':    lambda k, s, a: k,
    'checkSingleMultiRC':lambda k, s, a: k, 
  }

  @staticmethod
  def BaseTEC(params):
    '''
    Funtion: Return the sum of TEC through oprations in param.
    Input: params = [
      {'op': , 'size': , 'amount': },
      ...
    ]
    '''

    TECAcc = 0
    for param in params:
      op = param['op']
      k = TEC.kDict[op]
      TECAcc += TEC.TECFunDict[op](k, param.get('ARSize', 0), param.get('amount', 0))
    return TECAcc