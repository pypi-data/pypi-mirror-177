import unittest

import numpy as np
from matplotlib import pyplot as plt

from osaft.plotting.grid import (
    CartesianFluidGrid,
    CartesianGrid,
    CartesianScattererGrid,
)
from osaft.tests.plotting.grid.test_base_grid import plot_grid


class TestCartesianGrid(unittest.TestCase):
    def setUp(self) -> None:
        self.r_max = 2
        self.res_1 = 10
        self.res_2 = 20

        # Grid with the same resolution in both dimensions
        self.grid_1_res = CartesianGrid(
            self.r_max,
            self.res_1,
            False,
            False,
        )

        # Grid with the different resolutions in the two dimensions
        self.grid_2_res = CartesianGrid(
            self.r_max,
            (self.res_1, self.res_2),
            False,
            False,
        )

        # Grid with the same resolution in both dimensions
        self.grid_1_res_upper = CartesianGrid(
            self.r_max,
            self.res_1,
            True,
            False,
        )
        # Grid with the different resolutions in the two dimensions
        self.grid_2_res_upper = CartesianGrid(
            self.r_max,
            (self.res_1, self.res_2),
            True,
            False,
        )

    # -------------------------------------------------------------------------
    # Visual tests (skipped)
    # -------------------------------------------------------------------------

    @unittest.skip("Used only for visual testing during development.")
    def test_plot(self):
        plot_grid(self.grid_1_res)
        plot_grid(self.grid_2_res_upper)
        plot_grid(self.grid_1_res)
        plot_grid(self.grid_2_res_upper)
        plt.show()

    # -------------------------------------------------------------------------
    # Test step size tests
    # -------------------------------------------------------------------------

    def test_dz(self):
        dz = 2 * self.r_max / (self.res_1 - 1)
        self.assertEqual(self.grid_1_res.dz, dz)
        self.assertEqual(self.grid_2_res.dz, dz)

    def test_dx(self):
        dx_1 = 2 * self.r_max / (self.res_1 - 1)
        dx_2 = 2 * self.r_max / (self.res_2 - 1)
        self.assertEqual(self.grid_1_res.dx, dx_1)
        self.assertEqual(self.grid_2_res.dx, dx_2)

        dx_1 = self.r_max / (self.res_1 // 2 - 1)
        dx_2 = self.r_max / (self.res_2 - 1)
        self.assertEqual(self.grid_1_res_upper.dx, dx_1)
        self.assertEqual(self.grid_2_res_upper.dx, dx_2)

    # -------------------------------------------------------------------------
    # Array / resolution tests
    # -------------------------------------------------------------------------

    def test_arr_z(self) -> None:
        arr_z = np.linspace(-self.r_max, self.r_max, self.res_1)
        np.testing.assert_array_equal(self.grid_1_res.arr_z, arr_z)
        np.testing.assert_array_equal(self.grid_2_res.arr_z, arr_z)

    def test_arr_x(self) -> None:
        arr_x_1 = np.linspace(-self.r_max, self.r_max, self.res_1)
        arr_x_2 = np.linspace(-self.r_max, self.r_max, self.res_2)
        np.testing.assert_array_equal(self.grid_1_res.arr_x, arr_x_1)
        np.testing.assert_array_equal(self.grid_2_res.arr_x, arr_x_2)

        arr_x_1 = np.linspace(0, self.r_max, self.res_1 // 2)
        arr_x_2 = np.linspace(0, self.r_max, self.res_2)
        np.testing.assert_array_equal(
            self.grid_1_res_upper.arr_x,
            arr_x_1,
        )
        np.testing.assert_array_equal(
            self.grid_2_res_upper.arr_x,
            arr_x_2,
        )

    # -------------------------------------------------------------------------
    # Test offset
    # -------------------------------------------------------------------------

    def test_offset(self) -> None:
        self.grid_with_offset = CartesianGrid(
            self.r_max,
            5,
            True,
            True,
        )
        self.assertEqual(np.abs(self.grid_with_offset.arr_z).min(), 1e-30)

        self.grid_without_offset = CartesianGrid(
            self.r_max,
            5,
            True,
            False,
        )
        self.assertEqual(np.abs(self.grid_without_offset.arr_z).min(), 0)

    # -------------------------------------------------------------------------
    # Test meshes
    # -------------------------------------------------------------------------

    def test_meshes(self) -> None:

        # Upper = False
        arr_x = self.grid_1_res.arr_x
        arr_z = self.grid_1_res.arr_z
        mesh_z, mesh_x = np.meshgrid(arr_z, arr_x)

        np.testing.assert_array_equal(mesh_x, self.grid_1_res.mesh_x)
        np.testing.assert_array_equal(mesh_z, self.grid_1_res.mesh_z)

        # Upper = True
        arr_x = self.grid_1_res_upper.arr_x
        arr_z = self.grid_1_res_upper.arr_z
        mesh_z, mesh_x = np.meshgrid(arr_z, arr_x)

        np.testing.assert_array_equal(mesh_x, self.grid_1_res_upper.mesh_x)
        np.testing.assert_array_equal(mesh_z, self.grid_1_res_upper.mesh_z)

    # -------------------------------------------------------------------------
    # Test conversions
    # -------------------------------------------------------------------------

    def test_conversion(self) -> None:

        # Upper = False
        mesh_x = self.grid_1_res.mesh_x
        mesh_z = self.grid_1_res.mesh_z

        mesh_r = np.hypot(mesh_x, mesh_z)
        mesh_t = np.arctan2(mesh_x, mesh_z)

        np.testing.assert_array_equal(mesh_r, self.grid_1_res.mesh_r)
        np.testing.assert_array_equal(mesh_t, self.grid_1_res.mesh_theta)

        # Upper = True
        mesh_x = self.grid_2_res_upper.mesh_x
        mesh_z = self.grid_2_res_upper.mesh_z

        mesh_r = np.hypot(mesh_x, mesh_z)
        mesh_t = np.arctan2(mesh_x, mesh_z)

        np.testing.assert_array_equal(mesh_r, self.grid_2_res_upper.mesh_r)
        np.testing.assert_array_equal(mesh_t, self.grid_2_res_upper.mesh_theta)


class TestFluidCartesianGrid(unittest.TestCase):
    def setUp(self) -> None:
        self.r_min = 1
        self.r_max = 2
        self.res_1 = 20
        self.res_2 = 40

        # Grid with the same resolution in both dimensions
        self.grid_1_res = CartesianFluidGrid(
            self.r_min,
            self.r_max,
            self.res_1,
            False,
        )

        # Grid with the different resolutions in the two dimensions
        self.grid_2_res = CartesianFluidGrid(
            self.r_min,
            self.r_max,
            (self.res_1, self.res_2),
            False,
        )

        # Grid with the same resolution in both dimensions
        self.grid_1_res_upper = CartesianFluidGrid(
            self.r_min,
            self.r_max,
            self.res_1,
            True,
        )
        # Grid with the different resolutions in the two dimensions
        self.grid_2_res_upper = CartesianFluidGrid(
            self.r_min,
            self.r_max,
            (self.res_1, self.res_2),
            True,
        )

    @unittest.skip("Used only for visual testing during development.")
    def test_plot(self):
        plot_grid(self.grid_1_res)
        plot_grid(self.grid_2_res_upper)
        plot_grid(self.grid_1_res)
        plot_grid(self.grid_2_res_upper)
        plt.show()

    def test_mask(self):

        self.assertTrue((self.grid_1_res.mesh_r >= self.r_min).all())
        self.assertTrue((self.grid_1_res_upper.mesh_r >= self.r_min).all())
        self.assertTrue((self.grid_2_res.mesh_r >= self.r_min).all())
        self.assertTrue((self.grid_2_res_upper.mesh_r >= self.r_min).all())

        self.assertTrue(
            (
                np.hypot(
                    self.grid_1_res.mesh_x,
                    self.grid_1_res.mesh_z,
                )
                >= self.r_min
            ).all(),
        )
        self.assertTrue(
            (
                np.hypot(
                    self.grid_1_res_upper.mesh_x,
                    self.grid_1_res_upper.mesh_z,
                )
                >= self.r_min
            ).all(),
        )
        self.assertTrue(
            (
                np.hypot(
                    self.grid_2_res.mesh_x,
                    self.grid_2_res.mesh_z,
                )
                >= self.r_min
            ).all(),
        )
        self.assertTrue(
            (
                np.hypot(
                    self.grid_2_res_upper.mesh_x,
                    self.grid_2_res_upper.mesh_z,
                )
                >= self.r_min
            ).all(),
        )


class TestScattererCartesianGrid(unittest.TestCase):
    def setUp(self) -> None:
        self.r_min = 1
        self.r_max = 2
        self.res_1 = 20
        self.res_2 = 40

        # Grid with the same resolution in both dimensions
        self.grid_1_res = CartesianScattererGrid(
            self.r_max,
            self.res_1,
            False,
        )
        # Grid with the different resolutions in the two dimensions
        self.grid_2_res = CartesianScattererGrid(
            self.r_max,
            (self.res_1, self.res_2),
            False,
        )
        # Grid with the same resolution in both dimensions
        self.grid_1_res_upper = CartesianScattererGrid(
            self.r_max,
            self.res_1,
            True,
        )
        # Grid with the different resolutions in the two dimensions
        self.grid_2_res_upper = CartesianScattererGrid(
            self.r_max,
            (self.res_1, self.res_2),
            True,
        )

    @unittest.skip("Used only for visual testing during development.")
    def test_plot(self):
        plot_grid(self.grid_1_res)
        plot_grid(self.grid_2_res_upper)
        plot_grid(self.grid_1_res)
        plot_grid(self.grid_2_res_upper)
        plt.show()

    def test_mask(self):

        self.assertTrue((self.grid_1_res.mesh_r <= self.r_max).all())
        self.assertTrue((self.grid_1_res_upper.mesh_r <= self.r_max).all())
        self.assertTrue((self.grid_2_res.mesh_r <= self.r_max).all())
        self.assertTrue((self.grid_2_res_upper.mesh_r <= self.r_max).all())

        self.assertTrue(
            (
                np.hypot(
                    self.grid_1_res.mesh_x,
                    self.grid_1_res.mesh_z,
                )
                <= self.r_max
            ).all(),
        )
        self.assertTrue(
            (
                np.hypot(
                    self.grid_1_res_upper.mesh_x,
                    self.grid_1_res_upper.mesh_z,
                )
                <= self.r_max
            ).all(),
        )
        self.assertTrue(
            (
                np.hypot(
                    self.grid_2_res.mesh_x,
                    self.grid_2_res.mesh_z,
                )
                <= self.r_max
            ).all(),
        )
        self.assertTrue(
            (
                np.hypot(
                    self.grid_2_res_upper.mesh_x,
                    self.grid_2_res_upper.mesh_z,
                )
                <= self.r_max
            ).all(),
        )


if __name__ == "__main__":
    unittest.main()
