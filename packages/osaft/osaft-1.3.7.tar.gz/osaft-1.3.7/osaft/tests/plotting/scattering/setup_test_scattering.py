from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import Animation

from osaft import (
    FluidScatteringPlot,
    ParticleScatteringPlot,
    ParticleWireframePlot,
)
from osaft.plotting.scattering.base_plotter import BaseScatteringPlotter
from osaft.solutions.base_scattering import BaseScattering
from osaft.tests.plotting.basetest_plotting import BaseTestPlotting


class BaseTestScatteringPlotter(BaseTestPlotting):

    plot_cls: BaseScatteringPlotter

    def setUp(self) -> None:
        super().setUp()
        self.kwargs_options = {"mode": [None, 1, 1], "phase": [0, 1, 2]}
        self.name_prefix = ""

        if not self._is_base_class():
            self.plotting_cls = self._initialize_plotting_class()

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _generate_kwargs(self) -> dict:
        kwargs = dict()
        # Choose Values
        for key, value in self.kwargs_options.items():
            kwargs[key] = self.rng.choice(value)
        # Remove values from list
        for key, value in kwargs.items():
            self.kwargs_options[key].remove(value)
            if not self.kwargs_options[key]:
                self.kwargs_options.pop(key)
        return kwargs

    def _generate_animation_kwargs(self) -> dict:
        kwargs = self._generate_kwargs()
        try:
            kwargs.pop("phase")
            return kwargs
        except KeyError:
            return kwargs

    def _generate_evolution_kwargs(self) -> dict:
        return self._generate_animation_kwargs()

    @staticmethod
    def _name_from_kwargs(kwargs: dict) -> str:
        name = ""
        for key, value in kwargs.items():
            if isinstance(value, (bool, np.bool_)):
                if value:
                    name = f"{name}_{key}"
            elif value is not None or value != 0:
                name = f"{name}_{key}={value}"
        return name

    def _save_plot(self, fig: plt.Figure, kwargs: dict) -> None:
        name = self.name_prefix + self._name_from_kwargs(kwargs)
        self.save_fig(fig, name)

    @staticmethod
    def _handle_animation(animation: Animation) -> None:
        animation.resume()
        plt.show(block=False)
        plt.pause(1)
        plt.close("all")

    def _is_base_class(self) -> bool:
        return type(self) == BaseTestScatteringPlotter

    # -------------------------------------------------------------------------
    # Abstract Methods
    # -------------------------------------------------------------------------

    def _get_solution(self) -> BaseScattering:
        """Returns the solution class"""

    def _initialize_plotting_class(self) -> BaseScatteringPlotter:
        """Initializes the plotting class"""
        pass

    def _is_valid_field(self, kwargs: dict):
        return True

    def fcn_plot(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        pass

    def fcn_animate(self, **kwargs) -> Animation:
        pass

    def fcn_plot_evolution(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        pass

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_plot(self) -> None:
        if self._is_base_class():
            return
        while self.kwargs_options:
            kwargs = self._generate_kwargs()
            if self._is_valid_field(kwargs):
                fig, _ = self.fcn_plot(**kwargs)
                self._save_plot(fig, kwargs)
            else:
                self.assertRaises(ValueError, self.fcn_plot, **kwargs)

    def test_animation(self) -> None:
        if self._is_base_class():
            return
        while self.kwargs_options:
            kwargs = self._generate_animation_kwargs()
            if self._is_valid_field(kwargs):
                anim = self.fcn_animate(**kwargs)
                self._handle_animation(anim)
            else:
                self.assertRaises(ValueError, self.fcn_animate, **kwargs)

    def test_evolution(self) -> None:
        if self._is_base_class():
            return
        while self.kwargs_options:
            kwargs = self._generate_evolution_kwargs()
            if self._is_valid_field(kwargs):
                fig, _ = self.fcn_plot_evolution(**kwargs)
                self._save_plot(fig, kwargs)
            else:
                self.assertRaises(
                    ValueError, self.fcn_plot_evolution, **kwargs
                )


class BaseTestScatterTriPlotter(BaseTestScatteringPlotter):
    def setUp(self) -> None:
        super().setUp()
        self.tri_kwargs_options = {
            "inst": [True, True, False, False, False],
            "symmetric": [True, True, True, False, False, False],
            "tripcolor": [True, True, True, False],
            "cmap": ["jet", "magma"],
            "shading": ["flat", "flat"],
        }
        self.kwargs_options.update(self.tri_kwargs_options)

    def _is_base_class(self) -> bool:
        if super()._is_base_class():
            return True
        return type(self) == BaseTestScatterTriPlotter

    def _generate_animation_kwargs(self) -> dict:
        kwargs = super()._generate_animation_kwargs()
        try:
            kwargs.pop("inst")
            return kwargs
        except KeyError:
            return kwargs

    def _generate_evolution_kwargs(self) -> dict:
        kwargs = super()._generate_evolution_kwargs()
        kwargs_to_remove = ["inst", "cmap", "shading"]
        for kwarg in kwargs_to_remove:
            try:
                kwargs.pop(kwarg)
            except KeyError:
                pass
        return kwargs


class BaseTestFluidScatterPlotter(BaseTestScatterTriPlotter):
    def setUp(self) -> None:
        super().setUp()
        self.fluid_kwargs_options = {
            "scattered": [True, False, False],
            "incident": [True, False, False],
        }
        self.kwargs_options.update(self.fluid_kwargs_options)

    def _initialize_plotting_class(self) -> FluidScatteringPlot:
        sol = self._get_solution()
        r_max = 5 * sol.R_0
        plotting_cls = FluidScatteringPlot(sol, r_max=r_max)
        return plotting_cls

    def _is_valid_field(self, kwargs: dict) -> bool:
        if "scattered" not in kwargs or "incident" not in kwargs:
            return True
        if not kwargs["scattered"] and not kwargs["incident"]:
            return False
        return True

    def test_cmap(self) -> None:
        if self._is_base_class():
            return
        new_cmap = "grays"
        new_div_cmap = "RdYlBu"

        self.plotting_cls.cmap = new_cmap
        self.plotting_cls.div_cmap = new_div_cmap

        self.assertEqual(new_cmap, self.plotting_cls.cmap)
        self.assertEqual(new_div_cmap, self.plotting_cls.div_cmap)


class BaseTestFluidVelocityPlotter(BaseTestFluidScatterPlotter):
    def _is_base_class(self) -> bool:
        if super()._is_base_class():
            return True
        return type(self) == BaseTestFluidVelocityPlotter

    # -------------------------------------------------------------------------
    # Plotting Methods Implementations
    # -------------------------------------------------------------------------

    def fcn_plot(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_velocity(**kwargs)

    def fcn_animate(self, **kwargs) -> Animation:
        return self.plotting_cls.animate_velocity(**kwargs)

    def fcn_plot_evolution(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_velocity_evolution(**kwargs)


class BaseTestFluidPressurePlotter(BaseTestFluidScatterPlotter):
    def _is_base_class(self) -> bool:
        if super()._is_base_class():
            return True
        return type(self) == BaseTestFluidPressurePlotter

    # -------------------------------------------------------------------------
    # Plotting Methods Implementations
    # -------------------------------------------------------------------------

    def fcn_plot(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_pressure(**kwargs)

    def fcn_animate(self, **kwargs) -> Animation:
        return self.plotting_cls.animate_pressure(**kwargs)

    def fcn_plot_evolution(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_pressure_evolution(**kwargs)


class BaseTestFluidPotentialPlotter(BaseTestFluidScatterPlotter):
    def _is_base_class(self) -> bool:
        if super()._is_base_class():
            return True
        return type(self) == BaseTestFluidPotentialPlotter

    # -------------------------------------------------------------------------
    # Plotting Methods Implementations
    # -------------------------------------------------------------------------

    def fcn_plot(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_velocity_potential(**kwargs)

    def fcn_animate(self, **kwargs) -> Animation:
        return self.plotting_cls.animate_velocity_potential(**kwargs)

    def fcn_plot_evolution(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_velocity_potential_evolution(**kwargs)


class BaseTestFluidQuiverPlot(BaseTestFluidScatterPlotter):
    def setUp(self) -> None:
        super().setUp()
        # Add additional kwargs
        self.quiver_kwargs = {"quiver_color": [None, "black", "white"]}
        self.kwargs_options.update(self.quiver_kwargs)

    def _is_base_class(self) -> bool:
        if super()._is_base_class():
            return True
        return type(self) == BaseTestFluidQuiverPlot

    # -------------------------------------------------------------------------
    # Plotting Methods Implementations
    # -------------------------------------------------------------------------

    def fcn_plot(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_velocity(**kwargs)

    def fcn_animate(self, **kwargs) -> Animation:
        return self.plotting_cls.animate_velocity(**kwargs)

    def fcn_plot_evolution(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_velocity_evolution(**kwargs)


class BaseTestParticleScatterPlotter(BaseTestScatterTriPlotter):
    def setUp(self) -> None:
        super().setUp()
        # Add additional kwargs
        self.particle_kwargs_options = {
            "displacement": [True, False],
        }
        self.kwargs_options.update(self.particle_kwargs_options)

    def _is_base_class(self) -> bool:
        if super()._is_base_class():
            return True
        return type(self) == BaseTestParticleScatterPlotter

    def _initialize_plotting_class(self) -> ParticleScatteringPlot:
        plotting_cls = ParticleScatteringPlot(self._get_solution())
        return plotting_cls

    # -------------------------------------------------------------------------
    # Plotting Methods Implementations
    # -------------------------------------------------------------------------

    def fcn_plot(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_velocity(**kwargs)

    def fcn_animate(self, **kwargs) -> Animation:
        return self.plotting_cls.animate_velocity(**kwargs)

    def fcn_plot_evolution(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_velocity_evolution(**kwargs)


class BaseTestParticleQuiverPlot(BaseTestParticleScatterPlotter):
    def setUp(self) -> None:
        super().setUp()
        # Add additional kwargs
        self.quiver_kwargs = {"quiver_color": [None, "black", "white"]}
        self.kwargs_options.update(self.quiver_kwargs)

    def _is_base_class(self) -> bool:
        if super()._is_base_class():
            return True
        return type(self) == BaseTestParticleQuiverPlot


class BaseTestWireFrameScatterPlotter(BaseTestScatteringPlotter):
    def _is_base_class(self) -> bool:
        if super()._is_base_class():
            return True
        return type(self) == BaseTestWireFrameScatterPlotter

    def _initialize_plotting_class(self):
        plotting_cls = ParticleWireframePlot(self._get_solution())
        return plotting_cls

    # -------------------------------------------------------------------------
    # Plotting Methods Implementations
    # -------------------------------------------------------------------------

    def fcn_plot(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot(**kwargs)

    def fcn_animate(self, **kwargs) -> Animation:
        return self.plotting_cls.animate(**kwargs)

    def fcn_plot_evolution(self, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        return self.plotting_cls.plot_evolution(**kwargs)


if __name__ == "__main__":
    pass
