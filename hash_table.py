""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
"""
from __future__ import annotations
import primes as p

__author__ = 'Brendon Taylor. Modified by Graeme Gange, Alexey Ignatiev, and Jackson Goerner'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'

from referential_array import ArrayR
from typing import TypeVar, Generic

T = TypeVar('T')

'''
    TODO:
    Implement statistics by reading the spec sheet on differences between collision/conflicts. 
    I think I need to change linear probing because only time we care/collisions occur include when we're inserting. 
    What I've implemented so far is wrong in linear_probe.
'''


class LinearProbeTable(Generic[T]):
    """
        Linear Probe Table.

        attributes:
            count: number of elements in the hash table
            table: used to represent our internal array
            tablesize: current size of the hash table
            primes: prime generator for tablesize
    """

    def __init__(self, expected_size: int, tablesize_override: int = -1) -> None:
        """
            Initialiser.
            Creates a hash table of some size unless overridden with tablesize_override
            :expected_size: expected size of the hash table
            :tablesize_override: optional argument to override table size
            Complexity:
            Best case: O(1)
            Worst case: O(p) where p is the time taken to generate a prime number
        """
        self.count = 0
        self.tablesize = tablesize_override
        # Initialise iterator, if tablesize_override, skip 1st prime
        self.primes = p.LargestPrimeIterator(tablesize_override, 2)
        self.primes.__next__()
        if self.tablesize == -1:
            # Need to choose a number big enough to avoid collisions while being space efficient
            # This should be a prime number, and be big enough to avoid most collisions.
            # 2 multiplier, should be sufficient.
            self.primes = p.LargestPrimeIterator(expected_size * 2, 2)
            self.tablesize = self.primes.__next__()
        self.table = ArrayR(self.tablesize)
        # Initialising statistics counters
        self.conflict_count = 0
        self.probe_total = 0
        self.probe_max = 0
        self.rehash_count = 0

    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable.
            Uses MAD to uniformly distribute keys
            h(x) = [(a*x + b) % p] % N
            a,b: some integer [1, p-1] , p: prime number where p > N , N: hash table size.
        """
        # Initialise variables
        a = 1
        b = 1
        # Initialise iterator to get a larger prime number than tablesize.
        iterator = p.LargestPrimeIterator(int(self.tablesize * 1.6), 2)
        hash_base = iterator.__next__()

        for char in key:
            # Chain operations such that next value is dependent on the last character.
            # In this case we update b based on the previous result of h(x).
            b = (ord(char) + a * b) % self.tablesize
            a = a * hash_base % (self.tablesize - 1)
        return b

    def statistics(self) -> tuple:
        """
            Returns a tuple of 4 values:
            1. Total number of conflicts (conflict_count)
            2. Total distance probed throughout execution (probe_total)
            3. Length of longest probe chain (probe_max)
            4. Total number of times rehashing is done (rehash_count)
        """
        return (self.conflict_count, self.probe_total, self.probe_max, self.rehash_count)

    def __len__(self) -> int:
        """
            Returns number of elements in the hash table
            :complexity: O(1)
        """
        return self.count

    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
            Find the correct position for this key in the hash table using linear probing
            :complexity best: O(K) first position is empty
                            where K is the size of the key
            :complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
            :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash
        probe_chain = 0
        is_conflicted = False

        if is_insert and self.is_full():
            raise KeyError(key)

        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    if is_conflicted:
                        # Probed at least once, so increment conflict count
                        self.conflict_count += 1
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                if is_conflicted:
                    # Probed at least once, so increment conflict count
                    self.conflict_count += 1
                return position
            else:  # there is something but not the key, try next
                # Probe
                position = (position + 1) % len(self.table)
                # Update statistics, conflict here
                is_conflicted = True
                self.probe_total += 1
                probe_chain += 1
                # Update max probe chain
                if probe_chain > self.probe_max:
                    self.probe_max = probe_chain

        raise KeyError(key)

    def keys(self) -> list[str]:
        """
            Returns all keys in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][0])
        return res

    def values(self) -> list[T]:
        """
            Returns all values in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][1])
        return res

    def __contains__(self, key: str) -> bool:
        """
            Checks to see if the given key is in the Hash Table
            :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
            Get the item at a certain key
            :see: #self._linear_probe(key: str, is_insert: bool)
            :raises KeyError: when the item doesn't exist
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
            Set an (key, data) pair in our hash table
            :see: #self._linear_probe(key: str, is_insert: bool)
            :see: #self.__contains__(key: str)
        """
        # Check if need to rehash before insertion
        load_factor = self.count / self.tablesize
        if load_factor > 0.5:
            self._rehash()
        position = self._linear_probe(key, True)

        # Only increment count when adding to None. If modifying a current (key,value), don't increment count.
        if self.table[position] is None:
            self.count += 1

        self.table[position] = (key, data)

    def is_empty(self):
        """
            Returns whether the hash table is empty
            :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
            Returns whether the hash table is full
            :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
            Utility method to call our setitem method
            :see: #__setitem__(self, key: str, data: T)
        """

        # Note: Insert could be used to set or modify an element
        # If table is greater than half full, rehash, then insert.
        self[key] = data

    def _rehash(self) -> None:
        """
            Need to resize table and reinsert all values.
            Should modify the array -> self.count should remain unchanged.
        """
        # Find next prime number that is double
        self.tablesize = self.primes.__next__()
        # Temporarily store previous table and create new_table of roughly double size.
        prev_table = self.table
        # Reset count
        self.count = 0
        self.table = ArrayR(self.tablesize)
        # Updated self.table to be empty.
        # Have get_item available: NOTE: ArrayR initialized with None objects.
        for i in range(len(prev_table)):
            if prev_table[i] is not None:
                # Rehash and reinsert from old table
                self.insert(prev_table[i][0], prev_table[i][1])
        self.rehash_count += 1

    def __str__(self) -> str:
        """
            Returns all they key/value pairs in our hash table (no particular
            order).
            :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result


if __name__ == "__main__":
    s = LinearProbeTable(3, 10)
    print("Initial Size" + f' {s.tablesize}')
    print(s.hash(' 322'))
    s[' 2'] = 'Warzone'
    s['a'] = 'NBA goat is Ben Abraham'
    print(s['a'])
    print(s.count / s.tablesize)
    print("\n")
    print("First Rehash" + f" {s.tablesize}")
    print(s.hash(' 2'))
    print(s.hash(' 7'))
    print(s.count / s.tablesize)
    s[' 5'] = 'donkey fist'
    print(s.count / s.tablesize)
    print(s.statistics())
    # print(s.hash("123"))
    print(s.tablesize)
    print(s[' 5'])
    s['3'] = 'asd'
    s['4'] = 'abc'
    s['5'] = 'sdf'
    s['6'] = 'sadf'
    s['17'] = 'ad'
    s['423'] = 'sd'
    s['124'] = 'sd'
    s['34'] = 'df'
    s['345'] = 'ddff'
    print(s.statistics())
    # print("\n")
    # print(s.hash(" 2"))
    # print(s.hash("a"))
    # print(s.hash("     9"))
    # print(s.probe_total)

    # print(s.hash(' 2'))
    # print(s.hash('b'))

    # print(s.hash('     7'))
    # print(s.hash('100'))
    # print(s.hash("a") == s.hash(" 1"))
    # print(s.conflict_count)
    # print(s.probe_max)
    # print(s.probe_total)
    # print(s.hash("wdkoe"))
    # print(s.hash("wdoke"))
    # print(s.hash("123"))
    # print(s.hash("joemama"))
    # s['daniel'] = 'daniel'
    # print(s.tablesize)
    # print(s.count)
    # print(s)
    # s._rehash()
    # print(s.tablesize)
    # print(s.count)
    # print(s)

