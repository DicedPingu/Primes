import numpy as np
from typing import Generator

# Define a function to generate prime numbers (first attempt)
def prime_maker_first(n: int) -> Generator:
    # Yield the first prime number, 2
    yield 2
    # Initialize a list of prime numbers with 2
    prime_list: list = [2]
    # Set the starting point for the next number to be checked
    i: int = 1

    # Continue generating primes until the desired number of primes has been generated
    while len(prime_list) < n:
        # Move to the next odd number to check
        i += 2
        # Check if the current number is divisible by any of the previously generated prime numbers
        if 0 not in [i % p for p in prime_list]:
            # If the current number is prime, add it to the list of prime numbers and yield it
            prime_list.append(i)
            yield i


# Define a function to generate prime numbers (second attempt)
def prime_maker_second(n: int) -> Generator:
    # Yield the first prime number, 2
    yield 2

    # Define a nested function to check if a number is prime
    def _is_prime(i, primes):
        for p in primes:
            # If the square of the prime number is greater than the current number, no need to check further
            if p * p > i:
                return True
            # Check if the current number is divisible by any of the previously generated prime numbers
            if i % p == 0:
                return False
        # If the number is not divisible by any previous prime number, then it is a prime number
        return True

    # Set the starting point for the next number to be checked
    i = 1
    # Initialize an empty list of prime numbers
    prime_list: list[int] = []
    # Continue generating primes until the desired number of primes has been generated
    while len(prime_list) < n - 1:
        # Move to the next odd number to check
        i += 2
        # Check if the current number is a prime number
        if _is_prime(i, prime_list):
            # If the current number is prime, add it to the list of prime numbers and yield it
            prime_list.append(i)
            yield i


# Define a "private" function to get the next prime number for use in the numpy prime generator
def _get_next_prime(guess, primes_to_mod) -> int:
    # While the guess is not a prime number, keep incrementing by 2 until it is a prime number
    while not np.all(primes_to_mod[guess % primes_to_mod != 0]):
        guess += 2
    # Return the next prime number
    return guess

# Define a function to generate prime numbers using numpy
def prime_maker_np(n: int) -> Generator:
    # Yield the first prime number, 2
    yield 2
    # Initialize a numpy array of zeros with size n and dtype int32
    primey_list = np.zeros(shape=n, dtype=np.int32)
    # Set the first element of the numpy array to 2
    primey_list[0] = 2

    # Set the starting point for the next prime number to be generated
    last_prime = 1
    # Generate the remaining n-1 prime numbers
    for i in range(1, n):
        # Get the next prime number using the private function _get_next_prime
        last_prime = _get_next_prime(last_prime + 2, primey_list[1:i])
        # Add the next prime number to the numpy array
        primey_list[i] = last_prime
        # Yield the next prime number
        yield last_prime


# Define a function to generate prime numbers using the Sieve of Eratosthenes algorithm
def prime_maker_sieve(limit: int) -> np.ndarray:
    # Initialize a numpy array of ones with size limit and dtype int32
    prime_map = np.ones(limit, dtype=np.int32)
    # Set the first two elements of the numpy array to 0 (0 and 1 are not prime numbers)
    prime_map[0:2] = 0
    # Set all even numbers (except 2) to 0 (they are not prime numbers)
    prime_map[4::2] = 0
    # Iterate over all odd numbers up to the square root of limit
    for i in np.arange(3, int(limit ** 0.5) + 1, 2):
        # If the current number is a prime number, mark all its multiples as not prime
        if prime_map[i]:
            prime_map[i ** 2::i] = 0
    # Return the numpy array of all prime numbers up to the limit
    return np.nonzero(prime_map)[0]


primes_to_make = 2500
# OG function, finds 2500 primes in a couple of seconds.
print(np.fromiter(prime_maker_first(primes_to_make), dtype=np.int32))
# Function 2, finds 20 times the amount of primes, using the same time.
print(np.fromiter(prime_maker_second(primes_to_make * 20), dtype=np.int32))
# Other function, only 12 times faster than OG
print(np.fromiter(prime_maker_np(primes_to_make * 12), dtype=np.int32))
# Total beast function, 8000 times faster, you have to calculate the number you want primes up to
# The number needed to reach a certain amount of primes is 'n * (log(n) + log(log(n)))'
print(prime_maker_sieve(int(primes_to_make*(log(primes_to_make) + log(log(primes_to_make)))) * 8000))
