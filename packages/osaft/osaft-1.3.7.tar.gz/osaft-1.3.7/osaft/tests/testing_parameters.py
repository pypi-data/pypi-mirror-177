from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from typing import Any

import numpy as np

from osaft import WaveType


class BaseChangingVariable:
    """Type used as attribute of a `TestCase` that is changed automatically.

    To test the observer pattern testing, attributes of classes are
    changed to ensure proper linking. If a test class has an attribute of
    type :class:`BaseChangingVariable` then the attribute of the tested
    class with the name `name` is initially set to `value`. During the
    testing the attribute is changed to a new value using the method
    `change`.

    :param name: name of the attribute in the class to be tested
    :param value: initial value of the attribute
    :param seed: seed for RNG to make testing reproducible
    """

    def __init__(
        self,
        name: str,
        value: Any,
        seed: int,
    ) -> None:
        """Constructor method"""
        self.name = name
        self.value = value

        self.rng = np.random.default_rng(seed)

    @abstractmethod
    def change(self) -> None:
        """Randomly change `value`"""
        pass


class ChangingFromList(BaseChangingVariable):
    """Child of :class:`BaseChangingVariable`.

    The method `change` changes `value` by choosing an item from
    :attr:`list_of_values`.

    :param name: name of the attribute in the class to be tested
    :param value: initial value of the attribute
    :param list_of_values: list of values to choose from
    :param seed: seed for RNG to make testing reproducible
    """

    _longest_list = 0

    def __init__(
        self,
        name: str,
        value: Any,
        list_of_values: Sequence[Any],
        seed: int,
    ) -> None:

        super().__init__(name, value, seed)

        self.list_of_values = list_of_values

    def _set_longest_list(self) -> None:
        if len(self.list_of_values) > self._longest_list:
            ChangingFromList._longest_list = len(self.list_of_values)

    def _reset_non_tested_values(self) -> None:
        # [*list] syntax is needed for not passing a reference but creating an
        # actual new list
        self._non_tested_values = [*self.list_of_values]

    @property
    def list_of_values(self) -> list[any]:
        return self._list_of_values

    @list_of_values.setter
    def list_of_values(self, lst: list[any]) -> None:
        self._list_of_values = lst
        self._set_longest_list()
        self._reset_non_tested_values()

    @property
    def longest_list(self) -> int:
        return ChangingFromList._longest_list

    def change(self) -> None:
        """Randomly change `value`"""
        if len(self._non_tested_values) < 1:
            self._reset_non_tested_values()

        self.value = self.rng.choice(self._non_tested_values)
        self._non_tested_values.remove(self.value)


class ChangingBool(BaseChangingVariable):
    """Child of :class:`BaseChangingVariable`

    Child of :class:`BaseChangingVariable` for the case when value is of type
    `bool`.

    :param name: name of the attribute in the class to be tested
    :param value: initial value of the attribute
    :param seed: seed for RNG to make testing reproducible
    """

    def __init__(self, name: str, value: bool, seed: int) -> None:
        """Constructor method"""
        super().__init__(name, value, seed)

    @abstractmethod
    def change(self) -> None:
        """Randomly change `value`"""
        self.value = self.rng.random() > 0.5


class ChangingNumber(BaseChangingVariable):
    """Child of :class:`BaseChangingVariable`

    Child of :class:`BaseChangingVariable` for the case when value is a number.

    :param name: name of the attribute in the class to be tested
    :param value: initial value of the attribute
    :param seed: seed for RNG to make testing reproducible
    :param low: lowest value `value` is changed to
    :param high: highest value `value` is changed to
    """

    def __init__(
        self,
        name: str,
        value: None | float | int,
        seed: int,
        low: None | float | int,
        high: float | int,
    ) -> None:
        """Constructor method"""
        super().__init__(name, value, seed)
        self.test_inputs(value, low, high)
        self._low = low
        self._high = high

    @staticmethod
    def test_inputs(
        value: None | int | float,
        low: None | int | float,
        high: None | int | float,
    ):
        if low is not None and high is not None:
            assert low <= value <= high, "condition low < value < high not met"
        elif low is not None:
            assert low <= value, "condition low < value < high is not met"
        elif high is not None:
            assert value <= high, "condition low < value < high is not met"

    @property
    def low(self) -> None | int | float:
        return self._low

    @low.setter
    def low(self, value: int | float) -> None:
        if self.high is not None and value > self.high:
            raise ValueError(
                f"low (= {value}) needs to be smaller than high "
                f"(= {self.high})",
            )
        elif value > self.value:
            self._low = value
            self.value = value
            self.change()
        else:
            self._low = value

    @property
    def high(self) -> float | int:
        return self._high

    @high.setter
    def high(self, value: int | float) -> None:
        if self.low is not None and value < self.low:
            raise ValueError(
                f"high (= {value}) needs to be larger than low "
                f"(= {self.low})",
            )
        elif value < self.value:
            self._high = value
            self.value = value
            self.change()
        else:
            self._high = value

    @abstractmethod
    def change(self) -> None:
        """Randomly change `value`"""
        pass


