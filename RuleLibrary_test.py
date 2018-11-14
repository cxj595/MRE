# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-13

import unittest
from RuleLibrary import RuleLib
from RuleLibrary import RuleError

class TestRuleLib(unittest.TestCase):
  def testInit(self):
    self.maxDiff = None
    rules = [
      {'type': 'tiger', 'amount': 2},
      {'type': 'panda', 'amount': 3},
      {'type': 'hippo', 'amount': 4},
    ]
    RL = RuleLib(rules)
    expect = {
      'tiger': {'amount': 2, 'possibleSet': set(RuleLib.AR_TABLE['all'])},
      'panda': {'amount': 3, 'possibleSet': set(RuleLib.AR_TABLE['all'])},
      'hippo': {'amount': 4, 'possibleSet': set(RuleLib.AR_TABLE['all'])},
    }
    self.assertEqual(expect, RL.AR)
  
  def testAbsoluteRule(self):
    initRules = [
      {'type': 'tiger', 'amount': 1},
      {'type': 'panda', 'amount': 3},
      {'type': 'hippo', 'amount': 5},
    ]
    RL = RuleLib(initRules)
    addedRules = [
      {'class': 'RC', 'types': ['tiger'], 'param': ['-apple', 'pineapple']},
      {'class': 'AFloor', 'types': ['hippo'], 'param': ['-floor1']},
      {'class': 'RC', 'types': ['panda'], 'param': ['strawberry', 'orange']}
    ]
    RL.addRules(addedRules)
    tigerExpect = {'amount': 1, 'possibleSet': set([(1,1), (2,1)])}
    hippoExpect = {'amount': 5, 'possibleSet': set([(2,2), (2,3), (3, 2), (3,3)])}
    pandaExpect = {'amount': 3, 'possibleSet': set([(1,3)])}
    self.assertEqual(tigerExpect, RL.AR['tiger'])
    self.assertEqual(hippoExpect, RL.AR['hippo'])
    self.assertEqual(pandaExpect, RL.AR['panda'])

  def testRelativeRules(self):
    initRules = [
      {'type': 'tiger', 'amount': 1},
      {'type': 'panda', 'amount': 3},
      {'type': 'hippo', 'amount': 5},
    ]
    RL = RuleLib(initRules)
    
    addedRules = [
      {'class': 'RFloor', 'types':['tiger', 'panda'], 'param': -1},
      {'class': 'SameRC', 'types':['panda', 'hippo'], 'param': 'positive'},
    ]
    RL.addRules(addedRules)
    expectForRight = [
      {'class': 'RFloor', 'typeA': 'tiger', 'typeB': 'panda', 'param': -1},
      {'class': 'SameRC', 'typeA': 'panda', 'typeB': 'hippo', 'param': True},
    ]

    self.assertEqual(expectForRight[0], RL.RR[0])
    self.assertEqual(expectForRight[1], RL.RR[1])
  
  def testARGridUnderflow(self):
    initRules = [
      {'type': 'tiger', 'amount': 1},
      {'type': 'panda', 'amount': 3},
      {'type': 'hippo', 'amount': 5},
    ]
    RL = RuleLib(initRules)
    addedRules = [
      {'class': 'AFloor', 'types': ['tiger'], 'param': ['floor3']},
      {'class': 'AFloor', 'types': ['hippo'], 'param': ['floor1']},
      {'class': 'AFloor', 'types': ['panda'], 'param': ['-floor1', '-floor3']}
    ]
    RL.addRules(addedRules)
    tigerExpect = {'amount': 1, 'possibleSet': set([(3,3)])}
    hippoExpect = {'amount': 5, 'possibleSet': set([(2,3), (3,2), (2,2)])}
    pandaExpect = {'amount': 3, 'possibleSet': set([(1,1), (1,2), (1,3), (2,1), (3,1)])}

    self.assertEqual([tigerExpect, hippoExpect, pandaExpect], RL.AR)
    self.assertRaises(RuleError, RL.addRules, [{'class': 'RC', 'types': ['tiger'], 'param': ['lemon']}])
    pass

  def testChooseRule(self):
    pass