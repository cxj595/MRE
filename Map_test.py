from Map import Map
from nose.tools import raises

def test_init():
  m = Map()
  s = m.getEmpty()
  assert s == set([(i,j) for i in range(3) for j in range(3)])

def test_implement():
  m = Map()
  m.implement('tiger', set([(0,y) for y in range(3)]))
  assert m.map == [
    ['tiger', 'tiger', 'tiger'],
    ['', '', ''],
    ['', '', ''],
  ]

  m.implement('panda', set([(2,0), (2,1)]))
  assert m.map == [
    ['tiger', 'tiger', 'tiger'],
    ['', '', ''],
    ['panda', 'panda', ''],
  ]

@raises(RuntimeError)
def test_implement_conflict():
  m = Map()
  m.implement('tiger', set([(0,y) for y in range(3)]))
  assert m.map == [
    ['tiger', 'tiger', 'tiger'],
    ['', '', ''],
    ['', '', ''],
  ]
  
  m.implement('hippo', set([(0,0)]))