class ChangingFloat(ChangingNumber):
    """Child of :class:`BaseChangingVariable`

    Child of :class:`BaseChangingVariable` for the case when value is a
    `float`.

    :param name: name of the attribute in the class to be tested
    :param value: initial value of the attribute
    :param seed: seed for RNG to make testing reproducible
    :param low: lowest value `value` is changed to
    :param high: highest value `value` is changed to
    """

    def __init__(
        self,
        name: str,
        value: float,
        seed: int,
        low: None | float = None,
        high: None | float = None,
    ) -> None:
        """Constructor method"""
        super().__init__(name, value, seed, low, high)

    def change(self) -> None:
        """Randomly change `value`"""
        if self.low is not None and self.high is not None:
            self.value = self.low + (self.high - self.low) * self.rng.random()
        elif self.low is not None:
            change = self.value * (self.rng.random() - 0.5)
            if self.value + change > self.low:
                self.value += change
            else:
                self.value -= change
        elif self.high is not None:
            change = self.value * (self.rng.random() - 0.5)
            if self.value + change < self.high:
                self.value += change
            else:
                self.value -= change
        else:
            self.value += (self.rng.random() - 0.5) * self.value


class ChangingInt(ChangingNumber):
    """Child of :class:`BaseChangingVariable`

    Child of :class:`BaseChangingVariable` for the case when value is an
    `int`. Default values for `low` and `high` are 0 and 100 respectively. If
    `value` is outside this range the parameters have to be set accordingly.

    :param name: name of the attribute in the class to be tested
    :param value: initial value of the attribute
    :param seed: seed for RNG to make testing reproducible
    :param low: lowest value `value` is changed to
    :param high: highest value `value` is changed to
    """

    def __init__(
        self,
        name: str,
        value: int,
        seed: int,
        low: int = 0,
        high: int = 100,
    ):
        """Constructor method"""
        super().__init__(name, value, seed, low, high)

    def change(self) -> None:
        """Randomly change `value`"""
        self.value = self.rng.integers(low=self.low, high=self.high)


