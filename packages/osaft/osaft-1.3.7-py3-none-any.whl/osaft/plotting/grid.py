from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np

from osaft.core.functions import (
    cartesian_2_spherical_coordinates as c2s_coord,
)
from osaft.core.functions import (
    spherical_2_cartesian_coordinates as s2c_coord,
)

NDArray = np.ndarray


class BaseGrid(ABC):
    """Base class for coordinate grids

    :param r_max: characteristic length of grid
    :param resolution: number of points, if tuple resolution in each direction
    :param is_upper: if ``True`` only grid in upper half of cartesian plane
    """

    _mesh_x: NDArray
    _mesh_z: NDArray
    _mesh_r: NDArray
    _mesh_theta: NDArray

    def __init__(
        self,
        r_max: float,
        resolution: int | tuple[int, int],
        is_upper: bool,
    ) -> None:

        self._upper = is_upper
        self._r_max = r_max
        self._res_x1, self._res_x2 = self.unpack_resolution(resolution)
        self._compute_mesh()

    # -------------------------------------------------------------------------
    # __init__ helper methods
    # -------------------------------------------------------------------------

    def unpack_resolution(
        self,
        resolution: int | tuple[int, int],
    ) -> tuple[int, int]:
        """Unpacks resolution tuple if needed

        if ``res`` is an `int` a tuple ``(res, res)`` is
        returned. If `res` is a tuple with two values, `res` is
        passed through.
        :param resolution: res of the grid
        """
        if isinstance(resolution, Sequence):
            if len(resolution) == 1:
                if self._upper:
                    return resolution[0], resolution[0] // 2
                else:
                    return resolution[0], resolution[0]
            elif len(resolution) == 2:
                return resolution
            else:
                raise ValueError(
                    "Resolution needs to be either one value for both "
                    "direction or a tuple of two values.",
                )
        else:
            if self._upper:
                return resolution, resolution // 2
            else:
                return resolution, resolution

    # -------------------------------------------------------------------------
    # User API
    # -------------------------------------------------------------------------

    @property
    def mesh_x(self) -> NDArray:
        """Mesh grid array of x-coordinates / ordinate of"""
        return self._mesh_x

    @property
    def mesh_z(self) -> NDArray:
        """Mesh grid array of z-coordinates / abscissa of grid points"""
        return self._mesh_z

    @property
    def mesh_r(self) -> NDArray:
        """Mesh grid array of radial coordinates of grid points"""
        return self._mesh_r

    @property
    def mesh_theta(self) -> NDArray:
        """Mesh grid array of tangential coordinates of grid points"""
        return self._mesh_theta

    @property
    def flat_mesh_x(self) -> NDArray:
        """Flattened mesh array of x-coordinates / ordinate
        grid points"""
        return self.mesh_x.flatten()

    @property
    def flat_mesh_z(self) -> NDArray:
        """Flattened mesh grid array of z-coordinates / abscissa grid points"""
        return self.mesh_z.flatten()

    @property
    def flat_mesh_r(self) -> NDArray:
        """Flattened mesh grid array of radial coordinates of grid points"""
        return self.mesh_r.flatten()

    @property
    def flat_mesh_theta(self) -> NDArray:
        """Flattened mesh grid array of tang. coordinates of grid points"""
        return self.mesh_theta.flatten()

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    @abstractmethod
    def _compute_mesh(self) -> None:
        pass  # pragma: no coverage


