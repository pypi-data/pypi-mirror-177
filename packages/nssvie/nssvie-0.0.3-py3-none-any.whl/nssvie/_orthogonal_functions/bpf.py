"""Block Pulse Functions.

Classes
-------
BlockPulseFunction
"""
from numpy import (
    array,
    eye,
    triu,
    ones,
    full,
    transpose,
    diagflat,
    multiply,
    arange
)

from scipy.integrate import quad, dblquad

from stochastic.processes import BrownianMotion


class BlockPulseFunctions:
    """
    Generate a :math:`m`-set of block pulse functions.

    Parameters
    ----------
    T : float, default 1.0
        The right hand side of the interval :math:`[0,T)`
    m : int, default 50
        The number of equidistant intervals to divide :math:`[0,T)`

    Attributes
    ----------
    h : float
        The width of one of the :math:`m` intervals.
    """

    def __init__(self, T=1.0, m=20):
        self.m = m
        self.T = float(T)
        self.h = float(T / m)

    def __str__(self):
        str_name = (
            f"{self.m}-Set of block pulse functions on [0, {self.T})"
        )
        return str_name

    def __repr__(self):
        repr_string = f"BlockPulseFunctions(m={self.m}, [0, {self.T}))"
        return repr_string

    def _bpf_i(self, i, t):
        """Calculates the value of a block pulse function at :math:`t`.

        .. math::

            \\phi_i(t) = \\begin{cases} 1 & , \\ (i-1)h \\leq t < ih \\\\
                0 & , \\text{ otherwise.} \\end{cases}.

        Parameters
        ----------
        i: int
            Block pulse function no. :math:`i`.
        t: float
            The value :math:`t`.

        Returns
        -------
        float
            :math:`\\phi_i(t)``
        """
        if (i - 1) * self.h <= t < i * self.h:
            return 1.0
        else:
            return 0.0

    def _bpf_vector(self, t):
        """Calculates the value of the :math:`m`-set of block pulse
        functions at :math:`t`.

        .. math::

            \\phi(t) = (\\phi_1(t), \\ldots , \\phi_m(t))

        Parameters
        ----------
        t: float
            The value :math:`t`.

        Returns
        -------
        :class:`numpy.ndarray`
            :math:`\\phi(t)`
        """
        return array([self._bpf_i(i, t) for i in range(1, self.m + 1)])

    def _coeff_i(self, i, f):
        """Calculates the block pulse coefficient.

        .. math::

            f_i = \\frac{1}{h} \\int\\limits_0^T f(t) \\phi_i(t) dt

        For calculation of the definite integral
        :external:func:`scipy.integrate.quad` is used.

        Parameters
        ----------
        i: int
            Block pulse coefficient no. :math:`i`.
        f: callable
            The function :math:`f`.

        Returns
        -------
        float
            The block pulse function coefficient :math:`f_i` for the
            function :math:`f`.
        """
        return float(
            (1 / self.h)
            * quad(
                f,
                (i-1) * self.h,
                i * self.h)[0]
        )

    def _coeff_vector(self, f):
        """Calculates the block pulse coefficient vector.

        .. math::

            F = (f_1 , \\ldots, f_m)

        Parameters
        ----------
        f: callable
            The function :math:`f`.

        Returns
        -------
        :class:`numpy.ndarray`
            The block pulse function coefficient vector :math:`F` for
            the function :math:`f`.
        """
        return array([self._coeff_i(i, f) for i in range(1, self.m + 1)]).T

    def _coeff_ij(self, i, j, f):
        """Calculate the block pulse coefficient.

        .. math::

            k_{ij} = \\frac{1}{h^2} \\int\\limits_0^T \\int\\limits_0^T
                k(s,t) \\phi_i(s) \\phi_j(t) dt ds

        For calculation of the definite integral
        :external:func:`scipy.integrate.dblquad` is used.

        Parameters
        ----------
        i,j: int
            Block pulse coefficient no. :math:`i,j`.
        f: callable
            The function :math:`f`.

        Returns
        -------
        float
            Block pulse coefficient :math:`k_{ij`.
        """
        return dblquad(
            f,
            (i-1) * self.h,
            i * self.h,
            (j-1) * self.h,
            j * self.h,
        )[0]

    def _coeff_matrix(self, k):
        """Calculate the block pulse coefficient matrix.

        .. math::

            K = (k_{ij})_{i,j = 1 , \\ldots , m}

        Parameters
        ----------
        k:  callable
            The function :math:`k`.

        Returns
        -------
        :class:`numpy.ndarray`
            Block pulse coefficient matrix :math:`K`.
        """

        # Switch variables, see `scipy.integrate.dblquad`
        def k_var_switched(second_var, first_var):
            return k(first_var, second_var)

        K = array(
            [
                [
                    self._coeff_ij(i, j, k_var_switched)
                    for j in range(1, self.m + 1)
                ]
                for i in range(1, self.m + 1)
            ]
        )
        return self.h ** (-2) * K

    def _operational_matrix_of_integration(self):
        """Calculates the operational matrix of integration.

        .. math::

            P = \\frac{h}{2} \\begin{pmatrix} 1 & 2 & 2 & \\ldots & 2
                \\\\ 0 & 1 & 2 & \\ldots & 2 \\\\ 0 & 0 & 1 & \\ldots &
                2 \\\\ \\vdots & \\vdots & \\vdots & \\ddots & \\vdots
                \\\\ 0 & 0 & 0 & \\ldots & 1 \\end{pmatrix}

        Returns
        -------
        :class:`numpy.ndarray`
            Operational matrix of integration :math:`P`.

        Notes
        -----
        For detail see `Maleknejad et. al (2012)
        <https://www.sciencedirect.com/science/article/pii/
        S0895717711005504/>`_
        """
        # Construct the diagonal part
        diagonal = eye(self.m)

        # Contruct the upper triangular part
        upper_triu = triu(2 * ones((self.m, self.m)), k=1)

        return self.h * 0.5 * (diagonal + upper_triu)

    def _stochastic_operational_matrix_of_integration(self):
        """Calculates the stochastic operational matrix of integration.

        .. math::

            P = \\frac{h}{2} \\begin{pmatrix} B_{0.5h} & B_h & B_h &
                \\ldots & B_h \\\\ 0 & B_{1.5h} - B_h & B_{2h} - B_h &
                \\ldots & B_{2h} - B_h \\\\ 0 & 0 & B_{2.5h} - B_{2h} &
                \\ldots & B_{2h} - B_{2h} \\\\ \\vdots & \\vdots &
                \\vdots & \\ddots & \\vdots \\\\ 0 & 0 & 0 & \\ldots &
                B_{(m-0.5)h} - B_{(m-1)h} \\end{pmatrix}

        where :math:`B_t` is the Brownian motion. For sampling the
        Brownian motion
        :class:`stochastic.processes.continuous.BrownianMotion` is used.

        Returns
        -------
        :class:`numpy.ndarray`
            Stochastical operational matrix of integration :math:`P_S`.

        Notes
        -----
        For detail see `Maleknejad et. al (2012)
        <https://www.sciencedirect.com/science/article/pii/
        S0895717711005504/>`_
        """
        bb = BrownianMotion(drift=0, scale=1, t=self.T)

        # Generate a sample from the Brownian Motion
        bb_sample = bb.sample_at(
            [i * self.h for i in arange(0, self.m + 0.5, 0.5)]
        )

        # Construct the upper triangular part
        const_column = [
            bb_sample[i] - bb_sample[i-2]
            for i in range(2, 2*self.m + 2, 2)
        ]
        triu_matrix = triu(
            full((self.m, self.m), transpose([const_column])),
            k=1
        )

        # Construct the diagonal part
        diagonal = [
            (bb_sample[i] - bb_sample[i - 1])
            for i in range(1, 2*self.m, 2)
        ]
        diag_matrix = diagflat(diagonal)

        return (diag_matrix + triu_matrix)

    def _matrix_b1(self, kernel_1):
        """Generates the matrix :math:`B_1`from the article
        `Maleknejad et. al (2012)
        <https://www.sciencedirect.com/science/article/pii/
        S0895717711005504/>`_.

        Parameters
        ----------
        kernel_1: callable

        Returns
        -------
        :class:`numpy.ndarray`
            Matrix ``B_1``.
        """
        return multiply(
            self._operational_matrix_of_integration(),
            self._coeff_matrix(kernel_1),
        )

    def _matrix_b2(self, kernel_2):
        """Generates the matrix :math:`B_2`from the article
        `Maleknejad et. al (2012)
        <https://www.sciencedirect.com/science/article/pii/
        S0895717711005504/>`_.

        Parameter
        ---------
        kernel_2: callable

        Returns
        -------
        :class:`numpy.ndarray`
            Matrix ``B_2``.
        """
        return multiply(
            self._stochastic_operational_matrix_of_integration(),
            self._coeff_matrix(kernel_2),
        )
