from __future__ import annotations

""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev, with edits by Jackson Goerner'
__docformat__ = 'reStructuredText'

from bst import BSTInOrderIterator, BinarySearchTree
from typing import TypeVar, Generic, List
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_nodes_in_left_subtree(self, current: AVLTreeNode) -> int:
        """
            Returns the number of nodes in the left subtree of a node.
            : complexity: O(1)
        """
        return current.nodes_left_subtree

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """
        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def get_number_of_nodes(self) -> int:
        """
            Returns number of nodes in a tree through calling auxiliary method

            Complexity:
            BestCase = WorstCase = O(N) where N is the number of nodes in the tree
        """
        return self.get_number_of_nodes_aux(self.root)

    def get_number_of_nodes_aux(self, current: AVLTreeNode) -> int:
        """
            Returns number of nodes in a tree through pre-order traversal

            Complexity:
            BestCase = WorstCase = O(N) where N is the number of nodes in the tree
        """
        if current is None:
            return 0
        else:
            return 1 + self.get_number_of_nodes_aux(current.left) + self.get_number_of_nodes_aux(current.right)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            This method traverses through the tree until it finds the appropriate position (as a leaf node)
            to insert the key. It then pops stack frames, going back up the tree and assigning the parent to link
            to the returned child from the previous stack frame. In doing so, it updates the height and number of nodes
            in left-subtree of the node which was traversed whilst getting to the AVLTreeNode's appropriate position.

            Arguments:
            current: Represents the node with which we consider our root to insert the node into
            Key, Item: Represents the Key and Item to be Inserted into the Tree as an AVLTreeNode object

            Complexity:
            BestCase: O(Comp(==)) is the  when an AVLTreeNode is inserted at the root of the tree
            WorstCase: O(Comp(==) * log N) where N is the number of nodes in the tree as the tree is balanced
        """
        if current is None:  # Base Case: Reached Leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        # Continuously recurse down tree until we reach BaseCase either to the left or right
        # Subtree depending on the value of the key
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:
            # If key == current.key, we insert a duplicate which is invalid in AVL trees
            raise ValueError('Inserting duplicate item')

        # Whilst popping stack frames: Only updating values of nodes we recursed through
        if current.left is not None or current.right is not None:
            # Changing heights of nodes which had their subtree heights changed
            # Because they were recursed through to get to the position of Node to be inserted
            current.height = 1 + \
                max(self.get_height(current.left),
                    self.get_height(current.right))

            # Updating number of nodes only if the newly inserted
            # Node exists within the recursed through node's Left-Subtree.
            temp_tree = AVLTree()
            temp_tree.root = current.left
            if key in temp_tree:
                current.nodes_left_subtree += 1

        # Rebalance on every node we recurse back up through
        return self.rebalance(current)

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.

            Arguments:
            current: AVLTreeNode which we consider our root from which we delete from
            key: Represents the key which we're searching for to delete the subsequent node

            Complexity:
            BestCase: O(comp(==) * log N)) where N is the number of nodes in the tree when
            we're deleting an item at the root of the node as it avoids calling method get_number_of_nodes
            WorstCase: O(comp(==) * N)) where N is the number of nodes in the tree when we're deleting an item
            other than at the leaf and we need to call method get_number_of_nodes
        """
        if current is None:  # Can't find key to delete
            raise ValueError('Deleting non-existent item')

        # Recurse through tree to find the node with the key to delete
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)

        # If we've found our key, delete the key and link any pre-existing children
        # To the deleted nodes parent
        else:
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # Find successor, change node values and actually set deleted nodes key
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        # Whilst popping stack frames: Only updating values of nodes we recursed through
        if current.left is not None or current.right is not None:
            # Changing heights of nodes which had their subtree heights changed
            # Because they were recursed through to get to the position of Node to be inserted
            current.height = 1 + \
                max(self.get_height(current.left),
                    self.get_height(current.right))

            # Updating number of nodes in left_subtree of each node
            # That we recursed through to get to the position of the node to be deleted
            temp_tree = AVLTree()
            temp_tree.root = current.left
            current.nodes_left_subtree = temp_tree.get_number_of_nodes()

        # Rebalance on every node we recurse back up through
        return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.

            NOTE: Current always really refers to the root node.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            Complexity:
            BestCase = WorstCase = O(1)
        """

        no_left_node_initially = False

        if current.left is None:
            no_left_node_initially = True

        original_root = current
        original_right_left = current.right.left

        # Update new root node
        current = original_root.right

        # Remove current subtrees left link
        current.left = None

        # Update current subtrees left link
        original_root.right = None
        current.left = original_root

        # Add back in the deleted left node
        current.left.right = original_right_left

        # Update heights for current and current.left:
        if no_left_node_initially:
            # Update current.height and current.left.height through getting the height of their two subtrees
            # Which remain the same through rotation and finding the max of the two + 1

            # Try to access current.right.left, if current.right is a None object,
            # It'll raise AttributeError so set height of current.left to 0.
            try:
                height_new_left_node = 1 + self.get_height(current.right.left)
            except AttributeError:
                height_new_left_node = 0
            current.left.height = height_new_left_node

            # Update height of new root node as it uses previous result:
            height_new_root_node = 1 + \
                max(self.get_height(current.left),
                    self.get_height(current.right))
            current.height = height_new_root_node
        else:
            # Same as above but now there is a left node to the root initially
            height_new_left_node = 1 + \
                max(self.get_height(current.left.left),
                    self.get_height(current.left.right))
            current.left.height = height_new_left_node

            # Then update height of new root node as it uses previous result:
            height_new_root_node = 1 + \
                max(self.get_height(current.left),
                    self.get_height(current.right))
            current.height = height_new_root_node

        """
        
        
        WILL NEED TO CHANGE TO SIMILAR TO WHAT IS ABOVE!!! CAN'T UPDATE NODES IN LEFT SUBTREE USING GET_NUMBER_OF_NODES()
        
        
        """
        # Updates number of nodes in left subtree of new root:
        temp_tree = AVLTree()
        temp_tree.root = current.left
        current.nodes_left_subtree = temp_tree.get_number_of_nodes()

        temp_tree.root = current.left
        current.left.nodes_subtree = temp_tree.get_number_of_nodes() - 1

        return current

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity:
        """

        no_right_node_initially = False

        if current.right is None:
            no_right_node_initially = True

        original_root = current
        original_left_right = current.left.right

        # Update new root node
        current = original_root.left

        # Remove current subtrees right link
        current.right = None

        # Update current subtrees right link
        original_root.left = None
        current.right = original_root

        # Add back in the delete right node in step 2
        current.right.left = original_left_right

        # Update heights for current and current.right:
        if no_right_node_initially:
            # Update current.height and current.right.height through getting the height of their two subtrees
            # Which remain the same through rotation and finding the max of the two + 1

            # Try to access current.right.left, if current.right is a None object,
            # It'll raise AttributeError so set height of current.right to 0.
            try:
                height_new_right_node = 1 + self.get_height(current.right.left)
            except AttributeError:
                height_new_right_node = 0
            current.right.height = height_new_right_node

            # Update height of new root node as it uses previous result:
            height_new_root_node = 1 + \
                max(self.get_height(current.left),
                    self.get_height(current.right))
            current.height = height_new_root_node
        else:
            # Same as above but now there is a left node to the root initially
            height_new_right_node = 1 + \
                max(self.get_height(current.right.right),
                    self.get_height(current.right.left))
            current.right.height = height_new_right_node

            # Then update height of new node as it uses previous result:
            height_new_root_node = 1 + \
                max(self.get_height(current.left),
                    self.get_height(current.right))
            current.height = height_new_root_node

        """
        
        Once again, will need to update
        
        """
        # Updates left_subtree nodes
        temp_tree = AVLTree()
        temp_tree.root = current.right.left
        current.right.nodes_left_subtree = temp_tree.get_number_of_nodes()

        return current

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def find_ith_smallest(self, i: int) -> int:
        """
            Returns the value (int) of the ith smallest element to be used in range_between.

            Argument:
            i: Represents the index of the item we want to find in the tree

            Complexity:
            BestCase: O(comp(==)) where the ith smallest element is at the root as it requires no traversal
            WorstCase: O(logN * comp(==)) where the ith smallest element is at the leaf as we traverse through the Depth
            of the tree which is logN
        """
        current = self.root
        counter = i+1

        # Continue traversing to find current. If reach None object, invalid index
        while current is not None:
            # Found the key to be returned
            if current.nodes_left_subtree + 1 == counter:
                return current.key
            # Traverse Left Subtree and keep same counter as key in left-subtree
            elif current.nodes_left_subtree + 1 > counter:
                current = current.left
            # Traverse Right Subtree and decrement counter by number of nodes in left-subtree
            # We're ignoring by going to the Right Subtree
            else:
                counter -= current.nodes_left_subtree + 1
                current = current.right
        raise ValueError("Invalid Index Entered")

    def range_between(self, i: int, j: int) -> list:
        """
        Returns a sorted list of all elements in the tree between the ith and jth indices, inclusive
        through traversing until the ith key (which we found through find_ith_smallest method). 
        Then on each node in the traversal, we perform inorder traversal on its right-subtree
        with the function in the middle of the left and right search being appending to the final list
        of elements between indicies i and j. This inorder traversal on the right subtree occurs from
        the ith element, all the way back up to the root in the stack frames we used to traverse to
        the ith element initially.

        Arguments:
        i, j: Indicies we want to find the list of elements in the tree between

        Complexity:
        BestCase = WorstCase: O(j-i + logN) where N is the number of nodes in the Tree. This
        is the case because finding_ith_smallest is O(logN), then we traverse to ith smallest element O(logN)
        and from there, perform inorder traversal on only the node objects within range j-i and stop once we
        reach index i > j. Therefore, it'll perform j-1 inorder traversals.
        """
        key = self.find_ith_smallest(i)
        return self.range_between_aux(key, i, j, self.root, [], True, [])[1]

    def range_between_aux(self, key: int, i: int, j: int, current: AVLTreeNode, lst_of_keys: list, first_step: bool, lst_of_indicies: list) -> list:
        """
        Algorithm is illustrated above in range_between

        Arguments:
        key: The key of the ith smallest item
        i, j: The indicies to find the range of elements between
        current: The initial node we start traversing through the tree from (should be root)
        lst_of_keys: List of keys between indicies i to j (Inclusive)
        first_step: Boolean to indicate whether our recursive function call was made during the initial
        tree traversal which took O(log N) time to get to the ith smallest element.
        lst_of_indicies: List of indicies between i and j used to indicate when to stop recursion. 
        Example: If going from i = 2 to j = 4, the final lst_of_indicies = [2,3,4]

        Complexity:
        BestCase = WorstCase: O(j-i + logN) where N is the number of nodes in the Tree. This
        is the case because finding_ith_smallest is O(logN), then we traverse to ith smallest element O(logN)
        and from there, perform inorder traversal on only the node objects within range j-i and stop once we
        reach index i > j. Therefore, it'll perform j-1 inorder traversals.
        """

        # Traverse until you reach the ith smallest element:
        # The following is used just to get to the ith smallest key
        if first_step:
            # If key < current.key, search left-subtree
            if key < current.key:
                tmp_tuple = self.range_between_aux(
                    key, i, j, current.left, lst_of_keys, True, lst_of_indicies)
                # Update value of lst_of_keys
                lst_of_keys = tmp_tuple[1]
            # If key > current.key, seach right-subtree
            elif key > current.key:
                tmp_tuple = self.range_between_aux(
                    key, i, j, current.right, lst_of_keys, True, lst_of_indicies)
                # Update value of lst_of_keys
                lst_of_keys = tmp_tuple[1]

        # Now we've found ith smallest key: Perform traversal on the entire
        # Right-subtree of a node which we traversed through during the initial
        # Tree traversal to find ith smallest element

        # len(lst_of_indicies) would only ever in the worst case be j-i as it's only at most, of size j-1.

        # BaseCase: When we have every index from i to j (inclusive) in lst_of_indicies, stop recursion
        if len(lst_of_indicies) > (j-i):
            return (lst_of_indicies, lst_of_keys)

        # Try-Except used so that if we ever have a left-subtree be a None node, we can skip
        # The recursive call on the left-subtree through pass
        try:
            temp_tree = AVLTree()
            temp_tree.root = current.left
            # If ith smallest elements key is not in left-subtree, traverse through it
            # Part of inorder traversal (initial left-subtree search)
            if key not in temp_tree:
                self.range_between_aux(
                    key, i, j, current.left, lst_of_keys, False, lst_of_indicies)
        except AttributeError:
            pass

        # Performs middle of inorder traversal (appending valid item to list)
        if current.key >= key and not len(lst_of_indicies) > (j-i):
            lst_of_keys.append(current.item)
            # The following adds the correct index to lst_of_indicies through adding an integer
            # 1 greater than the current last element in the lst_of_indicies
            if len(lst_of_indicies) == 0:
                lst_of_indicies.append(i)
            else:
                lst_of_indicies.append(
                    lst_of_indicies[len(lst_of_indicies) - 1] + 1)

        # Try-Except used so that if we ever have a right-subtree be a None node, we can skip
        # The recursive call on the right-subtree through pass
        try:
            temp_tree = AVLTree()
            temp_tree.root = current.right
            # If ith smallest elements key is not in right-subtree, traverse through it
            # Part of inorder traversal (final right-subtree search)
            if key not in temp_tree:
                self.range_between_aux(
                    key, i, j, current.right, lst_of_keys, False, lst_of_indicies)
        except AttributeError:
            pass

        # Returns lists back to previous stack-frames to be assigned
        return (lst_of_indicies, lst_of_keys)