class RandomParameters:
    """Stores and changes a list of parameters commonly used for testing.

    :param default: if ``True`` default parameters are return, else random
       parameters
    """

    def __init__(self, default: bool = True):

        # Create seed
        seed = np.random.randint(1, 10000)
        self.seed = seed
        self.rng = np.random.default_rng(seed)

        # Geometry
        self._R_0 = ChangingFloat("R_0", 1e-6, self.seed, low=0)
        # Frequency
        self._f = ChangingFloat("f", 1e6, self.seed, low=0)
        # Inviscid Fluid
        self._c_f = ChangingFloat("c_f", 1.5e3, self.seed, low=0)
        self._rho_f = ChangingFloat("rho_f", 1e3, self.seed, low=0)
        # Compressible Particle (Inviscid Fluid)
        self._c_s = ChangingFloat("c_s", 2.5e3, self.seed, low=0)
        # Compressible Particle (Viscous Fluid)
        self._eta_s = ChangingFloat("eta_s", 1e-3, self.seed, low=0)
        self._zeta_s = ChangingFloat("zeta_s", 1e-3, self.seed, low=0)
        # Viscous Fluid
        self._eta_f = ChangingFloat(
            "eta_f",
            1e-3,
            self.seed,
            low=1e-5,
            high=1e-2,
        )
        self._zeta_f = ChangingFloat("zeta_f", 1e-3, self.seed, low=0)
        # Viscoelastic Fluid
        self._eta_p = ChangingFloat("eta_p", 1e-3, self.seed, low=0)
        self._zeta_p = ChangingFloat("zeta_p", 1e-3, self.seed, low=0)
        self._lambda_M = ChangingFloat("lambda_M", 1e-3, self.seed, low=0)
        # Rigid Solid
        self._rho_s = ChangingFloat("rho_s", 1.5e3, self.seed, low=0)
        # Elastic solid
        self._E_s = ChangingFloat("E_s", 75e6, self.seed, low=0)
        self._nu_s = ChangingFloat("nu_s", 0.3, self.seed, low=0, high=0.49)
        # Background Field
        self._p_0 = ChangingFloat("p_0", 1e5, self.seed, low=0)
        self._position = ChangingFloat(
            "position",
            np.pi / 4,
            self.seed,
            low=0,
            high=2 * np.pi,
        )
        self._wave_type = ChangingFromList(
            "wave_type",
            WaveType.STANDING,
            WaveType,
            self.seed,
        )

        self._N_max = ChangingInt(
            "N_max",
            2,
            self.seed,
            low=2,
            high=5,
        )

        if not default:
            self.change_all()

        self.list_parameters = self.get_list_parameters()

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def change_all(self) -> None:
        for para in self.list_parameters:
            para.change()

    def get_list_parameters(self) -> list:
        """Returns a list of all random parameters"""
        list_parameters = []

        for attr, val in vars(self).items():
            if isinstance(val, BaseChangingVariable):
                list_parameters.append(val)
        return list_parameters

    # -------------------------------------------------------------------------
    # Getters & Setters
    # -------------------------------------------------------------------------

    @property
    def R_0(self) -> float:
        return self._R_0.value

    @R_0.setter
    def R_0(self, value: float) -> None:
        self._R_0.value = value

    @property
    def f(self) -> float:
        return self._f.value

    @f.setter
    def f(self, value: float) -> None:
        self._f.value = value

    @property
    def c_f(self) -> float:
        return self._c_f.value

    @c_f.setter
    def c_f(self, value: float) -> None:
        self._c_f.value = value

    @property
    def rho_f(self) -> float:
        return self._rho_f.value

    @rho_f.setter
    def rho_f(self, value: float) -> None:
        self._rho_f.value = value

    @property
    def c_s(self) -> float:
        return self._c_s.value

    @c_s.setter
    def c_s(self, value: float) -> None:
        self._c_s.value = value

    @property
    def eta_s(self) -> float:
        return self._eta_s.value

    @eta_s.setter
    def eta_s(self, value: float) -> None:
        self._eta_s.value = value

    @property
    def zeta_s(self) -> float:
        return self._zeta_s.value

    @zeta_s.setter
    def zeta_s(self, value: float) -> None:
        self._zeta_s.value = value

    @property
    def rho_s(self) -> float:
        return self._rho_s.value

    @rho_s.setter
    def rho_s(self, value: float) -> None:
        self._rho_s.value = value

    @property
    def eta_f(self) -> float:
        return self._eta_f.value

    @eta_f.setter
    def eta_f(self, value: float) -> None:
        self._eta_f.value = value

    @property
    def zeta_f(self) -> float:
        return self._zeta_f.value

    @zeta_f.setter
    def zeta_f(self, value: float) -> None:
        self._zeta_f.value = value

    @property
    def eta_p(self) -> float:
        return self._eta_p.value

    @eta_p.setter
    def eta_p(self, value: float) -> None:
        self._eta_p.value = value

    @property
    def zeta_p(self) -> float:
        return self._zeta_p.value

    @zeta_p.setter
    def zeta_p(self, value: float) -> None:
        self._zeta_p.value = value

    @property
    def lambda_M(self) -> float:
        return self._lambda_M.value

    @lambda_M.setter
    def lambda_M(self, value: float) -> None:
        self._lambda_M.value = value

    @property
    def E_s(self) -> float:
        return self._E_s.value

    @E_s.setter
    def E_s(self, value: float) -> None:
        self._E_s.value = value

    @property
    def nu_s(self) -> float:
        return self._nu_s.value

    @nu_s.setter
    def nu_s(self, value: float) -> None:
        self._nu_s.value = value

    @property
    def p_0(self) -> float:
        return self._p_0.value

    @p_0.setter
    def p_0(self, value: float) -> None:
        self._p_0.value = value

    @property
    def position(self) -> float:
        return self._position.value

    @position.setter
    def position(self, value: float) -> None:
        self._position.value = value

    @property
    def wave_type(self) -> WaveType:
        return self._wave_type.value

    @wave_type.setter
    def wave_type(self, value: WaveType) -> None:
        self._wave_type.value = value

    @property
    def N_max(self):
        return self._N_max.value

    @N_max.setter
    def N_max(self, value: int):
        self._N_max.value = value


if __name__ == "__main__":
    pass
