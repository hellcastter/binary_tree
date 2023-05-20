"""
File: linkedbst.py
Author: Ken Lambert
"""

import random
from math import log
import time
import sys

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack

sys.setrecursionlimit(20000)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return lyst

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root

        while True:
            if node is None:
                return None

            if item == node.data:
                return node.data

            if item < node.data:
                node = node.left
            else:
                node = node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left is None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right is None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            node = self._root
            while True:
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break

                    node = node.left
                    continue
                # New item is greater or equal,
                # go right until spot is found
                if node.right is None:
                    node.right = BSTNode(item)
                    break

                node = node.right

        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if not top:
                return 0

            if not top.left and not top.right:
                return 0

            return max(height1(top.left), height1(top.right)) + 1

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(len(self) + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        top = self._root

        def search(top, low, high) -> list:
            if not top:
                return []

            if low <= top.data <= high:
                return search(top.left, low, high) + [top.data] + search(top.right, low, high)

            if top.data < low:
                return search(top.right, low, high)

            if top.data > high:
                return search(top.left, low, high)

            return []

        return search(top, low, high)

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = self.inorder()
        self._root = None

        def recursion(lst) -> BSTNode | None:
            length = len(lst)
            if length == 0:
                return None

            half = length // 2
            middle = lst[half]

            lst_left = lst[:half]
            lst_right = lst[half + 1:]

            return BSTNode(middle, recursion(lst_left), recursion(lst_right))


        self._root = recursion(nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        top = self._root

        def recursion(item, top, result = None):
            if not top:
                return result

            if top.data > item:
                result = top.data
                return recursion(item, top.left, result)

            if top.data == item:
                return recursion(item, top.right, result)


            if top.data < item:
                return recursion(item, top.right, result)

            return result

        return recursion(item, top)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        top = self._root

        def recursion(item, top, result = None):
            if not top:
                return result

            if top.data > item:
                return recursion(item, top.left, result)

            if top.data == item:
                return recursion(item, top.left, result)


            if top.data < item:
                result = top.data
                return recursion(item, top.right, result)

            return result

        return recursion(item, top)

    @classmethod
    def demo_bst(cls, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words_count = 10000
        with open(path, 'r', encoding='utf-8') as file:
            words = file.read().strip().split('\n')

        words = random.choices(words, k=words_count * 3)
        words.sort()

        random_words = random.choices(words, k=words_count)

        building_time = False

        print(f"Find {words_count} words in dict of {len(words)} words")
        print(f"Add building time: {building_time}")
        print("If you want add tree building time to result — change building_time to True")
        print()

        print(f"- in list: {cls.find_words_in_list(random_words, words)}s")
        print(
            "- in ordered BinaryTree: "
            f"{cls.consistent_tree(random_words, words, building_time)}s"
        )
        print(f"- in random BinaryTree: {cls.random_tree(random_words, words, building_time)}s")
        print(
            "- in balanced random BinaryTree: "
            f"{cls.balanced_tree(random_words, words, building_time)}s"
        )



    @staticmethod
    def find_words_in_list(random_words, words):
        """ Find words in list """
        start = time.time()

        for word in random_words:
            words.index(word)

        end = time.time()
        return end - start

    @staticmethod
    def consistent_tree(random_words, words, building_time=False):
        """ consistent_tree """
        start = time.time()
        consistent_tree = LinkedBST(words)

        if not building_time:
            start = time.time()

        for word in random_words:
            consistent_tree.find(word)

        end = time.time()
        return end - start


    @staticmethod
    def random_tree(random_words, words, building_time=False):
        """ random_tree """
        random.shuffle(words)
        start = time.time()

        consistent_tree = LinkedBST(words)

        if not building_time:
            start = time.time()

        for word in random_words:
            consistent_tree.find(word)

        end = time.time()
        return end - start

    @staticmethod
    def balanced_tree(random_words, words, building_time=False):
        """ balanced_tree """
        random.shuffle(words)
        start = time.time()
        consistent_tree = LinkedBST(words)
        consistent_tree.rebalance()

        if not building_time:
            start = time.time()

        for word in random_words:
            consistent_tree.find(word)

        end = time.time()
        return end - start

LinkedBST.demo_bst('words.txt')
