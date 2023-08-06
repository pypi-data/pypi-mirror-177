from __future__ import annotations

import unittest
from collections.abc import Callable
from numbers import Number
from typing import Any

import numpy as np

from osaft import WaveType
from osaft.core.frequency import Frequency
from osaft.solutions.base_solution import BaseSolution
from osaft.tests.testing_parameters import (
    BaseChangingVariable,
    RandomParameters,
)


class NumericTestCase(unittest.TestCase):
    def assertAlmostEqual(
        self,
        val1: Number,
        val2: Number,
        threshold: None | float = 1e-12,
        print_results: None | bool = False,
        user_msg: None | str = None,
    ) -> None:
        """Asserting the relative difference of two values when num. rounding
        errors can occur

        Assertion is handled by :meth:`BaseTest._assertAlmostEqual()`

        If the values are complex, then the real and imaginary part will be
        tested separately. Also, if one of the test fails, automatically, a
        nice formatted output is generated as error message.

        :param val1: first value to be compared
        :param val2: second value to be compared
        :param threshold: threshold of relative difference, defaults to 1e-12
        :param print_results: if True the two values are printed to the console
            for easier debugging, defaults to False
        :param user_msg: custom message that is printed if the assertion fails.
        """
        if print_results:
            msg = f"\nval1     : {val1:+.8e}\n"
            msg += f"val2     : {val2:+.8e}\n"
            if not val1 == 0 and not val2 == 0:
                msg += f"rel diff.: {abs((val1 - val2) / val1):+.8e}"
            print(msg)

        self._assertAlmostEqual(val1.real, val2.real, threshold)
        if isinstance(val1, complex) or isinstance(val2, complex):
            self._assertAlmostEqual(val1.imag, val2.imag, threshold, user_msg)

    def _assertAlmostEqual(
        self,
        val1: float,
        val2: float,
        threshold: float,
        user_msg: None | str = None,
    ) -> None:

        msg = "\nAssertion failed\n"
        if user_msg:
            msg += f"\n{user_msg}\n"

        if val1 == 0 or val2 == 0:
            msg += "One of the values is Zero; the other not\n"
            msg += f"val1     : {val1:+.8e}\n"
            msg += f"val2     : {val2:+.8e}\n"
            test = abs(val1) < threshold and abs(val2) < threshold
            self.assertTrue(expr=test, msg=msg)
        else:
            diff = np.abs(val1 - val2)
            if np.abs(val1) > np.abs(val2):
                test = np.abs(diff / val2) < threshold
            else:
                test = np.abs(diff / val1) < threshold

            msg += "The rel. diff. is bigger than the threshold\n"
            msg += f"val1     : {val1:+.8e}\n"
            msg += f"val2     : {val2:+.8e}\n"
            msg += f"rel diff.: {abs(diff/val1):+.8e}\n"
            msg += f"threshold: {threshold:+.8e}"

            self.assertTrue(expr=test, msg=msg)


