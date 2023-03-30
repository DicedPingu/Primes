import numpy as np
from math import log
from typing import Generator


def prime_maker_first(n: int) -> Generator:
    """First attempt at a prime maker.

    Args:
        n (int): Number of primes to produce.

    Yields:
        int: Prime Number
    """
    yield 2
    prime_list: list = [2]
    i: int = 1

    while len(prime_list) < n:
        i += 2
        if 0 not in [i % p for p in prime_list]:
            prime_list.append(i)
            yield i


def prime_maker_second(n: int) -> Generator:
    """My second attempt at a prime maker, 20 times faster than first attempt.

    Args:
        n (int): Number of primes to produce.

    Yields:
        int: Prime Number
    """
    yield 2

    def _is_prime(i, primes):
        for p in primes:
            if p * p > i:
                return True
            if i % p == 0:
                return False
        return True

    i = 1
    prime_list: list[int] = []
    while len(prime_list) < n - 1:
        i += 2
        if _is_prime(i, prime_list):
            prime_list.append(i)
            yield i


def _get_next_prime(guess, primes_to_mod) -> int:
    while not np.all(primes_to_mod[guess % primes_to_mod != 0]):
        guess += 2
    return guess

def prime_maker_np(n: int) -> Generator:
    """I made a generator in numpy, pretty sure it was faster, but I fucked it up.
    7 times faster than first attempt.

    Args:
        n (int): Number of primes to produce.

    Yields:
        int: Prime Number
    """
    yield 2
    primey_list = np.zeros(shape=n, dtype=np.int32)
    primey_list[0] = 2

    last_prime = 1
    for i in range(1, n):
        last_prime = _get_next_prime(last_prime + 2, primey_list[1:i])
        primey_list[i] = last_prime
        yield last_prime


class Prime_Maker_Class:
    def _get_next_prime(self) -> int:
        self.guess += 2
        primes_to_mod: np.ndarray = self.prime_list[1:self.index][self.prime_list[1:self.index] ** 2 <= self.guess]

        while True:
            if np.all(self.guess % primes_to_mod != 0):
                self.prime_list[self.index] = self.guess
                self.index += 1
                return self.guess
            else:
                self.guess += 2

    def __init__(self, primes_to_gen: int):
        """Create an iterator of primes through a class.

        Args:
            primes_to_gen (int): Number of primes to generate.
        """
        if primes_to_gen < 1:
            raise ValueError('Enter a number of primes to generate.')
        self.guess = 0
        self.primes_to_gen = primes_to_gen
        self.prime_list = np.zeros(shape=primes_to_gen, dtype=np.int32)
        self.index = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.primes_to_gen and self.guess:
            return self._get_next_prime()
        elif not self.guess:
            self.guess += 1
            self.prime_list[0] = 2
            return 2
        raise StopIteration


def prime_maker_sieve(limit: int) -> np.ndarray:  # of Eratosthenes
    """The best prime generator yet, Sieve Eratosthenes' algorithm fucking rocks!
    8000 times faster than my base prime generator.

    Args:
        limit (int): What number to stop generating primes at.

    Returns:
        np.ndarray: Returns a numpy array containing primes up to the limit given.
    """
    prime_map = np.ones(limit, dtype=np.int32)
    prime_map[0:2] = 0
    prime_map[4::2] = 0
    for i in np.arange(3, int(limit ** 0.5) + 1, 2):
        if prime_map[i]:
            prime_map[i ** 2::i] = 0
    return np.nonzero(prime_map)[0]


def prime_maker_sieve_iter(num_primes: int) -> Generator:  # of Eratosthenes
    """Prime generator which also uses Sieve's algorithm, 180 times faster than first.

    Args:
        num_primes (int): Number of primes to produce.

    Yields:
        int: Prime Number
    """
    upper_limit = int(num_primes * (log(num_primes) + log(log(num_primes))))
    prime_map = np.ones(upper_limit)
    prime_map[0:2] = 0
    prime_map[4::2] = 0
    primes_found = 1
    yield 2

    v = 3
    while primes_found < num_primes:
        if prime_map[v]:
            prime_map[v ** 2::v] = 0
            primes_found += 1
            yield v
        v += 2
