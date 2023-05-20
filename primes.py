"""
Check for largest prime
"""

from __future__ import annotations

__author__ = 'Bangze Han'
__docformat__ = 'reStructuredText'


class LargestPrimeIterator():
    def __init__(self, upper_bound, factor):
        """
        Initialise iterator class
        :param upper_bound: value for max prime number
        :param factor: value to be multiplied by each iteration
        """
        self.upper_bound = upper_bound
        self.factor = factor
        self.cur_prime = 0

    def peek(self):
        return self.cur_prime

    def __iter__(self):
        return self

    def __next__(self):
        """
        Calculate next prime number using a simple trial division, iterating backwards.
        For example the iterator LargestPrimeIterator(6, 2) should yield 5, 7, 13, 23, 43
        :return: largest prime number that is below upper bound

        :complexity:
        n is the current upper bound
        k is the cost of integer division
        best case O(sqrt(n)*k)
        worst case O(n*sqrt(n)*k)
        """
        # Check if there is a current prime value, otherwise use upper bound given
        if self.cur_prime:
            self.upper_bound = self.cur_prime * self.factor
        prime = False
        # Iterate from upper bound to 2, check for first largest prime number.
        while not prime and self.upper_bound > 2:
            self.upper_bound -= 1
            # Modulo every number from 0 to square root of the upper bound, if no remainders anywhere then it is prime
            # any() returns True if atleast one element in an iterable is True. Thus, if all elements are False, it'll return True, and set prime.
            if not any(self.upper_bound % x == 0 for x in range(2, int(self.upper_bound ** 0.5) + 1)):
                prime = True
        self.cur_prime = self.upper_bound
        return self.cur_prime


if __name__ == "__main__":
    S = LargestPrimeIterator(6, 2)
    print(S.peek())
    print(S.__next__())
    print(S.__next__())
    print(S.__next__())
    print(S.__next__())
    print(S.__next__())
