# -*- coding: utf8 -*-
from unittest import TestCase

from cluster.method.hierarchical import matrix


class TestHierarchicalPrimitiveData(TestCase):

    def test_matrix(self):
        """
        Tests matrix generation at level 0.

        At level 0 we don't care about the linkage as we don't compare clusters
        yet.

        Using [1, 2, 3, 4, 5] as input data, this should yield the following
        distance matrix:

            │  │ 1 │ 2 │ 3 │ 4 │ 5 │
            ├──┼───┼───┼───┼───┼───┤
            │ 1│   │ 1 │ 2 │ 3 │ 4 │
            │ 2│   │   │ 1 │ 2 │ 3 │
            │ 3│   │   │   │ 1 │ 2 │
            │ 4│   │   │   │   │ 1 │
            │ 5│   │   │   │   │   │

        The diagonal should be ignored, for this use-case.
        """

        data = set([1, 2, 3, 4, 5])
        result = matrix(data)

        # In the result, we expect to have triples. Each triple consists of the
        # two compared elements and the distance. The ordering of the first two
        # elements should not matter, but in this test we *assume* one ordering,
        # to make testing easier.

        expected = {(1, 2, 1),
                    (1, 3, 2),
                    (1, 4, 3),
                    (1, 5, 4),
                    (2, 3, 1),
                    (2, 4, 2),
                    (2, 5, 3),
                    (3, 4, 1),
                    (3, 5, 2),
                    (4, 5, 1)}

        self.assertEqual(result, expected)

    def test_matrix_one_iteration_single_linkage(self):
        """
        Tests clustering using one iteration.

        Using the following input data:

            │   │ 3 │ 5 │ 8 │ 12 │ 18 │
            ├───┼───┼───┼───┼────┼────┤
            │  3│   │ 2 │ 5 │  9 │ 15 │
            │  5│   │   │ 3 │  7 │ 13 │
            │  8│   │   │   │  4 │ 10 │
            │ 12│   │   │   │    │  6 │
            │ 18│   │   │   │    │    │

        We should get the following after one iteration:

            │           │ 3 │ 8, 5 l=3 │ 12 │ 18 │
            ├───────────┼───┼──────────┼────┼────┤
            │  3        │   │    2     │  9 │ 15 │
            │  8, 5 l=3 │   │          │  4 │ 10 │
            │ 12        │   │          │    │  6 │
            │ 18        │   │          │    │    │

        """

        data = [3, 5, 8, 12, 18]
        result = matrix(matrix(data), linkage='single')

        expected = {
            ((3, (8, 5)), 3),
            ((3, 12), 9),
            ((3, 18), 15),
            (((8, 5), 12), 4),
            (((8, 5), 18), 10),
            ((12, 18), 6),
        }

        self.assertTure(result, expected)
