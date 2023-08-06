import unittest

from osaft.solutions.base_scattering import BaseScattering
from osaft.tests.plotting.scattering.setup_test_scattering import (
    BaseTestParticleQuiverPlot,
)
from osaft.tests.solution_factory import SolutionFactory


class TestKingParticleScattering(BaseTestParticleQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "King1934_Particle"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().king_1934_scattering()


class TestYosiokaParticleScattering(BaseTestParticleQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Yosioka_Particle"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().yosioka_1955_scattering()


class TestHasegawaParticleScattering(BaseTestParticleQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Hasegawa1969_Particle"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().hasegawa_1969_scattering()


class TestDoiniRigidParticleScattering(BaseTestParticleQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini1994Rigid_Particle"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_1994_rigid_scattering()


class TestDoiniCompressibleParticleScattering(BaseTestParticleQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini1994Compressible_Particle"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_1994_compressible_scattering()


class TestDoiniViscous2021ParticleScattering(BaseTestParticleQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini2021Viscous_Particle"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_2021_viscous_scattering()


class TestDoiniViscoelastic2021ParticleScattering(BaseTestParticleQuiverPlot):
    def setUp(self):
        super().setUp()
        self.name_prefix = "Doini2021Viscoelastic_Particle"

    def _get_solution(self) -> BaseScattering:
        return SolutionFactory().doinikov_2021_viscoelastic_scattering()


if __name__ == "__main__":
    unittest.main()
