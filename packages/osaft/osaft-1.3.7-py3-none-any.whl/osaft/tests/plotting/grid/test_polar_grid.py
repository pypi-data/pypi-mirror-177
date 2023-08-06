import unittest

import numpy as np
from matplotlib import pyplot as plt

from osaft.plotting.grid import PolarFluidGrid, PolarGrid, PolarScattererGrid
from osaft.tests.plotting.grid.test_base_grid import plot_grid


class TestPolarGrid(unittest.TestCase):
    def setUp(self) -> None:
        self.r_min = 1
        self.r_max = 2
        self.res_1 = 10
        self.res_2 = 20

        # Grid with the same resolution in both dimensions
        self.grid_1_res = PolarGrid(
            self.r_min,
            self.r_max,
            self.res_1,
            False,
        )
        # Grid with the same resolution in both dimensions from a tuple
        self.grid_1_from_seq_res = PolarGrid(
            self.r_min,
            self.r_max,
            [self.res_1],
            False,
        )
        # Grid with the different resolutions in the two dimensions
        self.grid_2_res = PolarGrid(
            self.r_min,
            self.r_max,
            (self.res_1, self.res_2),
            False,
        )

        # Grid with the same resolution in both dimensions
        self.grid_1_res_upper = PolarGrid(
            self.r_min,
            self.r_max,
            self.res_1,
            True,
        )
        # Grid with the same resolution in both dimensions from a tuple
        self.grid_1_from_seq_res_upper = PolarGrid(
            self.r_min,
            self.r_max,
            [self.res_1],
            True,
        )
        # Grid with the different resolutions in the two dimensions
        self.grid_2_res_upper = PolarGrid(
            self.r_min,
            self.r_max,
            (self.res_1, self.res_2),
            True,
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

    def test_dr(self):
        dr = (self.r_max - self.r_min) / (self.res_1 - 1)
        self.assertAlmostEqual(self.grid_1_res.dr, dr)
        self.assertAlmostEqual(self.grid_1_from_seq_res.dr, dr)
        self.assertAlmostEqual(self.grid_2_res.dr, dr)

    def test_dtheta(self):
        dtheta_1 = 2 * np.pi / (self.res_1 - 1)
        dtheta_2 = 2 * np.pi / (self.res_2 - 1)
        self.assertAlmostEqual(self.grid_1_res.dtheta, dtheta_1)
        self.assertAlmostEqual(self.grid_1_from_seq_res.dtheta, dtheta_1)
        self.assertAlmostEqual(self.grid_2_res.dtheta, dtheta_2)

        dtheta_1_upper = np.pi / (self.res_1 // 2 - 1)
        dtheta_2_upper = np.pi / (self.res_2 - 1)
        self.assertEqual(self.grid_1_res_upper.dtheta, dtheta_1_upper)
        self.assertEqual(self.grid_1_from_seq_res_upper.dtheta, dtheta_1_upper)
        self.assertEqual(self.grid_2_res_upper.dtheta, dtheta_2_upper)

    # -------------------------------------------------------------------------
    # Array / resolution tests
    # -------------------------------------------------------------------------

    def test_arr_r(self) -> None:
        arr_r = np.linspace(self.r_min, self.r_max, self.res_1)
        np.testing.assert_array_equal(self.grid_1_res.arr_r, arr_r)
        np.testing.assert_array_equal(self.grid_1_from_seq_res.arr_r, arr_r)
        np.testing.assert_array_equal(self.grid_2_res.arr_r, arr_r)

    def test_arr_theta(self) -> None:
        arr_theta_1 = np.linspace(-np.pi, np.pi, self.res_1)
        arr_theta_2 = np.linspace(-np.pi, np.pi, self.res_2)
        np.testing.assert_array_equal(self.grid_1_res.arr_theta, arr_theta_1)
        np.testing.assert_array_equal(
            self.grid_1_from_seq_res.arr_theta,
            arr_theta_1,
        )
        np.testing.assert_array_equal(self.grid_2_res.arr_theta, arr_theta_2)

        arr_theta_1_upper = np.linspace(0, np.pi, self.res_1 // 2)
        arr_theta_2_upper = np.linspace(0, np.pi, self.res_2)
        np.testing.assert_array_equal(
            self.grid_1_res_upper.arr_theta,
            arr_theta_1_upper,
        )
        np.testing.assert_array_equal(
            self.grid_1_from_seq_res_upper.arr_theta,
            arr_theta_1_upper,
        )
        np.testing.assert_array_equal(
            self.grid_2_res_upper.arr_theta,
            arr_theta_2_upper,
        )

    # -------------------------------------------------------------------------
    # Test meshes
    # -------------------------------------------------------------------------

    def test_meshes(self) -> None:

        # Upper = False
        arr_r = self.grid_1_res.arr_r
        arr_t = self.grid_1_res.arr_theta
        mesh_t, mesh_r = np.meshgrid(arr_t, arr_r)

        np.testing.assert_array_equal(mesh_r, self.grid_1_res.mesh_r)
        np.testing.assert_array_equal(mesh_t, self.grid_1_res.mesh_theta)

        # Upper = True
        arr_r = self.grid_1_res_upper.arr_r
        arr_t = self.grid_1_res_upper.arr_theta
        mesh_t, mesh_r = np.meshgrid(arr_t, arr_r)

        np.testing.assert_array_equal(mesh_r, self.grid_1_res_upper.mesh_r)
        np.testing.assert_array_equal(mesh_t, self.grid_1_res_upper.mesh_theta)

    # -------------------------------------------------------------------------
    # Test conversions
    # -------------------------------------------------------------------------

    def test_conversion(self) -> None:

        # Upper = False
        mesh_r = self.grid_1_res.mesh_r
        mesh_t = self.grid_1_res.mesh_theta

        mesh_x = mesh_r * np.sin(mesh_t)
        mesh_z = mesh_r * np.cos(mesh_t)

        np.testing.assert_array_equal(mesh_x, self.grid_1_res.mesh_x)
        np.testing.assert_array_equal(mesh_z, self.grid_1_res.mesh_z)

        # Upper = True
        mesh_r = self.grid_1_res_upper.mesh_r
        mesh_t = self.grid_1_res_upper.mesh_theta

        mesh_x = mesh_r * np.sin(mesh_t)
        mesh_z = mesh_r * np.cos(mesh_t)

        np.testing.assert_array_equal(mesh_x, self.grid_1_res_upper.mesh_x)
        np.testing.assert_array_equal(mesh_z, self.grid_1_res_upper.mesh_z)

    def test_polar_scatterer_grid(self) -> None:

        self.scatterer_grid = PolarScattererGrid(1, 10, True)
        self.assertEqual(np.max(self.scatterer_grid.arr_r.min()), 1e-30)
        self.assertEqual(np.max(self.scatterer_grid.arr_r.max()), 1)

    def test_polar_fluid_grid(self) -> None:

        self.scatterer_grid = PolarFluidGrid(1, 2, 10, True)
        self.assertEqual(np.max(self.scatterer_grid.arr_r.min()), 1)
        self.assertEqual(np.max(self.scatterer_grid.arr_r.max()), 2)


if __name__ == "__main__":
    unittest.main()
