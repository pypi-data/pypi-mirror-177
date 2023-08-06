from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.quiver import Quiver

from osaft.core.functions import pi
from osaft.plotting.datacontainers.scattering_datacontainer import (
    ParticleScatteringData,
)
from osaft.plotting.datacontainers.wireframe_datacontainer import (
    ParticleWireframeData,
)
from osaft.plotting.scattering.base_plotter import BaseScatteringPlotter
from osaft.plotting.scattering.base_scattering_plots import (
    BaseScatteringPlots,
)
from osaft.plotting.scattering.tri_plotter import TriangulationPlotter
from osaft.plotting.scattering.wireframe_plotter import WireframePlotter
from osaft.solutions.base_scattering import BaseScattering

NDArray = np.ndarray


class ParticleScatteringPlot(BaseScatteringPlots):
    """Class for plotting scattering field of the particle

    Plots the acoustic field inside the particle using Matplotlib
    tricontourf or tripcolor plotting methods.

    :param sol: solution to be plotted
    :param resolution: if tuple (radial resolution, tangential resolution)
    :param n_quiver_points: anchor points along z for quiver
    :param cmap: color map
    """

    def __init__(
        self,
        sol: BaseScattering,
        resolution: int | tuple[int, int] = 100,
        n_quiver_points: int = 21,
        cmap: str = "winter",
    ):
        """Constructor method"""
        self.data = ParticleScatteringData(
            sol,
            resolution,
            n_quiver_points,
        )
        self.plotter = TriangulationPlotter(True, cmap)

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def plot_velocity(
        self,
        inst: bool = True,
        phase: float = 0,
        mode: None | int = None,
        displacement: bool = False,
        symmetric: bool = True,
        quiver_color: None | str = None,
        tripcolor: bool = False,
        ax: None | plt.Axes = None,
        **kwargs,
    ) -> tuple[plt.Figure, plt.Axes]:
        """Tricontourf plot for acoustic velocity field of the particle

        Plots the velocity amplitude of the first-order acoustic velocity field
        of the particle using Matplotlib's
        `tricontourf
        <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tricontour.html>`_
        or
        `tripcolor
        <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tripcolor.html>`_
        if ``tripcolor = True``.

        :param inst: if ``True`` instantaneous amplitude is plotted
        :param phase: phase :math:`[0, 2\\pi]`
        :param mode: mode of oscillation
        :param displacement: if ``True`` displacement, else velocity plot
        :param symmetric: if ``True`` the symmetry of the solution is used
        :param quiver_color: color of the quiver arrows, if None: no arrows
        :param tripcolor: switches between tripcolor and tricontourf plot
        :param ax: Axes object
        :param kwargs: passed through to tricontourf()
        """

        fig, ax = self._triangulation_plot(
            tripcolor=tripcolor,
            inst=inst,
            phase=phase,
            mode=mode,
            displacement=displacement,
            symmetric=symmetric,
            ax=ax,
            **kwargs,
        )

        if quiver_color:
            # particle plots does not a distinction between scattered and
            # incident field
            scattered = incident = False
            self._overlay_quiver(
                ax,
                phase,
                scattered,
                incident,
                mode,
                symmetric,
                quiver_color,
                animation=False,
            )

        return fig, ax

    def animate_velocity(
        self,
        frames: int = 64,
        interval: float = 100.0,
        mode: None | int = None,
        displacement: bool = True,
        symmetric: bool = True,
        quiver_color: None | str = None,
        tripcolor: bool = False,
        ax: None | plt.Axes = None,
        **kwargs,
    ) -> FuncAnimation:
        """Tricontourf animation for acoustic velocity field of the particle

        Animates the velocity amplitude of the first-order acoustic velocity
        field of the particle over one period using Matplotlib's
        `tricontourf
        <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tricontour.html>`_
        or
        `tripcolor
        <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tripcolor.html>`_
        if ``tripcolor = True``.


        :param frames: number of frames for the animation
        :param interval: interval between frames in ms
        :param mode: mode of oscillation
        :param displacement: if ``True`` displacement, else velocity plot
        :param symmetric: if ``True`` the symmetry of the solution is used
        :param quiver_color: color of the quiver arrows, if None: no arrows
        :param tripcolor: switches between tripcolor and tricontourf plot
        :param ax: Axes object
        :param kwargs: passed through to tricontourf()
        """

        if quiver_color:

            fig, ax = self.plot_velocity(
                inst=False,
                mode=mode,
                symmetric=symmetric,
            )

            # no scattered or incident field for scatterer
            scattered = incident = False
            Q = self._overlay_quiver(
                ax,
                0,
                scattered,
                incident,
                mode,
                symmetric,
                animation=True,
                quiver_color=quiver_color,
            )
            annotation = self.plotter._annotate_phase(ax, 0)

            def animate_quiver(frame: int, frames: int, Q: Quiver, annotation):
                phase = frame / frames * 2 * pi

                _, _, u, w, _ = self.data.get_velocity_quiver(
                    phase,
                    mode,
                    scattered,
                    incident,
                    symmetric,
                    animation=True,
                )

                self.plotter._update_phase_annotation(annotation, phase)

                Q.set_UVC(u, w)

                return (Q,)

            anim = FuncAnimation(
                fig,
                animate_quiver,
                frames=frames,
                interval=interval,
                blit=False,
                fargs=(frames, Q, annotation),
            )

            return anim
        else:
            return self._triangulation_animation(
                tripcolor=tripcolor,
                frames=frames,
                interval=interval,
                mode=mode,
                displacement=displacement,
                symmetric=symmetric,
                ax=ax,
                **kwargs,
            )

    # -------------------------------------------------------------------------
    # Private Methods
    # -------------------------------------------------------------------------

    def _triangulation_plot(
        self,
        tripcolor: bool,
        inst: bool,
        phase: float,
        mode: None | int,
        displacement: bool,
        symmetric: bool,
        ax: None | plt.Axes,
        **kwargs,
    ) -> tuple[plt.Figure, plt.Axes]:
        """Helper function for tripcolor/tricontourf plot

        :param tripcolor: if ``True`` tripcolor, else tricontourf plot
        :param inst: if ``True`` instantaneous amplitude is plotted
        :param phase: phase :math:`[0, 2\\pi]`
        :param mode: mode of oscillation
        :param displacement: if ``True`` displacement, else velocity plot
        :param symmetric: if ``True`` the symmetry of the solution is used
        :param ax: Axes object
        :param kwargs: passed through to plotting method
        """

        # Data
        if displacement:
            X, Z, C = self.data.get_displacement_magnitude(inst, phase, mode)
            cbar_label = "Displacement [m]"
        else:
            X, Z, C = self.data.get_velocity_magnitude(inst, phase, mode)
            cbar_label = "Velocity [m/s]"
        # Replace nan in the center
        C[0] = C[1]
        # Plot
        fig, ax, _, _, _ = self.plotter.plot(
            X=Z,
            Y=X,
            C=C,
            radius=self.data.sol.R_0,
            symmetric=symmetric,
            tripcolor=tripcolor,
            cbar_label=cbar_label,
            use_diverging_cmap=False,
            ax=ax,
            **kwargs,
        )
        return fig, ax

    def _triangulation_animation(
        self,
        tripcolor: bool,
        frames: int,
        interval: float,
        mode: None | int,
        displacement: bool,
        symmetric: bool,
        ax: None | plt.Axes,
        **kwargs,
    ) -> FuncAnimation:
        """Helper function for tripcolor/tricontourf animation

        :param tripcolor: if ``True`` tripcolor, else tricontourf plot
        :param frames: number of frames for the animation
        :param interval: interval between frames in ms
        :param mode: mode of oscillation
        :param displacement: if ``True`` displacement, else velocity plot
        :param symmetric: if ``True`` the symmetry of the solution is used
        :param ax: Axes object
        :param kwargs: passed through to tricontourf()
        """

        # Data function for animation
        def data_func(phase: float) -> tuple[NDArray, NDArray, NDArray]:
            """Returns the velocity field for given phase
            Closure is used to fix all additional parameters
            :param phase: phase
            """
            if displacement:
                return self.data.get_displacement_magnitude(True, phase, mode)
            else:
                return self.data.get_velocity_magnitude(True, phase, mode)

        # Color bar label
        if displacement:
            cbar_label = "Displacement [m]"
        else:
            cbar_label = "Velocity [m/s]"

        # Get norm
        if displacement:
            _, _, C = self.data.get_displacement_magnitude(False, mode=mode)
        else:
            _, _, C = self.data.get_velocity_magnitude(False, mode=mode)

        return self.plotter.animate(
            frames=frames,
            interval=interval,
            tripcolor=tripcolor,
            symmetric=symmetric,
            cbar_label=cbar_label,
            use_diverging_cmap=False,
            animate_meth=data_func,
            C_norm=C,
            radius=self.data.sol.R_0,
            ax=ax,
            **kwargs,
        )

    def plot_velocity_evolution(
        self,
        inst: bool = True,
        mode: None | int = None,
        displacement: bool = False,
        symmetric: bool = True,
        quiver_color: str = None,
        tripcolor: bool = False,
        layout: tuple[int, int] = (3, 3),
        **kwargs,
    ) -> tuple[plt.Figure, plt.Axes]:
        """Tricontourf plot for acoustic velocity field evolution of the
        particle

        Plots the velocity amplitude of the first-order acoustic velocity
        field of the fluid over one period at different phases using
        Matplotlib's
        `tricontourf
        <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tricontour.html>`_
        or
        `tripcolor
        <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tripcolor.html>`_
        if ``tripcolor = True``.

        The first phase value is always :math:`0\\pi` and the last one
        :math:`2\\pi`. The total number of plots and, hence, also the steps
        between the different phase values is the defined by the product of the
        ``layout`` tuple.

        :param inst: if ``True`` instantaneous amplitude is plotted
        :param mode: mode of oscillation
        :param displacement: if ``True`` displacement, else velocity plot
        :param symmetric: if ``True`` the symmetry of the solution is used
        :param quiver_color: color of the quiver arrows, if None: no arrows
        :param tripcolor: switches between tripcolor and tricontourf plot
        :param layout: number of rows and columns for plotting
        :param kwargs: passed through to the parent subplots command
        """

        n_row, n_col = layout
        n = n_col * n_row

        phases = np.linspace(0, 2, num=n)

        fig, axes = plt.subplots(
            n_row,
            n_col,
            sharex=True,
            sharey=True,
            **kwargs,
        )

        # Data
        if displacement:
            cbar_label = "Displacement [m]"
        else:
            cbar_label = "Velocity [m/s]"

        # Data function for subplots
        def data_func(phase: float) -> tuple[NDArray, NDArray, NDArray]:
            """Returns the velocity field for given phase
            Closure is used to fix all additional parameters
            :param phase: phase
            """
            if displacement:
                return self.data.get_displacement_magnitude(inst, phase, mode)
            else:
                return self.data.get_velocity_magnitude(inst, phase, mode)

        # Get norm
        if displacement:
            _, _, C_norm = self.data.get_displacement_magnitude(
                False,
                mode=mode,
            )
        else:
            _, _, C_norm = self.data.get_velocity_magnitude(False, mode=mode)

        for i, phase in enumerate(phases):

            row = i // n_col
            col = i % n_col
            ax = axes.flat[i]

            X, Z, C = data_func(phase=phase * np.pi)
            # Replace nan in the center
            C[0] = C[1]

            # Plot
            _, _, cnf, cbar, _ = self.plotter.plot(
                X=Z,
                Y=X,
                C=C,
                radius=self.data.sol.R_0,
                symmetric=symmetric,
                tripcolor=tripcolor,
                cbar_label=cbar_label,
                use_diverging_cmap=False,
                ax=ax,
                vmin=0,
                vmax=1.01 * np.nanmax(C_norm),
            )
            if quiver_color:
                # particle plots does not a distinction between scattered and
                # incident field
                scattered = incident = False
                self._overlay_quiver(
                    ax,
                    phase,
                    scattered,
                    incident,
                    mode,
                    symmetric,
                    animation=False,
                    quiver_color=quiver_color,
                )
            # remove colorbar
            cbar.remove()

            ax.set_title(f"{phase:.2f}" + r"$\pi$")

            if row != (n_row - 1):
                ax.set_xlabel("")
            if col > 0:
                ax.set_ylabel("")

        fig.tight_layout()
        cbar = fig.colorbar(cnf, ax=axes.ravel().tolist())
        cbar.ax.set_ylabel(cbar_label)

        return fig, axes