class PolarGrid(BaseGrid):
    """Polar coordinate grid for plotting

    Polar grid for radial coordinate between ``r_min`` and ``r_max``.

    :param r_min: smallest radius of polar grid
    :param r_max: largest radius of polar grid
    :param resolution: number of points, if tuple resolution in each direction
    :param is_upper: if ``True`` only grid in upper half of cartesian plane
    """

    def __init__(
        self,
        r_min: float,
        r_max: float,
        resolution: int | tuple[int, int],
        is_upper: bool,
    ) -> None:

        self._r_min = r_min
        super().__init__(r_max, resolution, is_upper)

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    @property
    def arr_r(self) -> NDArray:
        """Linearly spaced array in radial direction"""
        return np.linspace(self._r_min, self._r_max, self.res_r)

    @property
    def arr_theta(self) -> NDArray:
        """Linearly spaced array in tangential direction"""
        if self._upper:
            return np.linspace(0, np.pi, self.res_theta)
        else:
            return np.linspace(-np.pi, np.pi, self.res_theta)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def res_r(self) -> int:
        return self._res_x1

    @property
    def res_theta(self) -> int:
        return self._res_x2

    @property
    def dr(self) -> float:
        """Step size in radial direction"""
        return self.arr_r[1] - self.arr_r[0]

    @property
    def dtheta(self) -> float:
        """Step size in tangential direction"""
        return self.arr_theta[1] - self.arr_theta[0]

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def _compute_mesh(self) -> None:
        self._mesh_theta, self._mesh_r = np.meshgrid(
            self.arr_theta,
            self.arr_r,
        )
        self._mesh_x, self._mesh_z = s2c_coord(self._mesh_r, self._mesh_theta)


class PolarFluidGrid(PolarGrid):
    """Polar coordinate grid for the fluid domain for plotting

    :param R_0: scatterer radius
    :param r_max: largest radius of polar grid
    :param resolution: number of points, if tuple resolution in each direction
    :param is_upper: if ``True`` only grid in upper half of cartesian plane
    """

    def __init__(
        self,
        R_0: float,
        r_max: float,
        resolution: int | tuple[int, int],
        is_upper: bool,
    ) -> None:

        super().__init__(R_0, r_max, resolution, is_upper)


class PolarScattererGrid(PolarGrid):
    """Polar coordinate grid for the fluid domain for plotting

    :param R_0: scatterer radius
    :param resolution: number of points, if tuple resolution in each direction
    :param is_upper: if ``True`` only grid in upper half of cartesian plane
    """

    def __init__(
        self,
        R_0: float,
        resolution: int | tuple[int, int],
        is_upper: bool,
    ) -> None:

        super().__init__(1e-30, R_0, resolution, is_upper)


