import unittest

from osaft.core.functions import BesselFunctions as Bf
from osaft.core.functions import cos, exp, sin
from osaft.tests.basetest_scattering import (
    HelperCompareScattering,
    HelperScattering,
)
from osaft.tests.solution_factory import SolutionFactory
from osaft.tests.solutions.basedoinikov1994.test_base import (
    BaseTestDoinikov1994,
    TestBaseDoinikov1994,
)


class TestScattering(BaseTestDoinikov1994, HelperScattering):
    def setUp(self) -> None:
        super().setUp()

        self._v_particle_threshold = 1e-5
        self._v_fluid_threshold = 1e-3
        self._v_boundary_conditions = 1e-6

        self.cls = SolutionFactory().doinikov_1994_rigid_scattering()

    def V_r_sc(self, n, r) -> complex:
        # grad(phi)
        out = self.cls.k_f * self.alpha_n(n)
        out *= Bf.d1_hankelh1(n, self.cls.k_f * r)
        # curl(Psi)
        tmp = n * (n + 1) / r * self.beta_n(n)
        tmp *= Bf.hankelh1(n, self.cls.k_v * r)

        out -= tmp

        out *= self.cls.A_in(n)
        return out

    def V_theta_sc(self, n, r) -> complex:
        # curl(Psi)
        arg_v = self.cls.k_v * r
        out = Bf.hankelh1(n, arg_v)
        out += arg_v * Bf.d1_hankelh1(n, arg_v)
        out *= -self.beta_n(n)
        # grad(phi)
        out += self.alpha_n(n) * Bf.hankelh1(n, self.cls.k_f * r)

        out *= self.cls.A_in(n) / r
        return out

    # ------------------

    def radial_particle_velocity(self, r, theta, t, mode):
        if mode == 1 or mode is None:
            return self.particle_velocity(t) * cos(theta)
        else:
            return 0

    def tangential_particle_velocity(self, r, theta, t, mode):
        if mode == 1 or mode is None:
            return -self.particle_velocity(t) * sin(theta)
        else:
            return 0

    def particle_velocity(self, t):

        out = Bf.besselj(1, self.x)
        out += self.alpha_n(1) * Bf.hankelh1(1, self.x)
        out -= 2 * self.beta_n(1) * Bf.hankelh1(1, self.x_v)

        out *= self.cls.A_in(1) * self.cls.k_f * self.rho_t
        out /= self.x

        out *= exp(-1j * self.cls.omega * t)

        return out

    # ------------------
    # generic tests
    # ------------------

    def test_properties(self) -> None:
        properties = ["rho_t", "mu_1", "mu_2", "mu_3", "mu_4"]
        self._test_properties(properties)

    def test_methods_n(self) -> None:
        methods = {}
        methods["alpha_n"] = None
        methods["beta_n"] = None
        methods["xi_n"] = None
        methods["gamma_n"] = None
        methods["potential_coefficient"] = None

        self._test_methods_n(methods, threshold=1e-10)

    # ------------------

    def alpha_n(self, n: int) -> complex:
        if n > 1:
            out = n * (n + 1)
            out *= Bf.besselj(n, self.x) * Bf.hankelh1(n, self.x_v)

            out -= self.x * self.gamma_n(n) * Bf.d1_besselj(n, self.x)

            out /= self.xi_n(n)

        elif n > 0:
            out = -2 * (1 - self.rho_t) ** 2 * Bf.besselj(1, self.x)
            out *= Bf.hankelh1(1, self.x_v)

            out -= self.mu_1 * self.mu_3
            out /= self.mu_4

        else:
            out = -Bf.besselj(1, self.x) / Bf.hankelh1(1, self.x)

        return out

    def beta_n(self, n: int) -> complex:
        if n > 1:
            out = Bf.d1_besselj(n, self.x) * Bf.hankelh1(n, self.x)
            out -= Bf.besselj(n, self.x) * Bf.d1_hankelh1(n, self.x)
            out *= -self.x / self.xi_n(n)
        elif n > 0:
            out = self.mu_1 * Bf.hankelh1(1, self.x)
            out -= self.mu_2 * Bf.besselj(1, self.x)
            out *= -(1 - self.rho_t) / self.mu_4
        else:
            out = 0

        return out

    def potential_coefficient(self, n: int) -> complex:
        return self.cls.alpha_n(n) * self.cls.field.A_in(n)

    def xi_n(self, n: int) -> complex:
        out = -n * (n + 1)
        out *= Bf.hankelh1(n, self.x)
        out *= Bf.hankelh1(n, self.x_v)

        out += self.x * Bf.d1_hankelh1(n, self.x) * self.gamma_n(n)

        return out

    def gamma_n(self, n: int) -> complex:
        out = self.x_v * Bf.d1_hankelh1(n, self.x_v)
        out += Bf.hankelh1(n, self.x_v)
        return out

    # ------------------

    @property
    def mu_1(self) -> complex:
        out = -self.x * Bf.d1_besselj(1, self.x)
        out += self.rho_t * Bf.besselj(1, self.x)
        return out

    @property
    def mu_2(self) -> complex:
        out = -self.x * Bf.d1_hankelh1(1, self.x)
        out += self.rho_t * Bf.hankelh1(1, self.x)
        return out

    @property
    def mu_3(self) -> complex:
        out = 1 - 2 * self.rho_t
        out *= Bf.hankelh1(1, self.x_v)

        out += self.x_v * Bf.d1_hankelh1(1, self.x_v)
        return out

    @property
    def mu_4(self) -> complex:
        out = 2 * (1 - self.rho_t) ** 2
        out *= Bf.hankelh1(1, self.x)
        out *= Bf.hankelh1(1, self.x_v)

        out += self.mu_2 * self.mu_3
        return out


class TestScatteringCompareToKing(
    TestBaseDoinikov1994,
    HelperCompareScattering,
):
    def setUp(self) -> None:
        super().setUp()

        self._scattering_compare_threshold = 1e-2
        self.parameters.N_max = 3
        self.parameters.eta_f *= 1e-5
        self.parameters.zeta_f *= 1e-5
        self.parameters.R_0 = 1e-6

        self.cls = SolutionFactory().doinikov_1994_rigid_scattering()
        self.compare_cls = SolutionFactory().king_1934_scattering()


if __name__ == "__main__":
    unittest.main()
