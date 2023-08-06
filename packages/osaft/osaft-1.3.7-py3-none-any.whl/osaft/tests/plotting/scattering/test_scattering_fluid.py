import unittest

from osaft.solutions.base_scattering import BaseScattering
from osaft.tests.plotting.scattering.setup_test_scattering import (
    BaseTestFluidPotentialPlotter,
    BaseTestFluidPressurePlotter,
    BaseTestFluidVelocityPlotter,
)
from osaft.tests.solution_factory import SolutionFactory


class TestVelocityField(BaseTestFluidVelocityPlotter):
    def setUp(self) -> None:

        super().setUp()
        self.name_prefix = "Velocity_Plot_Yosioka_"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().yosioka_1955_scattering()


class TestPressureField(BaseTestFluidPressurePlotter):
    def setUp(self) -> None:
        super().setUp()
        self.name_prefix = "Pressure_Plot_Yosioka_"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().yosioka_1955_scattering()


class TestPotentialField(BaseTestFluidPotentialPlotter):
    def setUp(self) -> None:
        super().setUp()
        self.name_prefix = "Potential_Plot_Yosioka_"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().yosioka_1955_scattering()


if __name__ == "__main__":
    unittest.main()