class BaseTestSolutions(NumericTestCase):
    def setUp(self):

        self.parameters = RandomParameters()

        # List of classes to be tests
        self.list_cls = []

        # Frequency Class
        self.frequency = Frequency(self.parameters.f)

        # Runs
        self._n_runs = self.parameters._wave_type.longest_list

    @property
    def n_runs(self) -> int:
        return self._n_runs

    @n_runs.setter
    def n_runs(self, val) -> None:
        if val < self.parameters._wave_type.longest_list:
            raise ValueError(
                "n_runs must be greater than the longest "
                "list of ChangingFromList._longest_list",
            )
        else:
            self._n_runs = val

    # -------------------------------------------------------------------------
    # Getters & Setters
    # -------------------------------------------------------------------------

    @property
    def R_0(self) -> float:
        return self.parameters.R_0

    @property
    def f(self) -> float:
        return self.parameters.f

    @property
    def c_f(self) -> float:
        return self.parameters.c_f

    @property
    def rho_f(self) -> float:
        return self.parameters.rho_f

    @property
    def c_s(self) -> float:
        return self.parameters.c_s

    @property
    def eta_s(self) -> float:
        return self.parameters.eta_s

    @property
    def zeta_s(self) -> float:
        return self.parameters.zeta_s

    @property
    def rho_s(self) -> float:
        return self.parameters.rho_s

    @property
    def eta_f(self) -> float:
        return self.parameters.eta_f

    @property
    def zeta_f(self) -> float:
        return self.parameters.zeta_f

    @property
    def eta_p(self) -> float:
        return self.parameters.eta_p

    @property
    def zeta_p(self) -> float:
        return self.parameters.zeta_p

    @property
    def lambda_M(self) -> float:
        return self.parameters.lambda_M

    @property
    def E_s(self) -> float:
        return self.parameters.E_s

    @property
    def nu_s(self) -> float:
        return self.parameters.nu_s

    @property
    def p_0(self) -> float:
        return self.parameters.p_0

    @property
    def position(self) -> float:
        return self.parameters.position

    @property
    def wave_type(self) -> WaveType:
        return self.parameters.wave_type

    @property
    def N_max(self):
        return self.parameters.N_max

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_name_attribute(self) -> None:
        if hasattr(self, "cls"):
            if isinstance(self.cls, BaseSolution):
                self.assertTrue(self.cls.name != "")

    def test_copy(self) -> None:
        if hasattr(self, "cls"):
            if isinstance(self.cls, BaseSolution):
                tmp = self.cls.copy()
                self.assertTrue(type(self.cls) == type(tmp))
                self.assertFalse(self.cls is tmp)

    # -------------------------------------------------------------------------
    # Generic test methods for properties and methods
    # -------------------------------------------------------------------------

    def _test_properties(
        self,
        list_of_properties: list[str],
        threshold: float = 1e-12,
    ) -> None:
        """Tests the properties inside `list_of_properties` of self & self.cls

        If a test fails the name of the failing property is printed.

        :param list_of_properties: list of properties to be tested
        :param threshold: comparing threshold for the whole list
        """

        for name in list_of_properties:
            with self.subTest(property=name):
                self.do_testing(
                    func_1=lambda: getattr(self, name),
                    func_2=lambda: getattr(self.cls, name),
                    threshold=threshold,
                )

    def _test_methods_n(
        self,
        dict_of_methods: dict[str, dict[tuple[Any]]],
        n_end: int = 5,
        threshold: float = 1e-12,
        zero: None | float = None,
    ) -> None:
        """Tests the methods inside `dict_of_methods` of self & self.cls

        All methods have as first argument `n`. The key of the dict is the name
        of the methods. The `value` of the dict are the optional additional
        arguments.  If `value` == None, then it is a method solely depending on
        `n`.

        If a test fails the name of the failing method is printed.

        :param dict_of_methods: dict of methods and additional arguments to be
            tested
        :param n_end: n in [0, 1, ..., n_end]
        :param threshold: comparing threshold for the whole dict
        :param threshold: value below which test values are assumed to be zero
        """

        for method, args in dict_of_methods.items():
            func_1 = getattr(self, method)
            func_2 = getattr(self.cls, method)
            for n in range(n_end, 0, -1):

                if args is not None:
                    if isinstance(args, tuple):
                        arg = (n, *args)
                    else:
                        arg = (n, args)
                else:
                    arg = n

                with self.subTest(method=method, arguments=arg):
                    self.do_testing(
                        func_1=func_1,
                        args_1=arg,
                        func_2=func_2,
                        args_2=arg,
                        threshold=threshold,
                        zero=zero,
                    )

    # -----------------------------------------------------------------------------
    # Tests
    # -----------------------------------------------------------------------------

    def do_testing(
        self,
        func_1: Callable,
        func_2: Callable,
        args_1: None | Any = None,
        args_2: None | Any = None,
        threshold: float = 1e-10,
        zero: None | float = None,
    ) -> None:
        """Compares the outputs of `func_1` against `func_2`.

        The variables in
        :attr:`BaseTest.test_variables` are changed and assigned one
        after the other to test all dependencies. This procedure is repeated
        :attr:`BaseTest.n_runs` times. Arguments to the functions can be
        passed with `args_1` and `args_2` to the respective functions.
        Testing is handled by :meth:`BaseTest._test_variables()` and changing
        of the values :meth:`BaseTest.change_and_assign_single_variable`

        In order to test properties of a class the following syntax is used:

        .. highlight:: python

        self.do_testing(lambda: self.cls.some_property, self.some_function)

        :param func_1: first function
        :param func_2: second function
        :param args_1: arguments for first function
        :param args_2: arguments for second functions
        :param threshold: threshold for failing the test, defaults to 1e-12
        :param zero: value below which test values are assumed to be zero
        """
        self.assign_parameters()
        self._test_variables(
            func_1,
            args_1,
            func_2,
            args_2,
            threshold,
            zero,
        )
        for _ in np.arange(self.n_runs):
            for var in self.parameters.list_parameters:
                if self._check_if_has_attr(var.name):
                    with self.subTest(msg=f"Changing {var.name}"):
                        self.change_and_assign_single_variable(var)
                        self._test_variables(
                            func_1,
                            args_1,
                            func_2,
                            args_2,
                            threshold,
                            zero,
                        )

    def _check_if_has_attr(self, name: str):
        """Check if any class in list_cls has the attribute `name`

        param name: name of the attribute
        """
        list_hasattr = [hasattr(cls, name) for cls in self.list_cls]
        return np.any(list_hasattr)

    def _test_variables(
        self,
        func_1: Callable,
        args_1: tuple,
        func_2: Callable,
        args_2: tuple,
        threshold: None | float = 1e-12,
        zero: None | float = None,
    ) -> None:
        """Checks if func_1(args) is almost equal to func_2 args

        Checks if func_1(args) is almost equal to func_2 args with tolerance
        `threshold`. Values below `zero` are assumed to be 0.

        :param func_1: first function
        :param args_1: arguments for the first function
        :param func_2: second function
        :param args_2: arguments for the second function
        :param threshold: tolerance
        "param zero: value below which test values are assumed to be zero
        """
        # check type of parameters1
        first = self._get_value(func_1, args_1)
        second = self._get_value(func_2, args_2)

        if zero is not None:
            first = 0 if abs(first) < zero else first
            second = 0 if abs(second) < zero else second

        self.assertAlmostEqual(first, second, threshold=threshold)

    @staticmethod
    def _get_value(func: Callable, args: tuple):
        """Get the value of the function `func` with arguments `arg`

        :param func: function
        :param args: arguments
        """
        if args is None:
            out = func()
        elif isinstance(args, tuple):
            out = func(*args)
        else:
            out = func(args)
        return out

    def assign_parameters(self) -> None:
        """Assigns the changed parameters to all instances

        This needs to be implemented in each derived object of `BaseTest`

        :raises NotImplementedError: Needs to be implemented in the
            derived object of BaseTest
        """
        for var in self.parameters.list_parameters:
            for cls in self.list_cls:
                if hasattr(cls, var.name):
                    setattr(cls, var.name, var.value)

    def change_and_assign_single_variable(
        self,
        var: BaseChangingVariable,
    ) -> None:
        """`var` is changed and its value is assigned so the attribute with
        the name `var.name`.

        The method `var.change` is called which randomly changes
        `var.value`. `var.value` is then assigned to the attribute of `self`
        with the name `var.name`.
        Assigning is handled by :meth:`BaseTest.assign_parameters()`

        :param var: Attribute name
        """
        var.change()
        self.assign_parameters()

    def assertAlmostEqual(
        self,
        val1: Number,
        val2: Number,
        threshold: None | float = 1e-12,
        print_results: None | bool = False,
    ) -> None:

        super().assertAlmostEqual(
            val1,
            val2,
            threshold,
            print_results,
            user_msg=f"\nseed number {self.parameters.seed}\n",
        )


if __name__ == "__main__":
    pass
