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
  def test_level_1(self):
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
  
  def test_level_10(self):
    m = Map()
    initRules = [
      {'type': 'elephant', 'amount': 1},
      {'type': 'lion', 'amount': 3},
      {'type': 'hippo', 'amount': 1},
      {'type': 'panda', 'amount': 4},
    ]
    RL = RuleLib(initRules)
    root = StateNode(stateMap = m, ruleLib = RL)

    addedRules = [
      {'class': 'AFloor', 'types': ['elephant'], 'param': ['floor3']},
      {'class': 'RC', 'types': ['lion'], 'param': ['lemon']},
      {'class': 'RC', 'types': ['hippo'], 'param': ['pineapple', 'orange']}
    ]
    root.ruleLib.addRules(addedRules)
    
    tree = StateTree(root)
    tree.solve()
  
  def test_level_33(self):
    m = Map()
    initRules = [
      {'type': 'lion', 'amount': 3},
      {'type': 'panda', 'amount': 3},
      {'type': 'tiger', 'amount': 1},
      {'type': 'cat', 'amount': 1},
      {'type': 'turtle', 'amount': 1},
    ]
    RL = RuleLib(initRules)
    root = StateNode(stateMap = m, ruleLib = RL)

    addedRules = [
      {'class': 'RFloor', 'types': ['tiger', 'cat'], 'param': [1]},
      {'class': 'RC', 'types': ['lion'], 'param': ['-orange', '-strawberry']},
      {'class': 'RC', 'types': ['panda'], 'param': ['-pineapple', '-apple']},
      {'class': 'RC', 'types': ['tiger'], 'param': ['-apple', '-strawberry']}
    ]
    root.ruleLib.addRules(addedRules)
    
    tree = StateTree(root)
    tree.solve()

  def test_level_50(self):
    m = Map()
    initRules = [
      {'type': 'elephant', 'amount': 1},
      {'type': 'monkey', 'amount': 1},
      {'type': 'tiger', 'amount': 1},
      {'type': 'hippo', 'amount': 2},
      {'type': 'lion', 'amount': 2},
      {'type': 'panda', 'amount': 2},
    ]
    RL = RuleLib(initRules)
    root = StateNode(stateMap = m, ruleLib = RL)

    addedRules = [
      {'class': 'Adjacnet', 'types': ['lion', 'monkey']},
      {'class': 'Adjacnet', 'types': ['elephant', 'hippo']},
      {'class': 'Adjacnet', 'types': ['panda', 'tiger']},
      {'class': 'AFloor', 'types': ['lion'], 'param': ['floor2']},
      {'class': 'RC', 'types': ['panda'], 'param': ['-banana']},
      {'class': 'RC', 'types': ['elephant'], 'param': ['-lemon']},
    ]
    root.ruleLib.addRules(addedRules)
    
    tree = StateTree(root)
    tree.solve()
