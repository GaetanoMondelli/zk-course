1.a) Is it true that all odd squares are ≡ 1 (mod 8) ?

We can start with some examples to see if the statement is true:

3² = 9 ≡ 1 (mod 8)
5² = 25 ≡ 1 (mod 8)
7² = 49 ≡ 1 (mod 8)

We can see that the statement is true for the examples above. We can also prove this statement using the properties of modular arithmetic.

An odd number can be represneted as 2n + 1, where n is an integer. The square of an odd number can be represented 

(2n + 1)² = 1?
4² + 4n + 1 , we can see the congruence of each term and sum them up (because of the properties of modular arithmetic)
So 4n² ≡ 0 (mod 8) and 4n ≡ 0 (mod 8) and 1 ≡ 1 (mod 8)
So the sum of the terms is 1 ≡ 1 (mod 8)

Therefore, it is true that all odd squares are ≡ 1 (mod 8).

1.b) what about even squares (mod 8) ?

We can start with some examples to see if the statement is true:
n² = 4n² ≡ 0 (mod 8)

n=1, 2² = 4 ≡ 4 (mod 8)
n=2, 4² = 16 ≡ 0 (mod 8)
n=3, 6² = 36 ≡ 4 (mod 8)
n=4, 8² = 64 ≡ 0 (mod 8)

Looks like there are two possible results based on N. Wonmdering if we can use induction to prove this


For positive n the result is 0
Base Case
for n=0 the result is 0

Inductive step k where n = 2k
(2k)² = 4k² ≡ 0 (mod 8)

Now step k+1 where n = 2k+1
(2k+1)² = 4k² + 4k + 1 ≡ 1 (mod 8)

We proved this before, so we can say that the statement is true for all even squares

Now For negative n the result is 4

Base Case
for n=1 the result is 4

Inductive step k where n = 2k+1
(2k+1)² = 4k² + 4k + 1 ≡ 1 (mod 8)

Now step k+1 where n = 2k+1+1
(2k+2)² = 4k² + 8k + 4 ≡ 4 (mod 8)

Now this would probably require induction to prove, but I think we can say that the statement is true for all even squares


What do you understand by
a) O(n) linear time complexity
b) O(1) constant time complexity
c) O(log n) logarithmic time complexity

in order of complexity, O(1) < O(log n) < O(n)

In the context of proofs we are probably talking about space complexity (I have usually seen indicated with O(s) and time with o(n))

For a proof size it would be best to have it constant so we would not tell or give any indication of the size of the proof. This is, i suppose, not always possible, but it is the best case scenario.



















