""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from linked_stack import LinkedStack
from node import TreeNode
import sys


# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BSTInOrderIterator:
    """ In-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: TreeNode[K, I]) -> None:
        """ Iterator initialiser. """

        self.stack = LinkedStack()
        self.current = root

    def __iter__(self) -> BSTInOrderIterator:
        """ Standard __iter__() method for initialisers. Returns itself. """

        return self

    def __next__(self) -> K:
        """ The main body of the iterator.
            Returns keys of the BST one by one respecting the in-order.
        """

        while self.current:
            self.stack.push(self.current)
            self.current = self.current.left

        if self.stack.is_empty():
            raise StopIteration

        result = self.stack.pop()
        self.current = result.right

        return result.key


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree.
            :complexity: O(1)
        """

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __iter__(self) -> BSTInOrderIterator:
        """ Create an in-order iterator. """
        return BSTInOrderIterator(self.root)

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        if current is None:  # base case: empty
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:  # base case: found
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        # Returns current to the previous stack frame
        return current

    def __delitem__(self, key: K) -> None:
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.

            Complexity:
            BestCase = WorstCase: O(comp(==) * log N)) where N is the number of nodes in the tree
        """
        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        return current

    def get_successor(self, current: TreeNode) -> TreeNode:
        """
            Get successor of the current node.
            It should be a node in the subtree rooted at current having the smallest key among all the
            larger keys.
            If no such node exists, then none should be returned.

            Complexity:
            BestCase: O(1) when we have a highly unbalanced tree to the left with no right subtree.
            WorstCase: O(log N) * O(Comp(>)) where N is the number of Nodes. This complexity represents
            the depth traversed in a perfectly balanced BST.
        """

        # If Root node is None, we know there's no successor.
        if current.right is None:
            return None
        return self.get_successor_aux(current, current)

    def get_successor_aux(self, current: TreeNode, original_node: TreeNode) -> TreeNode:
        """
        This method returns the TreeNode which is the successor to our input (TreeNode). It'll firstly
        Search the right-subtree from the original_node and from then on, continously search the left-subtree
        Until we reach a Leaf Node which is returned as the successor.

        Arguments:
        current: Represents the current TreeNode we're at whilst traversing
        original_node: Represents the TreeNode which was the original node we were trying to traverse from
        to find the successor of

        Complexity:
        BestCase: O(1) when we have a highly unbalanced tree to the left with no right subtree.
        WorstCase: O(log N) * O(Comp(>)) where N is the number of Nodes. This complexity represents
        the depth traversed in a perfectly balanced BST.
        """
        # Base Case:
        # If current node doens't have a left child (Either just because or because it's a Leaf Node), that's the successor
        if current.left is None:
            return current
        # If left node > original_node, search left-subtree as we know it gets us closer to successor
        elif current.left.key > original_node.key:
            return self.get_successor_aux(current.left, original_node)
        # This is only called at the start to search the right subtree.
        else:
            return self.get_successor_aux(current.right, original_node)

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
            Get a node having the smallest key in the current sub-tree through
            continously traversing the left-subtree until we reach None. Then return node above None.
            It doesn't search entire subtree as it searches only down one path.

            Complexity:
            BestCase: O(1) where the tree is unbalanced entirely to the right side. Return Root Node.
            WorstCase: O(log N) where N represents the number of nodes and the tree is Perfectly Balanced,
            requiring the traversal of the Depth of the tree.
        """
        while current.left is not None:
            current = current.left
        return current

    def is_leaf(self, current: TreeNode) -> bool:
        """ Simple check whether or not the node is a leaf.
            Complexity:
            BestCase = WorstCase = O(1)
            """

        return current.left is None and current.right is None
