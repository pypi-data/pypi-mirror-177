from osaft import WaveType
from osaft.tests.basetest_numeric import BaseTestSolutions
from osaft.tests.solution_factory import SolutionFactory


class TestCompareSettnesStanding(BaseTestSolutions):
    def setUp(self):
        super().setUp()

        self.parameters.wave_type = WaveType.STANDING

        # Viscosity
        self.arf_compare_threshold = 10e-1
        self.small_boundary_layer = False
        self.large_boundary_layer = False

        # Viscosity
        self.parameters.eta_s = 1e-3
        self.parameters.zeta_s = 0
        self.parameters.zeta_f = 0
        self.parameters.eta_f = 1e-4
        self.parameters.R_0 = 5e-6

        # Frequency
        self.parameters.f = 2e6

        # Density
        self.parameters.rho_s = 2500

        self.cls = SolutionFactory().doinikov_1994_compressible_arf()

        self.compare_cls = SolutionFactory().settnes_2012_arf()

        self.list_cls = [self.cls, self.compare_cls]

    def test_comparison_arf(self):
        self.assertAlmostEqual(self.cls.compute_arf(), self.cls.compute_arf())


if __name__ == "__main__":
    pass
