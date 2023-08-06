import matplotlib.pyplot as plt
from matplotlib.quiver import Quiver

from osaft.plotting.datacontainers.scattering_datacontainer import (
    ScatteringFieldData,
)


class BaseScatteringPlots:
    """Base class for the scattering plots. Defines :meth:`_overlay_quiver`"""

    data: ScatteringFieldData

    def _overlay_quiver(
        self,
        ax: plt.Axes,
        phase: float,
        scattered: bool,
        incident: bool,
        mode: int,
        symmetric: bool,
        quiver_color: str,
        animation: bool,
    ) -> Quiver:
        Z, X, U, W, scale = self.data.get_velocity_quiver(
            phase,
            mode,
            scattered,
            incident,
            symmetric,
            animation,
        )

        Q = ax.quiver(
            Z,
            X,
            U,
            W,
            color=quiver_color,
            pivot="tail",
            scale_units="width",
            scale=scale,
        )

        return Q
