from osaft import WaveType
from osaft.solutions import (
    doinikov1994compressible,
    doinikov1994rigid,
    doinikov2021viscoelastic,
    doinikov2021viscous,
    gorkov1962,
    hasegawa1969,
    king1934,
    settnes2012,
    yosioka1955,
)
from osaft.tests.testing_parameters import RandomParameters


class SolutionFactory:

    parameters = RandomParameters()

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def king_1934_base(self, new: bool = False) -> king1934.BaseKing:
        """Returns an initiated class of ``king1934.BaseKing``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()
        sol = king1934.BaseKing(
            self.f,
            self.R_0,
            self.rho_s,
            self.rho_f,
            self.c_f,
            self.p_0,
            self.wave_type,
            self.position,
        )
        return sol

    def king_1934_scattering(
        self,
        new: bool = False,
    ) -> king1934.ScatteringField:
        """Returns an initiated class of ``king1934.ScatteringField``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()
        sol = king1934.ScatteringField(
            self.f,
            self.R_0,
            self.rho_s,
            self.rho_f,
            self.c_f,
            self.p_0,
            self.wave_type,
            self.position,
        )
        return sol

    def king_1934_arf(self, new: bool = False) -> king1934.ARF:
        """Returns an initiated class of ``king1934.ARF``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()
        sol = king1934.ARF(
            self.f,
            self.R_0,
            self.rho_s,
            self.rho_f,
            self.c_f,
            self.p_0,
            self.wave_type,
            self.position,
        )
        return sol

    def gorkov_1962_arf(self, new: bool = False) -> gorkov1962.ARF:
        """Returns an initiated class of ``gorkov1962.ARF``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = gorkov1962.ARF(
            self.f,
            self.R_0,
            self.rho_s,
            self.parameters.c_s,
            self.rho_f,
            self.c_f,
            self.p_0,
            self.wave_type,
            self.position,
        )
        return sol

    def yosioka_1955_base(
        self,
        new: bool = False,
    ) -> yosioka1955.BaseYosioka:
        """Returns an initiated class of ``yosioka1955.BaseYosioka``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = yosioka1955.BaseYosioka(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            c_s=self.c_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )

        return sol

    def yosioka_1955_scattering(
        self,
        new: bool = False,
    ) -> yosioka1955.ScatteringField:
        """Returns an initiated class of ``yosioka1955.ScatteringField``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = yosioka1955.ScatteringField(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            c_s=self.c_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )

        return sol

    def yosioka_1955_arf(
        self,
        new: bool = False,
    ) -> yosioka1955.ARF:
        """Returns an initiated class of ``yosioka1955.ARF``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = yosioka1955.ARF(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            c_s=self.c_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )

        return sol

    def hasegawa_1969_base(
        self,
        new: bool = False,
    ) -> hasegawa1969.BaseHasegawa:
        """Returns an initiated class of ``hasegawa1969.BaseHasegawa``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = hasegawa1969.BaseHasegawa(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            E_s=self.E_s,
            nu_s=self.nu_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )
        return sol

    def hasegawa_1969_scattering(
        self,
        new: bool = False,
    ) -> hasegawa1969.ScatteringField:
        """Returns an initiated class of ``hasegawa1969.ScatteringField``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = hasegawa1969.ScatteringField(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            E_s=self.E_s,
            nu_s=self.nu_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )
        return sol

    def hasegawa_1969_arf(
        self,
        new: bool = False,
    ) -> hasegawa1969.ARF:
        """Returns an initiated class of ``hasegawa1969.ARF``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = hasegawa1969.ARF(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            E_s=self.E_s,
            nu_s=self.nu_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )
        return sol

    def doinikov_1994_rigid_scattering(
        self,
        new: bool = False,
    ) -> doinikov1994rigid.ScatteringField:
        """Returns an initiated class of ``doinikov1994rigid.ScatteringField``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = doinikov1994rigid.ScatteringField(
            self.f,
            self.R_0,
            self.rho_s,
            self.rho_f,
            self.c_f,
            self.eta_f,
            self.zeta_f,
            self.p_0,
            self.wave_type,
            self.position,
        )
        return sol

    def doinikov_1994_rigid_arf(
        self,
        new: bool = False,
    ) -> doinikov1994rigid.ARF:
        """Returns an initiated class of ``doinikov1994rigid.ARF``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = doinikov1994rigid.ARF(
            self.f,
            self.R_0,
            self.rho_s,
            self.rho_f,
            self.c_f,
            self.eta_f,
            self.zeta_f,
            self.p_0,
            self.wave_type,
            self.position,
        )
        return sol

    def doinikov_1994_compressible_scattering(
        self,
        new: bool = False,
    ) -> doinikov1994compressible.ScatteringField:
        """Returns an initiated class of
        ``doinikov1994compressible.ScatteringField``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = doinikov1994compressible.ScatteringField(
            self.f,
            self.R_0,
            self.rho_s,
            self.c_s,
            self.eta_s,
            self.zeta_s,
            self.rho_f,
            self.c_f,
            self.eta_f,
            self.zeta_f,
            self.p_0,
            self.wave_type,
            self.position,
        )
        return sol

    def doinikov_1994_compressible_arf(
        self,
        new: bool = False,
    ) -> doinikov1994compressible.ARF:
        """Returns an initiated class of ``doinikov1994compressible.ARF``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = doinikov1994compressible.ARF(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            c_s=self.c_s,
            eta_s=self.eta_s,
            zeta_s=self.zeta_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            eta_f=self.eta_f,
            zeta_f=self.zeta_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )
        return sol

    def settnes_2012_arf(
        self,
        new: bool = False,
    ) -> settnes2012.ARF:
        """Returns an initiated class of ``settnes2021.ARF``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = settnes2012.ARF(
            self.f,
            self.R_0,
            self.rho_s,
            self.c_s,
            self.rho_f,
            self.c_f,
            self.eta_f,
            self.p_0,
            self.wave_type,
            self.position,
        )
        return sol

    def doinikov_2021_viscous_scattering(
        self,
        new: bool = False,
    ) -> doinikov2021viscous.ScatteringField:
        """Returns an initiated class of
        ``doinikov2021viscous.ScatteringField``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = doinikov2021viscous.ScatteringField(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            E_s=self.E_s,
            nu_s=self.nu_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            eta_f=self.eta_f,
            zeta_f=self.zeta_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )
        return sol

    def doinikov_2021_viscous_streaming(
        self,
        new: bool = False,
    ) -> doinikov2021viscous.StreamingField:
        """Returns an initiated class of ``doinikov2021viscous.StreamingField``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = doinikov2021viscous.StreamingField(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            E_s=self.E_s,
            nu_s=self.nu_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            eta_f=self.eta_f,
            zeta_f=self.zeta_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )
        return sol

    def doinikov_2021_viscous_arf(
        self,
        new: bool = False,
    ) -> doinikov2021viscous.ARF:
        """Returns an initiated class of ``doinikov2021viscous.ARF``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = doinikov2021viscous.ARF(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            E_s=self.E_s,
            nu_s=self.nu_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            eta_f=self.eta_f,
            zeta_f=self.zeta_f,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )
        return sol

    def doinikov_2021_viscoelastic_scattering(
        self,
        new: bool = False,
    ) -> doinikov2021viscoelastic.ScatteringField:
        """Returns an initiated class of
        ``doinikov2021viscoelastic.ScatteringField``

        :param new: if ``True`` new random parameter values are computed
        """
        if new:
            self.parameters.change_all()

        sol = doinikov2021viscoelastic.ScatteringField(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s,
            E_s=self.E_s,
            nu_s=self.nu_s,
            rho_f=self.rho_f,
            c_f=self.c_f,
            eta_f=self.eta_f,
            zeta_f=self.zeta_f,
            eta_p=self.eta_p,
            zeta_p=self.eta_p,
            lambda_M=self.lambda_M,
            p_0=self.p_0,
            wave_type=self.wave_type,
            position=self.position,
        )
        return sol

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


if __name__ == "__main__":
    pass
