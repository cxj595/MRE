# -*- coding: utf-8 -*-
# @Author: Mio Xie
# @Date  : 2018-11-13

from RuleLibrary import RuleLib
from nose.tools import raises
import StateTree


def test_Init():
  rules = [
    {'type': 'tiger', 'amount': 2},
    {'type': 'panda', 'amount': 3},
    {'type': 'hippo', 'amount': 4},
  ]
  RL = RuleLib(rules)
  expect = {
    'tiger': {'amount': 2, 'possibleSet': set(RL.AR_TABLE['all'])},
    'panda': {'amount': 3, 'possibleSet': set(RL.AR_TABLE['all'])},
    'hippo': {'amount': 4, 'possibleSet': set(RL.AR_TABLE['all'])},
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
  RL.logger = StateTree.StateNode.logger()

  RL.addRules(addedRules)
  tigerExpect = {'amount': 1, 'possibleSet': set([(0,2)])}
  hippoExpect = {'amount': 5, 'possibleSet': set([(0,0), (1,0), (2,0), (2,1), (2,2)])}
  pandaExpect = {'amount': 3, 'possibleSet': set([(0,1), (1,1), (1,2)])}

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
  RL.logger = StateTree.StateNode.logger()
  
  addedRules = [
    {'class': 'RFloor', 'types':['tiger', 'panda'], 'param': 'higher'},
    {'class': 'SameRC', 'types':['panda', 'hippo'], 'param': 'positive'},
  ]
  RL.addRules(addedRules)
  expectForRight = [
    {'class': 'RFloor', 'typeA': 'tiger', 'typeB': 'panda', 'param': 'higher'},
    {'class': 'SameRC', 'typeA': 'panda', 'typeB': 'hippo', 'param': 'positive'},
  ]

  assert expectForRight == RL.RR
