Block pulse functions
~~~~~~~~~~~~~~~~~~~~~

Define an :math:`m`-set of block pulse functions as

.. math::

    \phi_i(t) = \begin{cases} 1 & , \ (i-1)h \leq t < ih \\ 0 &
    \text{otherwise} \end{cases} \qquad (i=1,\ldots,m)

for :math:`t \in [0,T)` and an interval width of :math:`h=\frac{T}{m}`.
The BPFs are *disjoint*, i.e.

.. math::

    \phi_i(t)\phi_j(t) = \delta_{ij} \phi_i(t)

for :math:`i,j = 1, \ldots, m` and :math:`\delta_{ij}` the Kronecker delta and
*orthogonal*, i.e.

.. math::

    \int\limits_0^T \phi_i(t) \phi_j(t) dt = h \delta_{ij}

for :math:`i,j=1,\ldots,m`.