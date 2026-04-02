import time


class Generator:
    _N = 624
    _M = 397
    _MATRIX_A = 0x9908B0DF
    _UPPER_MASK = 0x80000000
    _LOWER_MASK = 0x7FFFFFFF

    def __init__(this, seed: int | None = None):
        if seed is None:
            seed = int(time.time() * 1_000_000) & 0xFFFFFFFF
        this._mt = this._init_state(seed)
        this._idx = this._N

    def random(this) -> float:
        if this._idx >= this._N:
            this._twist(this._mt)
            this._idx = 0
        y = this._temper(this._mt[this._idx])
        this._idx += 1
        return y / 4294967296.0

    def _init_state(this, seed: int) -> list:
        mt = [0] * this._N
        mt[0] = seed & 0xFFFFFFFF
        for i in range(1, this._N):
            mt[i] = (1812433253 * (mt[i - 1] ^ (mt[i - 1] >> 30)) + i) & 0xFFFFFFFF
        return mt

    def _twist(this, mt: list) -> None:
        for i in range(this._N):
            y = (mt[i] & this._UPPER_MASK) | (mt[(i + 1) % this._N] & this._LOWER_MASK)
            mt[i] = mt[(i + this._M) % this._N] ^ (y >> 1)
            if y & 1:
                mt[i] ^= this._MATRIX_A

    def _temper(this, y: int) -> int:
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y & 0xFFFFFFFF
