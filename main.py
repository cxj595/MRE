from StateTree import StateNode
from StateTree import StateTree
from RuleLibrary import RuleLib
from ThinkingEnergyCost import TEC
from Map import Map

def case1():
  RL = RuleLib([
    {'type': 'elephant', 'amount': 1},
    {'type': 'lion', 'amount': 3},
    {'type': 'panda', 'amount': 5},
  ])

  RL.addRules([
    {'class': 'AFloor', 'types': 'elephant',},
    {'class': 'AFloor', 'types': 'lion'}
  ])

  TECTemp = RL.TECAcc
  RL.TECAcc = 0
  root = StateNode({'map': Map(), 'rules': RL}, energy=TECTemp)
  tree = StateTree(root)

