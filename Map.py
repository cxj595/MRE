# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-14
import pprint

class Map(object):
  '''
  Property: 
  map(matrix)
  logger = StateNode.logger

  Function:
    getEmpty(self): return the set of empty grids
    implement(self, type, grids): write the map
  '''


  def __init__(self):
    self.map = [['', '', ''], ['', '', ''], ['', '', '']]
    self.logger = None # 与节点链接后由节点提供
  
  
  def implement(self, animalType, grids):
    '''
    Function: Write Map
    Input: animalType(string), grids(set)
    '''

    sizeToWrite = 0
    for (x, y) in grids:
      if self.map[x][y] == '':
        self.map[x][y] = animalType
        sizeToWrite += 1
      else: #已经有动物
        raise RuntimeError('Animal conflict')
    
    self.logger += [{'op': 'writeMap', 'size': sizeToWrite}]


  def findSet(self, target):
    s = set([])
    for i in range(3):
      for j in range(3):
        if self.map[i][j] == target:
          s |= set([(i,j)])
    return s


  def getEmpty(self):
    return self.findSet('')
  
  
  def outputMap(self):
    pprint.pprint(self.map)



