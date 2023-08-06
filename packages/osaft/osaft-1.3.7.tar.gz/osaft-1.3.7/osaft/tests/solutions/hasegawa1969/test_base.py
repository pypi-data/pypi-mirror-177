from osaft.tests.basetest_numeric import BaseTestSolutions
from osaft.tests.solution_factory import SolutionFactory


class TestScattering(BaseTestSolutions):
    def setUp(self) -> None:
        super().setUp()

        self.cls = SolutionFactory().hasegawa_1969_base()

        self.list_cls = [self.cls]

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    @property
    def lambda_rho(self) -> float:
        return self.rho_s / self.rho_f

    @property
    def x_f(self) -> float:
        return self.R_0 * self.cls.k_f

    @property
    def x_s_l(self) -> float:
        return self.R_0 * self.cls.k_s_l

    @property
    def x_s_t(self) -> float:
        return self.R_0 * self.cls.k_s_t

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_properties(self) -> None:
        properties = ["lambda_rho", "x_s_l", "x_s_t", "x_f"]
        self._test_properties(properties)
