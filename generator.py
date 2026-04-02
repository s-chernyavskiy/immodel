import time

_N = 624
_M = 397
_MATRIX_A = 0x9908B0DF
_UPPER_MASK = 0x80000000
_LOWER_MASK = 0x7FFFFFFF


def _init_state(seed: int) -> list:
    mt = [0] * _N
    mt[0] = seed & 0xFFFFFFFF
    for i in range(1, _N):
        mt[i] = (1812433253 * (mt[i - 1] ^ (mt[i - 1] >> 30)) + i) & 0xFFFFFFFF
    return mt


def _twist(mt: list) -> None:
    for i in range(_N):
        y = (mt[i] & _UPPER_MASK) | (mt[(i + 1) % _N] & _LOWER_MASK)
        mt[i] = mt[(i + _M) % _N] ^ (y >> 1)
        if y & 1:
            mt[i] ^= _MATRIX_A


def _temper(y: int) -> int:
    y ^= y >> 11
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    y ^= y >> 18
    return y & 0xFFFFFFFF


class Generator:
    """MT19937: uniform floats in [0, 1)."""

    def __init__(this, seed: int | None = None):
        if seed is None:
            seed = int(time.time() * 1_000_000) & 0xFFFFFFFF
        this._mt = _init_state(seed)
        this._idx = _N

    def random(this) -> float:
        if this._idx >= _N:
            _twist(this._mt)
            this._idx = 0
        y = _temper(this._mt[this._idx])
        this._idx += 1
        return y / 4294967296.0
