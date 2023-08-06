import unittest

from osaft.solutions.base_scattering import BaseScattering
from osaft.tests.plotting.scattering.setup_test_scattering import (
    BaseTestWireFrameScatterPlotter,
)
from osaft.tests.solution_factory import SolutionFactory


class TestKingWireFrameScattering(BaseTestWireFrameScatterPlotter):
    def setUp(self):
        super().setUp()
        self.name_prefix = "King1934_WireFrame"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().king_1934_scattering()


class TestYosiokaWireFrameScattering(BaseTestWireFrameScatterPlotter):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Yosioka_WireFrame"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().yosioka_1955_scattering()


class TestHasegawaWireFrameScattering(BaseTestWireFrameScatterPlotter):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Hasegawa1969_WireFrame"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().hasegawa_1969_scattering()


class TestDoiniRigidWireFrameScattering(BaseTestWireFrameScatterPlotter):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini1994Rigid_WireFrame"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_1994_rigid_scattering()


class TestDoiniCompressibleWireFrameScattering(
    BaseTestWireFrameScatterPlotter,
):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini1994Compressible_WireFrame"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_1994_compressible_scattering()


class TestDoiniViscous2021WireFrameScattering(BaseTestWireFrameScatterPlotter):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini2021Viscous_WireFrame"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_2021_viscous_scattering()


class TestDoiniViscoelastic2021WireFrameScattering(
    BaseTestWireFrameScatterPlotter,
):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini2021Viscoelastic_WireFrame"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_2021_viscoelastic_scattering()


if __name__ == "__main__":
    unittest.main()
