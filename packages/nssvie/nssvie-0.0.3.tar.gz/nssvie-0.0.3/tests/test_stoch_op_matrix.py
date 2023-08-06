from nssvie._orthogonal_functions import BlockPulseFunctions

from numpy import (
    array,
    round,
    array_equal
)

from stochastic.random import seed


def test_stoch_op_matrix():
    seed(1337)
    bpf = BlockPulseFunctions(T=1.0, m=5)
    P_S = array([
        [
            0.01210147462, 0.16197333499, 0.16197333499, 0.16197333499,
            0.16197333499
        ],
        [
            0.0, -0.04355908408, -0.48290521059, -0.48290521059,
            -0.48290521059
        ],
        [
            0.0, 0.0, 0.79693150201, 0.47868274005, 0.47868274005
        ],
        [
            0.0, 0.0, 0.0, 0.58717680419, -0.20414451125
        ],
        [
            0.0, 0.0, 0.0, 0.0, 0.04690799472
        ],
    ])
    assert array_equal(
        P_S,
        round(bpf._stochastic_operational_matrix_of_integration(), 11)
    )
