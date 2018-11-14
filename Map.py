# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-14

class Map(object):
  '''
  Property: map(matrix)
  Function:
    getEmpty(self): return the set of empty grids
    implement(self, type, grids): write the map
  '''
  def __init__(self):
    self.map = [['', '', ''], ['', '', ''], ['', '', '']]
  
  def implement(self, animalType, grids):
    '''
    Function: Write Map
    Input: animalType(string), grids(set)
    '''

    for (x, y) in grids:
      if self.map[x][y] == '':
        self.map[x][y] = animalType
      else: #已经有动物
        raise ValueError('Animal conflict')
  
  def getEmpty(self):
    emptySet = set([])
    for x in range(1,4):
      for y in range(1,4):
        if self.map[x][y] == '':
          emptySet |= (x,y)
    
    return emptySet
