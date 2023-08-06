"""
A python package for computing a numerical solution of stochastic
Volterra integral equations of the second kind based on block pulse
functions as suggested in `Maleknejad et. al (2012)
<https://www.sciencedirect.com/science/article/pii/S0895717711005504/>`_

In this package we implemented the suggested methods from the cited
paper. For a detailed theoretical background we refer to this paper.
"""
from nssvie._integral_equations import SVIE

__all__ = ["SVIE"]                                          # noqa: F401

from nssvie._version import version

__version__ = version

__all__.append(__version__)

del version