class CartesianGrid(BaseGrid):
    """Cartesian coordinate grid for plotting

    Cartesian grid for horizontal coordinate between ranging from ``-r_max`` to
    ``r_max`` and vertical coordinate ranging from ``0`` to ``r_max`` or from
    ``-r_max`` to ``r_max`` (see ``upper``).

    :param r_max: characteristic length of grid
    :param resolution: number of points, if tuple resolution in each direction
    :param is_upper: if ``True`` only grid in upper half of cartesian plane
    :param use_offset: if ``True`` center point is slightly offset,
       to avoid singularity
    """

    def __init__(
        self,
        r_max: float,
        resolution: int | tuple[int, int],
        is_upper: bool,
        use_offset: bool,
    ) -> None:
        """Constructor method"""

        self._offset = use_offset
        super().__init__(r_max, resolution, is_upper)

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    @property
    def arr_x(self) -> NDArray:
        """Linearly spaced array in x-direction"""
        if self._upper:
            return np.linspace(0, self._r_max, self.res_x)
        else:
            return np.linspace(-self._r_max, self._r_max, self.res_x)

    @property
    def arr_z(self) -> NDArray:
        """Linearly spaced array in z-direction

        if ``offset`` is ``True`` a slight offset is added to the center
        point to avoid possible singularities
        """
        arr = np.linspace(-self._r_max, self._r_max, self.res_z)
        if self.res_z % 2 and self._offset:
            arr[self.res_z // 2] = 1e-30
        return arr

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def res_x(self) -> int:
        return self._res_x2

    @property
    def res_z(self) -> int:
        return self._res_x1

    @property
    def dx(self) -> float:
        return self.arr_x[1] - self.arr_x[0]

    @property
    def dz(self) -> float:
        return self.arr_z[1] - self.arr_z[0]

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def _compute_mesh(self) -> None:
        self._mesh_z, self._mesh_x = np.meshgrid(self.arr_z, self.arr_x)
        self._mesh_r, self._mesh_theta = c2s_coord(self.mesh_x, self.mesh_z)


class MaskedCartesianGrid(CartesianGrid):
    """Masked cartesian coordinate grid for plotting

    Cartesian grid for horizontal coordinate ranging from ``-r_max`` to
    ``r_max`` and vertical coordinate ranging from ``0`` to ``r_max`` or from
    ``-r_max`` to ``r_max`` (see ``upper``). Either the inside of a circle
    of radius ``r_mask`` is masked (``inner = False``) or the outside is
    masked (``inner = True``).

    :param r_mask: radius of the masking circle
    :param r_max: characteristic length of grid
    :param resolution: number of points, if tuple resolution in each direction
    :param is_upper: if ``True`` only grid in upper half of cartesian plane
    :param inner: if ``True`` grid points inside circle, else outside
    :param use_offset: if ``True`` center point is slightly offset,
       to avoid singularity
    """

    def __init__(
        self,
        r_mask: float,
        r_max: float,
        resolution: int | tuple[int, int],
        is_upper: bool,
        inner: bool,
        use_offset: bool,
    ) -> None:
        self._inner = inner
        self._r_mask = r_mask
        super().__init__(r_max, resolution, is_upper, use_offset)

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def _compute_mesh(self) -> None:
        super()._compute_mesh()
        self._mask_grid()

    def _mask_grid(self) -> None:
        R = np.hypot(self._mesh_z, self._mesh_x)
        if self._inner:
            bools_cartesian = R <= self._r_mask
            bools_polar = self.mesh_r <= self._r_mask
        else:
            bools_cartesian = R >= self._r_mask
            bools_polar = self.mesh_r >= self._r_mask

        self._mesh_z = self._mesh_z[bools_cartesian]
        self._mesh_x = self._mesh_x[bools_cartesian]

        self._mesh_r = self._mesh_r[bools_polar]
        self._mesh_theta = self._mesh_theta[bools_polar]


class CartesianFluidGrid(MaskedCartesianGrid):
    """Masked cartesian coordinate grid of the fluid domain for plotting

    Cartesian grid for horizontal coordinate ranging from ``-r_max`` to
    ``r_max`` and vertical coordinate ranging from ``0`` to ``r_max`` or from
    ``-r_max`` to ``r_max`` (see ``upper``). The points inside the
    scatterer are masked/deleted.

    :param R_0: radius of the masking circle
    :param r_max: dimension of the grid
    :param resolution: number of points, if tuple resolution in each direction
    :param is_upper: if ``True`` only grid in upper half of cartesian plane
    """

    def __init__(
        self,
        R_0: float,
        r_max: float,
        resolution: int | tuple[int, int],
        is_upper: bool,
    ) -> None:

        super().__init__(R_0, r_max, resolution, is_upper, False, False)


class CartesianScattererGrid(MaskedCartesianGrid):
    """Masked cartesian coordinate grid of the scatterer domain for plotting

    Cartesian grid for horizontal coordinate ranging from ``-r_max`` to
    ``r_max`` and vertical coordinate ranging from ``0`` to ``r_max`` or from
    ``-r_max`` to ``r_max`` (see ``upper``). The points outside the
    scatterer are masked/deleted.

    :param R_0: radius of the scatterer
    :param resolution: number of points, if tuple resolution in each direction
    :param is_upper: if ``True`` only grid in upper half of cartesian plane
    :param use_offset: if ``True`` center point is slightly offset,
       to avoid singularity
    """

    def __init__(
        self,
        R_0: float,
        resolution: int | tuple[int, int],
        is_upper: bool,
        use_offset: bool = True,
    ) -> None:
        super().__init__(R_0, R_0, resolution, is_upper, True, use_offset)


if __name__ == "__main__":
    pass
