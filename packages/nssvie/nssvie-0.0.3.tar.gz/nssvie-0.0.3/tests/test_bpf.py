from nssvie._orthogonal_functions import BlockPulseFunctions
from numpy import (
    array,
    array_equal
)


def test_bpf_vector():
    bpf = BlockPulseFunctions(T=1.0, m=5)
    bpf_vector = array([0.0, 0.0, 1.0, 0.0, 0.0])
    assert array_equal(bpf._bpf_vector(t=0.5), bpf_vector)
