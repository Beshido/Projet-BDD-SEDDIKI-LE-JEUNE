import unittest
from standard_chase import standard_chase
from constraints import TGD, EGD

class StandardChaseTestCase(unittest.TestCase):

    def test_standard_chase_with_empty_database(self):
        D = []
        sigma = []
        self.assertTrue(standard_chase(D, sigma))

    def test_standard_chase_with_single_TGD_constraint(self):
        D = [('a', 'b'), ('b', 'c')]
        sigma = [TGD(('x',), ('y',), ('a', 'b'), ('b', 'c'))]
        self.assertTrue(standard_chase(D, sigma))

    def test_standard_chase_with_single_EGD_constraint(self):
        D = [('a', 'b'), ('b', 'c')]
        sigma = [EGD(('x', 'y'), ('a', 'b'), ('b', 'c'))]
        self.assertTrue(standard_chase(D, sigma))

    def test_standard_chase_with_TGD_and_EGD_constraints(self):
        D = [('a', 'b'), ('b', 'c'), ('c', 'd')]
        sigma = [
            TGD(('x',), ('y',), ('a', 'b'), ('b', 'c')),
            EGD(('x', 'y'), ('b', 'c'), ('c', 'd'))
        ]
        self.assertTrue(standard_chase(D, sigma))

    def test_standard_chase_with_unsatisfiable_constraint(self):
        D = [('a', 'b')]
        sigma = [TGD(('x',), ('y',), ('a', 'b'), ('b', 'c'))]
        self.assertFalse(standard_chase(D, sigma))

    def test_standard_chase_with_circular_dependency(self):
        D = [('a', 'b'), ('b', 'a')]
        sigma = [TGD(('x',), ('y',), ('a', 'b'), ('b', 'a'))]
        self.assertFalse(standard_chase(D, sigma))

if __name__ == '__main__':
    unittest.main()
