import unittest

import numpy as np
from matplotlib import pyplot as plt

from osaft.plotting.grid import BaseGrid, PolarGrid


def plot_grid(grid: BaseGrid) -> None:
    fig, ax = plt.subplots()
    ax.scatter(grid.mesh_z, grid.mesh_x)
    ax.set_aspect("equal")
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    ax.scatter(grid.mesh_theta, grid.mesh_r)


class TestBaseGrid(unittest.TestCase):
    """Testing BaseGrid methods on PolarGrid, since BaseGrid is an ABC"""

    # -------------------------------------------------------------------------
    # Resolution unpacking
    # -------------------------------------------------------------------------

    def test_int_resolution(self) -> None:

        self.grid = PolarGrid(0, 1, 10, False)
        res_x1 = self.grid._res_x1
        res_x2 = self.grid._res_x2
        self.assertEqual(res_x1, 10)
        self.assertEqual(res_x2, 10)

    def test_tuple_resolution(self) -> None:

        self.grid = PolarGrid(0, 1, (10, 20), False)
        res_x1 = self.grid._res_x1
        res_x2 = self.grid._res_x2
        self.assertEqual(res_x1, 10)
        self.assertEqual(res_x2, 20)

    def test_even_int_resolution_upper(self) -> None:

        self.grid = PolarGrid(0, 1, 10, True)
        res_x1 = self.grid._res_x1
        res_x2 = self.grid._res_x2
        self.assertEqual(res_x1, 10)
        self.assertEqual(res_x2, 5)

    def test_odd_int_resolution_upper(self) -> None:

        self.grid = PolarGrid(0, 1, 11, True)
        res_x1 = self.grid._res_x1
        res_x2 = self.grid._res_x2
        self.assertEqual(res_x1, 11)
        self.assertEqual(res_x2, 5)

    def test_ValuerError(self) -> None:
        self.assertRaises(
            ValueError,
            PolarGrid,
            r_min=0,
            r_max=1,
            resolution=3 * [10],
            is_upper=True,
        )

    # -------------------------------------------------------------------------
    # Flatten mesh
    # -------------------------------------------------------------------------

    def test_flatten_mesh(self):

        self.grid = PolarGrid(0, 1, 11, True)
        array = np.random.random((3, 3))
        flat_array = array.flatten()

        self.grid._mesh_r = array
        self.grid._mesh_theta = array
        self.grid._mesh_x = array
        self.grid._mesh_z = array

        np.testing.assert_array_equal(self.grid.flat_mesh_r, flat_array)
        np.testing.assert_array_equal(self.grid.flat_mesh_theta, flat_array)
        np.testing.assert_array_equal(self.grid.flat_mesh_x, flat_array)
        np.testing.assert_array_equal(self.grid.flat_mesh_z, flat_array)


if __name__ == "__main__":
    unittest.main()
