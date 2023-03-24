import unittest
from lfa_project.Test.ColorAveragorTest import ColorAveragorTest
from lfa_project.Test.DeepSearchTest import DeepSearchTest
from lfa_project.Test.FilterOnConditionsTest import FilterOnConditionsTest
from lfa_project.Test.HierarchicalSelectorTest import HierarchicalSelectorTest

if __name__ == '__main__':
        
    allTests = unittest.TestSuite()
    allTests.addTest(unittest.TestLoader().loadTestsFromTestCase(ColorAveragorTest))
    allTests.addTest(unittest.TestLoader().loadTestsFromTestCase(DeepSearchTest))
    allTests.addTest(unittest.TestLoader().loadTestsFromTestCase(FilterOnConditionsTest))
    allTests.addTest(unittest.TestLoader().loadTestsFromTestCase(HierarchicalSelectorTest))

    unittest.TextTestRunner(verbosity=2).run(allTests)

