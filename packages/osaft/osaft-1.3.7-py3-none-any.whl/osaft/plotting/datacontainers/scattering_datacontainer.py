from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from osaft.core.functions import exp
from osaft.core.functions import (
    spherical_2_cartesian_coordinates as s2c_coord,
)
from osaft.core.variable import ActiveVariable, PassiveVariable
from osaft.plotting.datacontainers.base_velocity_datacontainer import (
    VelocityFieldData,
)
from osaft.solutions.base_scattering import BaseScattering

NDArray = np.ndarray


class ScatteringFieldData(VelocityFieldData, ABC):
    """Container for plotting data for the scattering field

    :param sol: solution
    :param r_min: start point for radial plotting range
    :param r_max: end point for tangential plotting range
    :param res: resolution, if tuple (radial resolution, tangential resolution)
    :param n_quiver_points: number of points along z-axis for quiver plot
    :param symmetric: if ``True`` the dataset is assumed to be symmetric
    """

    def __init__(
        self,
        sol: BaseScattering,
        r_min: float,
        r_max: float,
        res: int | tuple[int, int] = 100,
        n_quiver_points: int | tuple[int, int] = 21,
        symmetric: bool = True,
    ) -> None:
        """Constructor method"""

        VelocityFieldData.__init__(
            self,
            sol,
            r_min,
            r_max,
            res,
            n_quiver_points,
            symmetric,
        )

        # Velocities for the scattering field (complex valued)
        self._u = ActiveVariable(self._reset_complex_array, "x coordinate")
        self._w = ActiveVariable(self._reset_complex_array, "z coordinate")

        self._u.is_computed_by(self._sol, self._grid, self._mode)
        self._w.is_computed_by(self._sol, self._grid, self._mode)

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def get_velocity_magnitude(
        self,
        instantaneous: bool = True,
        phase: float = 0,
        mode: None | int = None,
    ) -> tuple[NDArray, NDArray, NDArray]:
        """Returns the velocity magnitudes

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the magnitude of the velocity field at
        these points

        :param instantaneous: if `True` the instant magnitude is returned
        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        """
        self._mode.value = mode
        if instantaneous:
            return self.x, self.z, self._velocity_norm_inst(phase)
        else:
            return self.x, self.z, self.u_norm

    def get_displacement_magnitude(
        self,
        instantaneous: bool = True,
        phase: float = 0,
        mode: None | int = None,
    ) -> tuple[NDArray, NDArray, NDArray]:
        """Returns the displacement magnitudes

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the magnitude of the displacement field at
        these points

        :param instantaneous: if `True` the instant magnitude is returned
        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        """
        self._mode.value = mode
        if instantaneous:
            return self.x, self.z, self._disp_norm_inst(phase)
        else:
            return self.x, self.z, self.u_norm / self.sol.omega

    def get_velocity_vector(
        self,
        phase: float = 0,
        mode: None | int = None,
    ) -> tuple[NDArray, NDArray, NDArray, NDArray]:
        """Returns the velocity vectors

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the velocity field vectors at
        these points

        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        """
        self._mode.value = mode
        if phase == 0:
            return self.x, self.z, self.u.real, self.w.real
        else:
            u = self.u * np.exp(-1j * phase)
            w = self.w * np.exp(-1j * phase)
            return self.x, self.w, u.real, w.real

    def get_displacement_vector(
        self,
        phase: float = 0,
        mode: None | int = None,
    ) -> tuple[NDArray, NDArray, NDArray, NDArray]:
        """Returns the displacement vectors

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the displacement field vectors at
        these points

        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        """
        self._mode.value = mode
        if phase == 0:
            u = 1j * self.u / self.sol.omega
            w = 1j * self.w / self.sol.omega
        else:
            u = self.u * np.exp(-1j * phase) / self.sol.omega
            w = self.w * np.exp(-1j * phase) / self.sol.omega
        return self.x, self.w, u.real, w.real

    # -------------------------------------------------------------------------
    # Private Methods
    # -------------------------------------------------------------------------

    def _velocity_norm_inst(
        self,
        phase: float,
    ) -> NDArray:
        """Instantaneous velocity magnitude

        :param phase: phase angle
        """
        if phase == 0:
            return np.hypot(self.u.real, self.w.real)
        else:
            u = self.u * exp(-1j * phase)
            w = self.w * exp(-1j * phase)
            return np.hypot(u.real, w.real)

    def _disp_norm_inst(
        self,
        phase: float,
    ) -> NDArray:
        """Instantaneous displacement magnitude

        :param phase: phase angle
        """
        u = 1j * self.u * exp(-1j * phase) / self.sol.omega
        w = 1j * self.w * exp(-1j * phase) / self.sol.omega
        norm = np.hypot(u.real, w.real)
        return norm

    def _compute_data(self) -> None:
        """Compute the velocity data and store them in respective attributes

        Scattering velocity field is computed on the polar grid and transformed
        to Cartesian coordinates for plotting.
        """
        arr_r = self.grid.arr_r
        arr_theta = self.grid.arr_theta

        for index, r in enumerate(arr_r):
            # Indexing
            min_index = index * self.grid.res_theta
            max_index = min_index + self.grid.res_theta

            # Coordinates
            xs, zs = s2c_coord(r, arr_theta)
            self._x.value[min_index:max_index] = xs
            self._z.value[min_index:max_index] = zs

            # Displacements Velocities
            u, w = self._compute_velocities(r, arr_theta)
            self._u.value[min_index:max_index] = u
            self._w.value[min_index:max_index] = w
            self._v_norm.value[min_index:max_index] = np.hypot(
                np.abs(u),
                np.abs(w),
            )

    def _compute_data_quiver(self) -> None:
        """Compute the velocity data for the quiver and store them in
        respective attributes

        Scattering velocity field is computed on the cartesian grid
        """
        arr_r = self.grid_quiver.flat_mesh_r
        arr_theta = self.grid_quiver.flat_mesh_theta
        u = np.zeros_like(arr_r, dtype=np.complex_)
        w = np.zeros_like(arr_r, dtype=np.complex_)
        for i, (r, theta) in enumerate(zip(arr_r, arr_theta)):
            u[i], w[i] = self._compute_velocities(r, theta)

        # convert vectors from polar coordinates to cartesian
        u_cartesian = np.cos(arr_theta) * u - np.sin(arr_theta) * w
        w_cartesian = np.sin(arr_theta) * u + np.cos(arr_theta) * w

        self._z_quiver.value[:] = self.grid_quiver.flat_mesh_z
        self._x_quiver.value[:] = self.grid_quiver.flat_mesh_x
        self._u_quiver.value[:] = u_cartesian
        self._w_quiver.value[:] = w_cartesian

    def get_velocity_quiver(
        self,
        phase: float = 0,
        mode: None | int = None,
        scattered: bool = True,
        incident: bool = True,
        symmetric: bool = True,
        animation: bool = True,
    ) -> tuple[NDArray, NDArray, NDArray, NDArray, float]:
        """Returns the velocity potential

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the magnitude of the pressure field at
        these points

        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        :param scattered: option if scattering field is plotted
        :param incident: option if incident field is plotted
        :param symmetric: return symmetric solution
        :param animation: are the arrows used in an animation
        """
        self._mode.value = mode
        self.scattered = scattered
        self.incident = incident

        u = self.u_quiver * exp(-1j * phase)
        w = self.w_quiver * exp(-1j * phase)

        # remove nan from u and w
        bools = np.isnan(u)
        u[bools] = 0
        w[bools] = 0

        if animation:
            norm = np.max(np.hypot(abs(u), abs(w)))
        else:
            norm = np.max(np.hypot(u.real, w.real))
        scale = self.n_quiver_points / 2 * norm

        z = self.z_quiver
        x = self.x_quiver
        if symmetric:
            z = np.concatenate([z, z])
            u = np.concatenate([u, u])

            x = np.concatenate([-x, x])
            w = np.concatenate([-w, w])

        return z, x, u.real, w.real, scale

    @abstractmethod
    def _compute_velocities(
        self,
        r: float,
        theta: float | NDArray,
    ) -> tuple[NDArray, NDArray]:
        """Compute the velocity data and return it

        :param arr_r: array of r-coordinates
        :param theta: polar angle
        """
        pass  # pragma: no cover


