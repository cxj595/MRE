# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-13

from RuleLibrary import RuleLib
from RuleLibrary import RuleError
from nose.tools import raises


def test_Init():
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
  assert expect == RL.AR

def test_AbsoluteRule():
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
  hippoExpect = {'amount': 5, 'possibleSet': set([(1,1), (1,2), (1,3), (2,1), (3,1)])}
  pandaExpect = {'amount': 3, 'possibleSet': set([(2,3), (3,2), (2,2)])}

  assert tigerExpect == RL.AR['tiger']
  assert hippoExpect == RL.AR['hippo']
  assert pandaExpect == RL.AR['panda']

def test_RelativeRules():
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

  assert expectForRight == RL.RR

@raises(RuleError)
def test_ARGridUnderflow():
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
  
  RL.addRules([{'class': 'RC', 'types': ['tiger'], 'param': ['lemon']}])

def testChooseRule():
  pass