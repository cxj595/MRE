from StateTree_test import Test_Tree as demoSuite


if __name__ == "__main__":
  demo = demoSuite()
  demoCase = 1

  print('Demo ' + str(demoCase))
  demoCase += 1
  demo.test_level_1()

  print('Demo ' + str(demoCase))
  demoCase += 1
  demo.test_level_10()

  print('Demo ' + str(demoCase))
  demoCase += 1
  demo.test_level_33()

  print('Demo ' + str(demoCase))
  demoCase += 1
  demo.test_level_50()

  print('Demo ' + str(demoCase))
  demoCase += 1
  demo.test_custom_level_1()

  print('Demo ' + str(demoCase))
  demoCase += 1
  demo.test_custom_level_2()


  print('Demo ' + str(demoCase))
  demoCase += 1
  demo.test_custom_level_3()
  