class ParticleWireframePlot(BaseScatteringPlotter):
    """Plotting class for wireframe plot of the particle

    :param sol: solution to be plotted
    :param nbr_r_levels: number of circles shown in the wireframe
    :param nbr_theta_levels: number of radii shown in the wireframe
    :param resolution: resolution, if tuple `(radial res, tangential res)`
    :param scale_factor: scaling factor for the displacements, if ``None`` auto
    """

    def __init__(
        self,
        sol: BaseScattering,
        nbr_r_levels: int = 10,
        nbr_theta_levels: int = 10,
        resolution: int | tuple[int, int] = (100, 100),
        scale_factor: float = 0.1,
    ) -> None:
        # Call to parent class
        super().__init__(True)

        self.data = ParticleWireframeData(
            sol,
            nbr_r_levels,
            nbr_theta_levels,
            resolution,
            scale_factor,
        )
        self.plotter = WireframePlotter()

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def plot(
        self,
        phase: float = 0,
        mode: None | int = None,
        ax: None | plt.Axes = None,
    ) -> tuple[plt.Figure, plt.Axes]:
        """Plot wireframe

        :param phase: phase to be plotted
        :param mode: mode to be plotted, if ``None`` superposition of all modes
        :param ax: if ``ax`` is passed, plot will be drawn on ``ax``
        """
        self.data.mode = mode
        radii, circles = self.data.get_displacements()
        fig, ax = self.plotter.plot(radii, circles, phase, ax)

        return fig, ax

    def animate(
        self,
        frames: int = 64,
        interval: float = 100.0,
        mode: None | int = None,
        ax: None | plt.Axes = None,
    ):
        """Animate wireframe

        :param frames: number of frames for the animation
        :param interval: interval between frames in milliseconds
        :param mode: mode to be plotted, if ``None`` superposition of all modes
        :param ax: if ``ax`` is passed, plot will be drawn on ``ax``
        """
        self.data.mode = mode
        anim = self.plotter.animate(
            frames=frames,
            interval=interval,
            deformed_radii=self.data.deformed_radii,
            deformed_circles=self.data.deformed_circles,
            ax=ax,
        )
        return anim

    def plot_evolution(
        self,
        mode: None | int = None,
        layout: tuple[int, int] = (3, 3),
        **kwargs,
    ) -> tuple[plt.Figure, plt.Axes]:
        """Plot wireframe over one period

        :param layout: subplot layout of the figure
        :param mode: mode to be plotted, if ``None`` superposition of all modes
        """

        self.data.mode = mode
        n_row, n_col = layout
        n = n_col * n_row

        phases = np.linspace(0, 2, num=n)

        fig, axes = plt.subplots(
            n_row,
            n_col,
            sharex=True,
            sharey=True,
            **kwargs,
        )

        for i, phase in enumerate(phases):

            row = i // n_col
            col = i % n_col
            ax = axes.flat[i]

            radii, circles = self.data.get_displacements()
            _, _ = self.plotter.plot(radii, circles, phase * np.pi, ax)

            ax.set_title(f"{phase:.2f}" + r"$\pi$")

            if row != (n_row - 1):
                ax.set_xlabel("")
            if col > 0:
                ax.set_ylabel("")

        fig.tight_layout()
        return fig, axes


if __name__ == "__main__":
    pass
