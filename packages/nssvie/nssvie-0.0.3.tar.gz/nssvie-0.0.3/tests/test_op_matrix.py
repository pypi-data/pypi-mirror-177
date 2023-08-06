from nssvie._orthogonal_functions import BlockPulseFunctions

from numpy import (
    array,
    array_equal
)


def test_op_matrix():
    bpf = BlockPulseFunctions(T=1.0, m=5)
    P = array([
        [0.1, 0.2, 0.2, 0.2, 0.2],
        [0.0, 0.1, 0.2, 0.2, 0.2],
        [0.0, 0.0, 0.1, 0.2, 0.2],
        [0.0, 0.0, 0.0, 0.1, 0.2],
        [0.0, 0.0, 0.0, 0.0, 0.1],
    ])
    assert array_equal(
        P, bpf._operational_matrix_of_integration()
    )
