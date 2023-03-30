from primes import *
import cProfile


primes_to_make = 2500

print(np.fromiter(prime_maker_first(primes_to_make), dtype=np.int32))
print(np.fromiter(prime_maker_second(primes_to_make * 20), dtype=np.int32))
print(np.fromiter(prime_maker_np(primes_to_make * 12), dtype=np.int32))
print(np.fromiter(Prime_Maker_Class(primes_to_make * 7), dtype=np.int32))
print(prime_maker_sieve(int(primes_to_make*(log(primes_to_make) + log(log(primes_to_make)))) * 8000))
print(np.fromiter(prime_maker_sieve_iter(primes_to_make * 180), dtype=np.int32))


cProfile.run('(np.fromiter(prime_maker_first(primes_to_make), dtype=np.int32))', sort='tottime')
cProfile.run('np.fromiter(prime_maker_second(primes_to_make * 20), dtype=np.int32)', sort='tottime')
cProfile.run('np.fromiter(prime_maker_np(primes_to_make * 12), dtype=np.int32)', sort='tottime')
cProfile.run('np.fromiter(Prime_Maker_Class(primes_to_make * 7), dtype=np.int32)', sort='tottime')
cProfile.run('prime_maker_sieve(int(primes_to_make*(log(primes_to_make) + log(log(primes_to_make)))) * 8000)', sort='tottime')
cProfile.run('np.fromiter(prime_maker_sieve_iter(primes_to_make * 180), dtype=np.int32)', sort='tottime')
