import unittest

from osaft.tests.solution_factory import SolutionFactory
from osaft.tests.solutions.basedoinikov1994.test_base import (
    TestBaseDoinikov1994,
)


class BaseTestARF(TestBaseDoinikov1994):
    def setUp(self) -> None:
        super().setUp()

        self.long_wavelength = False
        self.small_boundary_layer = False
        self.large_boundary_layer = False
        self.background_streaming = True
        self.fastened_sphere = False

        self.parameters._eta_f.low = 1e-5
        self.parameters._eta_f.high = 1e-3
        self.parameters._f.low = 1e6
        self.parameters._f.high = 10e6
        self.parameters._R_0.low = 1e-6

        self.cls = SolutionFactory().doinikov_1994_rigid_arf()
        self.cls.long_wavelength = self.long_wavelength
        self.cls.small_boundary_layer = self.small_boundary_layer
        self.large_boundary_layer = self.large_boundary_layer
        self.fastened_sphere = self.fastened_sphere

        self.list_cls = [self.cls]

    def assign_parameters(self) -> None:
        super().assign_parameters()

        self.cls.fastened_sphere = self.fastened_sphere
        self.cls.small_boundary_layer = self.small_boundary_layer
        self.cls.large_boundary_layer = self.large_boundary_layer
        self.cls.long_wavelength = self.long_wavelength
        self.cls.background_streaming = self.background_streaming
        self.cls.N_max = self.N_max


if __name__ == "__main__":
    unittest.main()