# -----------------------------------------------------------------------------
# ParticleScatteringData
# -----------------------------------------------------------------------------


class ParticleScatteringData(ScatteringFieldData):
    """Container for plotting data for the displacement field in the particle

    :param sol: solution
    :param res: resolution, if tuple (radial resolution, tangential resolution)
    :param n_quiver_points: anchor points along z for quiver arrows
    """

    def __init__(
        self,
        sol: BaseScattering,
        res: int | tuple[int, int] = 100,
        n_quiver_points: int = 21,
    ) -> None:
        """Constructor method"""

        r_min = self._EPS_r_min
        r_max = sol.R_0
        super().__init__(
            sol,
            r_min,
            r_max,
            res,
            n_quiver_points,
        )

    # -------------------------------------------------------------------------
    # Private Methods
    # -------------------------------------------------------------------------

    def _compute_velocities(
        self,
        r: NDArray,
        theta: float,
    ):
        """Compute the velocity data and return it

        :param arr_r: array of r-coordinates
        :param theta: polar angle
        """
        u = self.sol.radial_particle_velocity(r, theta, 0, self.mode)
        w = self.sol.tangential_particle_velocity(r, theta, 0, self.mode)
        return u, w


# -----------------------------------------------------------------------------
# FluidScatteringData
# -----------------------------------------------------------------------------


