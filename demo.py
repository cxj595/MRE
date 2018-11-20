from StateTree import StateNode
from StateTree import StateTree
from Map import Map
from RuleLibrary import RuleLib
from StateTree_test import Test_Tree as demoSuite


if __name__ == "__main__":
  demo = demoSuite()
  demo.test_level_1()
  print()
  demo.test_level_10()
  print()
  demo.test_level_33()
  print()
  demo.test_level_50()

