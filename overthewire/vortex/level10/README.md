# Vortex Level 10 → Level 11

## Random?

Read in 20 integers and write the seed used to generate those numbers in unsigned little endian format. You have a time limit of 30 seconds to do this. You must login to vortex.labs.overthewire.org


# Notes

- I remember this level
- It is using a weak PRNG, not CSRNG, it's [LCG][Linear Congruential Generator (LCG)]
  - You can analyse the output and deduce the seed
    - I wrote a python script to do this, but I've lost it.
  - This [PRNG] wikipedia article is interesting about how 40 years on weak PRNG are still problems.
    - Better PRNG exist, such as Mersenne Twister, WELL, and xorshift

[LCG]: https://en.wikipedia.org/wiki/Linear_congruential_generator
[PRNG]: https://en.wikipedia.org/wiki/Pseudorandom_number_generator