class FluidScatteringData(ScatteringFieldData):
    """Container for plotting data for the scattering field in the fluid

    :param sol: solution
    :param r_max: end point for tangential plotting range
    :param res: resolution, if tuple (radial resolution, tangential resolution)
    :param n_quiver_points: anchor points along z for quiver arrows
    """

    def __init__(
        self,
        sol: BaseScattering,
        r_max: float,
        scattering: bool = True,
        incident: bool = True,
        res: int | tuple[int, int] = 100,
        n_quiver_points: int = 21,
    ) -> None:
        """Constructor method"""

        r_min = sol.R_0
        super().__init__(
            sol,
            r_min,
            r_max,
            res,
            n_quiver_points,
        )

        self._scattered = PassiveVariable(
            scattering,
            "option: plot scattering field",
        )
        self._incident = PassiveVariable(
            incident,
            "option: plot incident field",
        )

        self._vel_pot = ActiveVariable(
            self._reset_complex_array,
            "velocity potential",
        )
        self._pressure = ActiveVariable(
            self._reset_complex_array,
            "acoustic pressure",
        )

        # Set links
        self._u.is_computed_by(self._scattered, self._incident)
        self._w.is_computed_by(self._scattered, self._incident)
        self._vel_pot.is_computed_by(self._sol, self._grid, self._mode)
        self._pressure.is_computed_by(self._sol, self._grid, self._mode)

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def get_pressure(
        self,
        instantaneous: bool = True,
        phase: float = 0,
        mode: None | int = None,
        scattered: bool = True,
        incident: bool = True,
    ) -> tuple[NDArray, NDArray, NDArray]:
        """Returns the velocity potential

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the magnitude of the pressure field at
        these points

        :param instantaneous: if ``True``, then instantaneous field
        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        :param scattered: option if scattering field is plotted
        :param incident: option if incident field is plotted
        """
        self._mode.value = mode
        self.scattered = scattered
        self.incident = incident
        if instantaneous:
            pressure_inst = self.pressure * exp(-1j * phase)
            return self.x, self.z, pressure_inst.real
        else:
            return self.x, self.z, np.abs(self.pressure)

    def get_velocity_potential(
        self,
        instantaneous: bool = True,
        phase: float = 0,
        mode: None | int = None,
        scattered: bool = True,
        incident: bool = True,
    ) -> tuple[NDArray, NDArray, NDArray]:
        """Returns the velocity potential

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the magnitude of the velocity potential field at
        these points

        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        :param scattered: option if scattering field is plotted
        :param incident: option if incident field is plotted
        """
        self._mode.value = mode
        self.scattered = scattered
        self.incident = incident
        if instantaneous:
            vel_pot_inst = self.velocity_potential * exp(-1j * phase)
            return self.x, self.z, vel_pot_inst.real
        else:
            return self.x, self.z, np.abs(self.velocity_potential)

    def get_velocity_magnitude(
        self,
        instantaneous: bool = True,
        phase: float = 0,
        mode: None | int = None,
        scattered: bool = True,
        incident: bool = True,
    ) -> tuple[NDArray, NDArray, NDArray]:
        """Returns the velocity magnitudes

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the magnitude of the velocity field at
        these points

        :param instantaneous: option if instantaneous or average magnitude
        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        :param scattered: option if scattering field is plotted
        :param incident: option if incident field is plotted
        """
        self.scattered = scattered
        self.incident = incident
        return super().get_velocity_magnitude(instantaneous, phase, mode)

    def get_velocity_vector(
        self,
        phase: float = 0,
        mode: None | int = None,
        scattered: bool = True,
        incident: bool = True,
    ) -> tuple[NDArray, NDArray, NDArray, NDArray]:
        """Returns the velocity vectors

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the velocity field vectors at
        these points

        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        :param scattered: option if scattering field is plotted
        :param incident: option if incident field is plotted
        """
        self.scattered = scattered
        self.incident = incident
        return super().get_velocity_vector(phase, mode)

    def get_displacement_vector(
        self,
        phase: float = 0,
        mode: None | int = None,
        scattered: bool = True,
        incident: bool = True,
    ) -> tuple[NDArray, NDArray, NDArray, NDArray]:
        """Returns the displacement vectors

        returns the coordinates of the points of the plotting grid `x`,
        `y` and the displacement field vectors at
        these points

        :param phase: phase angle
        :param mode: mode of oscillation, if `None` superposition
        :param scattered: option if scattering field is plotted
        :param incident: option if incident field is plotted
        """
        self.scattered = scattered
        self.incident = incident
        return super().get_displacement_vector(phase, mode)

    # -------------------------------------------------------------------------
    # Getters for Dependent Variables
    # -------------------------------------------------------------------------
    @property
    def velocity_potential(self) -> np.array:
        if np.all(self._vel_pot.value == 0):
            self._compute_velocity_potential()
        return self._vel_pot.value

    @property
    def pressure(self) -> np.array:
        if np.all(self._pressure.value == 0):
            self._compute_pressure()
        return self._pressure.value

    @property
    def scattered(self) -> bool:
        """Option if scattering field is plotted

        :getter: returns True (plot field) or False (do not plot field)
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._scattered.value

    @scattered.setter
    def scattered(self, value: bool) -> None:
        self._scattered.value = value

    @property
    def incident(self) -> bool:
        """Option if incident field is plotted

        :getter: returns True (plot field) or False (do not plot field)
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._incident.value

    @incident.setter
    def incident(self, value: bool) -> None:
        self._incident.value = value

    def _compute_pressure(self) -> None:
        """Compute the velocity data and store them in respective attributes

        Scattering velocity field is computed on the polar grid and transformed
        to Cartesian coordinates for plotting.
        """
        arr_r = self.grid.arr_r
        arr_theta = self.grid.arr_theta

        for index, r in enumerate(arr_r):
            # Indexing
            min_index = index * self.grid.res_theta
            max_index = min_index + self.grid.res_theta

            # Coordinates
            xs, zs = s2c_coord(r, arr_theta)
            self._x.value[min_index:max_index] = xs
            self._z.value[min_index:max_index] = zs

            # Pressure
            pressure = self.sol.pressure(
                r,
                arr_theta,
                0,
                self.scattered,
                self.incident,
                self.mode,
            )
            self._pressure.value[min_index:max_index] = pressure

    def _compute_velocity_potential(self) -> None:
        """Compute the velocity data and store them in respective attributes

        Scattering velocity field is computed on the polar grid and transformed
        to Cartesian coordinates for plotting.
        """
        arr_r = self.grid.arr_r
        arr_theta = self.grid.arr_theta

        for index, r in enumerate(arr_r):
            # Indexing
            min_index = index * self.grid.res_theta
            max_index = min_index + self.grid.res_theta

            # Coordinates
            xs, zs = s2c_coord(r, arr_theta)
            self._x.value[min_index:max_index] = xs
            self._z.value[min_index:max_index] = zs

            # Velocity Potential
            vel_pot = self.sol.velocity_potential(
                r,
                arr_theta,
                0,
                self.scattered,
                self.incident,
                self.mode,
            )
            self._vel_pot.value[min_index:max_index] = vel_pot

    # -------------------------------------------------------------------------
    # Private Methods
    # -------------------------------------------------------------------------

    def _compute_velocities(
        self,
        r: float,
        theta: float | NDArray,
    ) -> tuple[NDArray, NDArray]:
        """Compute the velocity data and return it

        :param r: radial coordinate
        :param theta: single value or array of tangential coordinates
        """
        u = self.sol.radial_acoustic_fluid_velocity(
            r,
            theta,
            0,
            self.scattered,
            self.incident,
            self.mode,
        )
        w = self.sol.tangential_acoustic_fluid_velocity(
            r,
            theta,
            0,
            self.scattered,
            self.incident,
            self.mode,
        )
        return u, w


if __name__ == "__main__":
    pass
