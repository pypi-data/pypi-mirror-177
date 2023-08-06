import unittest

from osaft.core.functions import pi
from osaft.plotting.datacontainers.scattering_datacontainer import (
    FluidScatteringData,
)
from osaft.tests.solution_factory import SolutionFactory


class TestBaseScatteringDatacontainer(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.sol = SolutionFactory().yosioka_1955_scattering()

        self.cls = FluidScatteringData(
            self.sol,
            5 * self.sol.R_0,
        )

    def test_setters_and_getters(self):
        # Change solution
        sol_2 = SolutionFactory().doinikov_1994_rigid_scattering()

        self.cls.sol = sol_2

        # Change r_min
        self.cls.r_min = 2e-6
        self.assertEqual(self.cls.r_min, 2e-6)

        # Change r_max
        self.cls.r_max = 10e-6
        self.assertEqual(self.cls.r_max, 10e-6)

        # Change theta min
        self.cls.theta_min = pi / 4
        self.assertEqual(self.cls.theta_min, pi / 4)

        # Change theta max
        self.cls.theta_max = pi / 2
        self.assertEqual(self.cls.theta_max, pi / 2)

        # Change n_quiver_points
        self.cls.n_quiver_points = 42
        self.assertEqual(self.cls.n_quiver_points, 42)

    def test_change_resolution(self):
        self.cls.resolution = 200
        self.assertEqual(self.cls.grid.res_r, 200)


if __name__ == "__main__":
    unittest.main()
