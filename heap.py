"""Max Heap implemented using an array"""
from __future__ import annotations
__author__ = "Brendon Taylor, modified by Jackson Goerner"
__docformat__ = 'reStructuredText'

from typing import Generic
from referential_array import ArrayR, T
from material import Material

class MaxHeap(Generic[T]):
    MIN_CAPACITY = 1

    def __init__(self, max_size: int) -> None:
        self.length = 0
        self.the_array = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)

    def __len__(self) -> int:
        return self.length

    def is_full(self) -> bool:
        return self.length + 1 == len(self.the_array)

    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position
        :pre: 1 <= k <= self.length
        """
        item = self.the_array[k]
        while k > 1 and item > self.the_array[k // 2]:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        self.the_array[k] = item

    def add(self, element: T) -> bool:
        """
        Swaps elements while rising
        """
        if self.is_full():
            raise IndexError

        self.length += 1
        self.the_array[self.length] = element
        self.rise(self.length)

    def largest_child(self, k: int) -> int:
        """
        Returns the index of k's child with greatest value.
        :pre: 1 <= k <= self.length // 2
        """
        
        if 2 * k == self.length or \
                self.the_array[2 * k] > self.the_array[2 * k + 1]:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """ Make the element at index k sink to the correct position.
            :pre: 1 <= k <= self.length
            :complexity: ???
        """
        item = self.the_array[k]

        while 2 * k <= self.length:
            max_child = self.largest_child(k)
            if self.the_array[max_child] <= item:
                break
            self.the_array[k] = self.the_array[max_child]
            k = max_child

        self.the_array[k] = item
        
    def get_max(self) -> T:
        """ Remove (and return) the maximum element from the heap. """
        if self.length == 0:
            raise IndexError

        max_elt = self.the_array[1]
        self.length -= 1
        if self.length > 0:
            self.the_array[1] = self.the_array[self.length+1]
            self.sink(1)
        return max_elt

    def bottom_up(self, lst_items: list):
        """
        Bottom up construction of a heap, used when there are known size of items used (in list form).

        :param lst_items: List of items used
        :return: none

        :complexity: O(n) where n is the number of elements in the heap
        """
        # Update max size and array
        # max_size == len(lst_items) == length as size required is known
        self.max_size = len(lst_items)
        self.the_array = ArrayR(max(self.MIN_CAPACITY, self.max_size) + 1)
        self.length = len(lst_items)
        # Copy array to self
        for i in range(self.max_size):
            self.the_array[i+1] = lst_items[i]
        # Iterate in reverse to heapify every parent
        for i in range(self.max_size//2, 0, -1):
            self.sink(i)

class MaxHeapMats(MaxHeap):
    """
    Modified version of MaxHeap which takes in Materials
    """
    def __init__(self, max_size: int):
        MaxHeap.__init__(self, max_size)
        self.max_size = max_size

    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position
        :pre: 1 <= k <= self.length
        :complexity: O(log n * O(comp==)) where n is the number of elems in the heap.
        """
        item = self.the_array[k]
        while k > 1 and item.mining_rate > self.the_array[k // 2].mining_rate:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        self.the_array[k] = item


    def sink(self, k: int) -> None:
        """
        Make the element at index k sink to the correct position.
        :pre: 1 <= k <= self.length
        :complexity: worst case O(log n * O(comp(==))), best case O(comp(==)), where n is the number of elems in heap.
        """
        item = self.the_array[k]

        while 2 * k <= self.length:
            max_child = self.largest_child(k)
            if self.the_array[max_child].mining_rate <= item.mining_rate:
                break
            self.the_array[k] = self.the_array[max_child]
            k = max_child

        self.the_array[k] = item

    def largest_child(self, k: int) -> int:
        """
        Returns the index of k's child with greatest value.
        :pre: 1 <= k <= self.length // 2
        :complexity: worst case = best case = O(comp(==))
        """

        if 2 * k == self.length or \
                self.the_array[2 * k].mining_rate > self.the_array[2 * k + 1].mining_rate:
            return 2 * k
        else:
            return 2 * k + 1

class MaxHeapTuple(MaxHeap):
    """
    Modified version of MaxHeap which takes in a Tuple -> (key, item)
    """
    def __init__(self, max_size: int):
        MaxHeap.__init__(self, max_size)
        self.max_size = max_size

    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position
        :pre: 1 <= k <= self.length
        :complexity: O(log n * O(comp==)) where n is the number of elems in the heap.
        """
        item = self.the_array[k]
        while k > 1 and item[0] > self.the_array[k // 2][0]:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        self.the_array[k] = item


    def sink(self, k: int) -> None:
        """
        Make the element at index k sink to the correct position.
        :pre: 1 <= k <= self.length
        :complexity: worst case O(log n * O(comp(==))), best case O(comp(==)), where n is the number of elems in heap.
        """
        item = self.the_array[k]

        while 2 * k <= self.length:
            max_child = self.largest_child(k)
            if self.the_array[max_child][0] <= item[0]:
                break
            self.the_array[k] = self.the_array[max_child]
            k = max_child

        self.the_array[k] = item

    def largest_child(self, k: int) -> int:
        """
        Returns the index of k's child with greatest value.
        :pre: 1 <= k <= self.length // 2
        :complexity: worst case = best case = O(comp(==))
        """

        if 2 * k == self.length or \
                self.the_array[2 * k][0] > self.the_array[2 * k + 1][0]:
            return 2 * k
        else:
            return 2 * k + 1



if __name__ == '__main__':
    items = [ int(x) for x in input('Enter a list of numbers: ').strip().split() ]
    heap = MaxHeap(len(items))

    for item in items:
        heap.add(item)
        
    while(len(heap) > 0):
        print(heap.get_max())