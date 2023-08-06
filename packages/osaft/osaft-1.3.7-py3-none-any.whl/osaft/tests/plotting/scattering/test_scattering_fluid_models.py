import unittest

from osaft.solutions.base_scattering import BaseScattering
from osaft.tests.plotting.scattering.setup_test_scattering import (
    BaseTestFluidQuiverPlot,
)
from osaft.tests.solution_factory import SolutionFactory


class TestKingFluidScattering(BaseTestFluidQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "King1934_Fluid"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().king_1934_scattering()


class TestYosiokaFluidScattering(BaseTestFluidQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Yosioka_Fluid"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().yosioka_1955_scattering()


class TestHasegawaFluidScattering(BaseTestFluidQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Hasegawa1969_Fluid"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().hasegawa_1969_scattering()


class TestDoiniRigidFluidScattering(BaseTestFluidQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini1994Rigid_Fluid"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_1994_rigid_scattering()


class TestDoiniCompressibleFluidScattering(BaseTestFluidQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini1994Compressible_Fluid"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_1994_compressible_scattering()


class TestDoiniViscous2021FluidScattering(BaseTestFluidQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini2021Viscous_Fluid"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_2021_viscous_scattering()


class TestDoiniViscoelastic2021FluidScattering(BaseTestFluidQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini2021Viscoelastic_Fluid"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_2021_viscoelastic_scattering()


if __name__ == "__main__":
    unittest.main()
