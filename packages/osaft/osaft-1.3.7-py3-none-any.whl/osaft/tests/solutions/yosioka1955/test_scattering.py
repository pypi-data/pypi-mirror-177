import unittest

from osaft.core.functions import BesselFunctions as Bf
from osaft.tests.basetest_numeric import BaseTestSolutions
from osaft.tests.basetest_scattering import (
    HelperCompareScattering,
    HelperScattering,
)
from osaft.tests.solution_factory import SolutionFactory


class TestScattering(BaseTestSolutions, HelperScattering):
    def setUp(self) -> None:

        BaseTestSolutions.setUp(self)

        self.cls = SolutionFactory().yosioka_1955_scattering()

        self.list_cls = [self.cls]

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def A_n(self, n: int) -> complex:

        lamb = self.cls.lambda_rho
        k_f = self.cls.k_f
        k_s = self.cls.k_s
        x_f = self.R_0 * k_f
        x_s = self.R_0 * k_s
        j = lambda x: Bf.besselj(n, x)
        dj = lambda x: Bf.d1_besselj(n, x)
        h = lambda x: Bf.hankelh2(n, x)
        dh = lambda x: Bf.d1_hankelh2(n, x)

        A_num = lamb * k_f * j(x_s) * dj(x_f) - k_s * dj(x_s) * j(x_f)
        A_denom = k_s * dj(x_s) * h(x_f) - lamb * k_f * j(x_s) * dh(x_f)
        A = A_num / A_denom * self.cls.field.A_in(n)

        return A

    def B_n(self, n: int) -> complex:

        lamb = self.cls.lambda_rho
        k_f = self.cls.k_f
        k_s = self.cls.k_s
        x_f = self.cls.x_f
        x_s = self.cls.x_s
        j = lambda x: Bf.besselj(n, x)
        dj = lambda x: Bf.d1_besselj(n, x)
        h = lambda x: Bf.hankelh2(n, x)
        dh = lambda x: Bf.d1_hankelh2(n, x)

        B_num = 1j * k_f
        B_denom = k_s * dj(x_s) * h(x_f)
        B_denom -= lamb * k_f * j(x_s) * dh(x_f)
        B_denom *= x_f**2
        B = B_num / B_denom * self.cls.field.A_in(n)

        return B

    def potential_coefficient(self, n: int) -> complex:
        return -self.A_n(n)

    def V_r_sc(self, n, r):
        A_n = self.cls.A_n(n)
        k_f = self.cls.k_f
        return k_f * A_n * Bf.d1_hankelh2(n, k_f * r)

    def V_theta_sc(self, n, r):
        A_n = self.cls.A_n(n)
        k_f = self.cls.k_f
        return A_n * Bf.hankelh2(n, k_f * r) / r

    def radial_particle_velocity(self, r, theta, t, mode) -> float:
        def radial_func(l, x):
            k = self.cls.k_s
            B = self.cls.B_n(l)
            j = Bf.d1_besselj(l, k * x)
            return B * k * j

        return self.cls.radial_mode_superposition(
            radial_func,
            r,
            theta,
            t,
            mode,
        )

    def tangential_particle_velocity(self, r, theta, t, mode) -> float:
        def radial_func(l, x):
            k = self.cls.k_s
            B = self.cls.B_n(l)
            j = Bf.besselj(l, k * x)
            return B * j / r

        return self.cls.tangential_mode_superposition(
            radial_func,
            r,
            theta,
            t,
            mode,
        )

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_potentials_interface(self) -> None:
        """
        ensures the boundary condition:
        The potential at the particle / fluid - interface is similar.
        """

        def potential_inside(l, x, th, time):
            return self.rho_s * self.cls.Phi_star(x, th, time, l)

        def potential_outside(l, x, th, time):
            return self.rho_f * self.cls.Phi_1(x, th, time, l)

        self.parameters.list_parameters.remove(self.parameters._R_0)
        for n in range(self.n_runs, -1, -1):
            theta = self.get_random_theta()
            t = self.get_random_t()
            self.do_testing(
                func_1=potential_outside,
                args_1=(n, self.R_0, theta, t),
                func_2=potential_inside,
                args_2=(n, self.R_0, theta, t),
            )

    def test_methods_n(self) -> None:
        methods = {}
        methods["A_n"] = None
        methods["B_n"] = None
        methods["potential_coefficient"] = None
        self._test_methods_n(methods, n_end=6, threshold=1e-6)

    def test_V_r_sc(self):
        for n in range(self.n_runs):
            r = self.get_random_r(self.cls)
            self.do_testing(
                func_1=self.cls.V_r_sc,
                args_1=(n, r),
                func_2=self.V_r_sc,
                args_2=(n, r),
            )

    def test_V_theta_sc(self):
        for n in range(self.n_runs):
            r = self.get_random_r(self.cls)
            self.do_testing(
                func_1=self.cls.V_theta_sc,
                args_1=(n, r),
                func_2=self.V_theta_sc,
                args_2=(n, r),
            )


class TestScatteringCompareToKing(BaseTestSolutions, HelperCompareScattering):
    def setUp(self) -> None:

        BaseTestSolutions.setUp(self)

        self._scattering_compare_threshold = 1e-3

        self.parameters.c_s = 1e9 * self.c_f
        self.parameters._c_s.low = 1e9 * self.c_f

        self.cls = SolutionFactory().yosioka_1955_base()

        self.compare_cls = SolutionFactory().king_1934_scattering()

        self.list_cls = [self.cls, self.compare_cls]


if __name__ == "__main__":
    unittest.main()
