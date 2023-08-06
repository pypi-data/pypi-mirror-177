from abc import abstractmethod

from osaft import WaveType
from osaft.core.backgroundfields import WrongWaveTypeError
from osaft.tests.testing_parameters import RandomParameters


class HelperARF:
    """Baseclass for testing the ARF computation"""

    _threshold = 1e-12

    @abstractmethod
    def compute_arf(self):
        pass

    def test_wrong_wave_type_error(self):
        WaveType.WRONGWAVETYPE = 3, "wrong wave type"
        self.cls.wave_type = WaveType.WRONGWAVETYPE
        self.assertRaises(WrongWaveTypeError, self.cls.compute_arf)

    def test_arf(self) -> None:
        self.do_testing(
            self.compute_arf,
            self.cls.compute_arf,
            threshold=self._threshold,
            zero=1e-30,
        )


class HelperStandingARF(HelperARF):

    parameters: RandomParameters

    def test_arf(self) -> None:
        self.parameters.wave_type = WaveType.STANDING
        self.parameters._wave_type.list_of_values = [WaveType.STANDING]
        HelperARF.test_arf(self)


class HelperTravelingARF(HelperARF):

    parameters: RandomParameters

    def test_arf(self) -> None:

        self.parameters.wave_type = WaveType.TRAVELLING
        self.parameters._wave_type.list_of_values = [WaveType.TRAVELLING]
        HelperARF.test_arf(self)


class HelperCompareARF:
    arf_compare_threshold = 1e-12

    def test_comparison_arf(self):
        self.do_testing(
            self.cls.compute_arf,
            self.compare_cls.compute_arf,
            threshold=self.arf_compare_threshold,
            zero=1e-30,
        )
