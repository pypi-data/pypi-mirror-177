from osaft.tests.basetest_numeric import BaseTestSolutions
from osaft.tests.solution_factory import SolutionFactory


class TestScattering(BaseTestSolutions):
    def setUp(self) -> None:
        super().setUp()

        self.cls = SolutionFactory().yosioka_1955_base()

        self.list_cls = [self.cls]

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    @property
    def lambda_rho(self) -> float:
        return self.rho_s / self.rho_f

    @property
    def sigma(self) -> float:
        return self.c_s / self.c_f

    @property
    def x_f(self) -> float:
        return self.R_0 * self.cls.k_f

    @property
    def x_s(self) -> float:
        return self.R_0 * self.cls.k_s

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_properties(self) -> None:
        properties = ["lambda_rho", "sigma", "x_s", "x_f"]
        self._test_properties(properties)
