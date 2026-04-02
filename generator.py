import time


class Generator:
    _N = 624
    _M = 397
    _MATRIX_A = 0x9908B0DF
    _UPPER_MASK = 0x80000000
    _LOWER_MASK = 0x7FFFFFFF

    def __init__(self, seed: int | None = None):
        if seed is None:
            seed = int(time.time() * 1_000_000) & 0xFFFFFFFF
        self._mt = self._init_state(seed)
        self._idx = self._N

    def random(self) -> float:
        if self._idx >= self._N:
            self._twist(self._mt)
            self._idx = 0
        y = self._temper(self._mt[self._idx])
        self._idx += 1
        return y / 4294967296.0

    def _init_state(self, seed: int) -> list:
        mt = [0] * self._N
        mt[0] = seed & 0xFFFFFFFF
        for i in range(1, self._N):
            mt[i] = (1812433253 * (mt[i - 1] ^ (mt[i - 1] >> 30)) + i) & 0xFFFFFFFF
        return mt

    def _twist(self, mt: list) -> None:
        for i in range(self._N):
            y = (mt[i] & self._UPPER_MASK) | (mt[(i + 1) % self._N] & self._LOWER_MASK)
            mt[i] = mt[(i + self._M) % self._N] ^ (y >> 1)
            if y & 1:
                mt[i] ^= self._MATRIX_A

    def _temper(self, y: int) -> int:
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y & 0xFFFFFFFF
