from StateTree import StateNode
from StateTree import StateTree
from Map import Map
from RuleLibrary import RuleLib
from nose.tools import raises

class Test_Node(object):
  def test_init(self):
    m = Map()
    initRules = [
      {'type': 'tiger', 'amount': 1},
      {'type': 'panda', 'amount': 3},
      {'type': 'hippo', 'amount': 5},
    ]
    RL = RuleLib(initRules)
    root = StateNode(stateMap = m, ruleLib = RL)

    addedRules = [
      {'class': 'AFloor', 'types': ['tiger'], 'param': ['floor3']},
      {'class': 'AFloor', 'types': ['hippo'], 'param': ['floor1']},
      {'class': 'AFloor', 'types': ['panda'], 'param': ['-floor1', '-floor3']}
    ]
    root.ruleLib.addRules(addedRules)
    
    assert root.id == []
    assert root.parent == None
    assert root.children == []
    assert root.ruleLib.AR['panda']['possibleSet'] == set(RuleLib.AR_TABLE['floor2'])

    
class Test_Tree(object):
  def test_solve_blackBox(self):
    m = Map()
    initRules = [
      {'type': 'tiger', 'amount': 1},
      {'type': 'panda', 'amount': 3},
      {'type': 'hippo', 'amount': 5},
    ]
    RL = RuleLib(initRules)
    root = StateNode(stateMap = m, ruleLib = RL)

    addedRules = [
      {'class': 'AFloor', 'types': ['tiger'], 'param': ['floor3']},
      {'class': 'AFloor', 'types': ['hippo'], 'param': ['floor1']},
      {'class': 'AFloor', 'types': ['panda'], 'param': ['-floor1', '-floor3']}
    ]
    root.ruleLib.addRules(addedRules)
    
    tree = StateTree(root)
    tree.solve()

