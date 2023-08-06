from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from osaft.core.variable import ActiveVariable, PassiveVariable
from osaft.plotting.grid import (
    CartesianFluidGrid,
    CartesianGrid,
    CartesianScattererGrid,
    MaskedCartesianGrid,
    PolarGrid,
)
from osaft.solutions.base_scattering import BaseScattering
from osaft.solutions.base_streaming import BaseStreaming

NDArray = np.ndarray


class VelocityFieldData(ABC):
    """Container for plotting data for scattering and streaming plots

    :param sol: solution
    :param r_min: start point for radial plotting range in [m]
    :param r_max: end point for tangential plotting range  in [m]
    :param res: resolution, if tuple (radial resolution, tangential resolution)
    :param n_quiver_points: anchor points along z for quiver arrows
    :param symmetric: if ``True`` the dataset is assumed to be symmetric
    """

    _EPS_r_min = 1e-30

    def __init__(
        self,
        sol: BaseScattering | BaseStreaming,
        r_min: float,
        r_max: float,
        res: int | tuple[int, int],
        n_quiver_points: int | tuple[int, int],
        symmetric,
    ) -> None:
        """Constructor method"""

        # Parameters for the coordinate grid
        self._r_min = PassiveVariable(r_min, "r min")
        self._r_max = PassiveVariable(r_max, "r max")
        self._resolution = PassiveVariable(res, "plotting resolution")
        self._n_quiver_points = PassiveVariable(
            n_quiver_points,
            "quiver resolution along z",
        )
        self._symmetric = PassiveVariable(symmetric)

        # Solution to be plotted
        self._sol = PassiveVariable(sol, "solution for plotting")
        self._mode = PassiveVariable(None, "mode")

        # Dependent Variables: Data containers for solution
        self._x = ActiveVariable(self._reset_real_array, "x coordinate")
        self._z = ActiveVariable(self._reset_real_array, "z coordinate")
        self._u = ActiveVariable(
            self._reset_complex_array,
            "velocity/displacement in x-direction",
        )
        self._w = ActiveVariable(
            self._reset_complex_array,
            "velocity/displacement in y-direction",
        )
        self._v_norm = ActiveVariable(
            self._reset_real_array,
            "norm of the velocity / displacement",
        )
        # Dependent Variables: Data containers for quiver solution
        self._x_quiver = ActiveVariable(
            self._reset_real_array_quiver,
            "x coordinate of quiver arrows",
        )
        self._z_quiver = ActiveVariable(
            self._reset_real_array_quiver,
            "z coordinate of quiver arrows",
        )
        self._u_quiver = ActiveVariable(
            self._reset_complex_array_quiver,
            "velocity in z-direction (quiver)",
        )
        self._w_quiver = ActiveVariable(
            self._reset_complex_array_quiver,
            "velocity in x-direction (quiver)",
        )

        # Dependent Variables: Coordinate grid
        self._grid = ActiveVariable(self._get_grid)
        self._grid_quiver = ActiveVariable(self._get_grid_quiver)

        # Setting links
        self._grid.is_computed_by(
            self._r_min,
            self._r_max,
            self._resolution,
            self._symmetric,
        )
        self._grid_quiver.is_computed_by(
            self._r_min,
            self._r_max,
            self._n_quiver_points,
            self._symmetric,
        )
        # contour solution
        self._x.is_computed_by(self._grid)
        self._z.is_computed_by(self._grid)
        self._u.is_computed_by(self._sol, self._grid, self._mode)
        self._w.is_computed_by(self._sol, self._grid, self._mode)
        self._v_norm.is_computed_by(self._sol, self._grid, self._mode)
        # quiver solution
        self._x_quiver.is_computed_by(self._grid_quiver)
        self._z_quiver.is_computed_by(self._grid_quiver)
        self._u_quiver.is_computed_by(self._sol, self._grid_quiver, self._mode)
        self._w_quiver.is_computed_by(self._sol, self._grid_quiver, self._mode)

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def get_velocity_magnitude(self) -> tuple[NDArray, NDArray, NDArray]:
        """Returns the velocity magnitudes

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the magnitude of the velocity field at
        these points
        """
        return self.x, self.z, self.u_norm  # pragma: no cover

    def get_velocity_vector(self) -> tuple[NDArray, NDArray, NDArray, NDArray]:
        """Returns the velocity vectors

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the velocity field vectors at
        these points
        """
        return self.x, self.z, self.u, self.w  # pragma: no cover

    def get_velocity_vector_quiver(
        self,
    ) -> tuple[NDArray, NDArray, NDArray, NDArray]:
        """Returns the velocity vectors and coordinates for the quiver plot"""
        return (
            self.z_quiver,
            self.x_quiver,  # pragma: no cover
            self.u_quiver,
            self.w_quiver,  # pragma: no cover
        )

    # -------------------------------------------------------------------------
    # Getters and Setters for Independent Variables
    # -------------------------------------------------------------------------

    @property
    def sol(self) -> BaseScattering | BaseStreaming:
        """Solution for plotting

        :getter: returns the end point for radial plotting range
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._sol.value

    @sol.setter
    def sol(self, value: BaseScattering | BaseStreaming) -> None:
        self._sol.value = value

    @property
    def r_min(self) -> float:
        """Endpoint for radial plotting range [m]

        :getter: returns the end point for radial plotting range
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._r_min.value

    @r_min.setter
    def r_min(self, value: float) -> None:
        self._r_min.value = value

    @property
    def r_max(self) -> float:
        """Start point for radial plotting range [m]

        :getter: returns the start point for radial plotting range
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._r_max.value

    @r_max.setter
    def r_max(self, value: float) -> None:
        self._r_max.value = value

    @property
    def n_quiver_points(self) -> int:
        """Number of anchor points for quiver arrows

        :getter: returns n_point
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._n_quiver_points.value

    @n_quiver_points.setter
    def n_quiver_points(self, value: int) -> None:
        self._n_quiver_points.value = value

    @property
    def resolution(self) -> int | tuple[int, int]:
        """Resolution for scattering / streaming plots

        `resolution` can be an `int` when the resolution in radial and
        tangential direction is the same, or a `tuple` of two `int`
        for independent resolutions (radial resolution, tangential_resolution)
        :getter: returns plotting resolution
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._resolution.value

    @resolution.setter
    def resolution(self, value: int | tuple[int, int]) -> None:
        self._resolution.value = value

    @property
    def mode(self) -> int:
        """Mode that is plotted. If `None` all modes up to `sol.N_max`
        are superimposed.
        :getter: returns the mode
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._mode.value

    @property
    def symmetric(self) -> bool:
        """Symmetry option of the grid

        If ``True`` the velocity field is assumed to be symmetric.
        :getter: returns plotting resolution
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._symmetric.value

    @symmetric.setter
    def symmetric(self, value: bool) -> None:
        self._symmetric = value

    # -------------------------------------------------------------------------
    # Getters for Dependent Variables (contour solution)
    # -------------------------------------------------------------------------

    @property
    def grid(self) -> PolarGrid:
        """Plotting grid"""
        return self._grid.value

    @property
    def x(self) -> NDArray:
        """x-coordinates of the plotting grid in [m]"""
        if np.all(self._x.value == 0):
            self._compute_data()
        return self._x.value

    @property
    def z(self) -> NDArray:
        """z-coordinates of the plotting grid in [m]"""
        if np.all(self._z.value == 0):
            self._compute_data()  # pragma: no cover
        return self._z.value

    @property
    def u(self) -> NDArray:
        """Velocity / displacement in x-direction in [m/s]"""
        if np.all(self._u.value == 0):
            self._compute_data()
        return self._u.value

    @property
    def w(self) -> NDArray:
        """Velocity / displacement in z-direction in [m/s]"""
        if np.all(self._w.value == 0):
            self._compute_data()  # pragma: no cover
        return self._w.value

    @property
    def u_norm(self) -> NDArray:
        """Norm of the velocity / displacement in z-direction in [m/s]

        norm = abs(u) ** 2 + abs(w) ** 2
        """
        if np.all(self._v_norm.value == 0):
            self._compute_data()
        return self._v_norm.value

    # -------------------------------------------------------------------------
    # Getters for Dependent Variables (quiver solution)
    # -------------------------------------------------------------------------

    @property
    def grid_quiver(self) -> CartesianGrid:
        """Plotting grid"""
        return self._grid_quiver.value

    @property
    def x_quiver(self) -> NDArray:
        """x-coordinates of the quiver plotting grid in [m]"""
        if np.all(self._x_quiver.value == 0):
            self._compute_data_quiver()
        return self._x_quiver.value

    @property
    def z_quiver(self) -> NDArray:
        """z-coordinates of the quiver plotting grid in [m]"""
        if np.all(self._z_quiver.value == 0):
            self._compute_data_quiver()  # pragma: no cover
        return self._z_quiver.value

    @property
    def u_quiver(self) -> NDArray:
        """Velocity / displacement in x-direction in [m/s]"""
        if np.all(self._u_quiver.value == 0):
            self._compute_data_quiver()
        return self._u_quiver.value

    @property
    def w_quiver(self) -> NDArray:
        """Velocity / displacement in z-direction in [m/s]"""
        if np.all(self._w_quiver.value == 0):
            self._compute_data_quiver()  # pragma: no cover
        return self._w_quiver.value

    # -------------------------------------------------------------------------
    # Methods for dependent variables
    # -------------------------------------------------------------------------

    def _reset_real_array(self) -> NDArray:
        """Resets real arrays for coordinates and norm"""
        return np.zeros(
            self.grid.res_r * self.grid.res_theta,
            dtype=np.float64,
        )

    def _reset_real_array_quiver(self) -> NDArray:
        """Resets real arrays (quiver) for coordinates and norm"""
        return np.zeros(
            len(self.grid_quiver.flat_mesh_x),
        )

    def _reset_complex_array(self) -> NDArray:
        """Resets complex arrays for complex velocities and norm"""
        return np.zeros(
            self.grid.res_r * self.grid.res_theta,
            dtype=np.complex128,
        )

    def _reset_complex_array_quiver(self) -> NDArray:
        """Resets complex arrays (quiver) for complex velocities and norm"""
        return np.zeros(
            len(self.grid_quiver.flat_mesh_x),
            dtype=np.complex128,
        )

    # -------------------------------------------------------------------------
    # Private Methods
    # -------------------------------------------------------------------------

    def _get_grid(self) -> PolarGrid:
        """Returns a new coordinate grid"""
        return PolarGrid(
            self.r_min,
            self.r_max,
            self.resolution,
            self.symmetric,
        )

    def _get_grid_quiver(self) -> MaskedCartesianGrid:
        """Returns a new coordinate grid for the quiver plots"""
        if self.r_min <= self._EPS_r_min:
            return CartesianScattererGrid(
                self.r_max,
                self.n_quiver_points,
                self.symmetric,
            )
        else:
            return CartesianFluidGrid(
                self.sol.R_0,
                self.r_max,
                self.n_quiver_points,
                self.symmetric,
            )

    @abstractmethod
    def _compute_data(self) -> tuple[NDArray, NDArray]:
        """Compute the velocity data and store it in the attributes"""
        pass  # pragma: no cover

    @abstractmethod
    def _compute_data_quiver(self) -> tuple[NDArray, NDArray]:
        """Compute the velocity data and store it in the respective
        attributes"""
        pass  # pragma: no cover


if __name__ == "__main__":
    pass
