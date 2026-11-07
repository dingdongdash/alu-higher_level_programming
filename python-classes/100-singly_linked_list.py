#!/usr/bin/python3
"""This module defines a Node class and a sorted singly linked list class."""


class Node:
    """This class defines a node of a singly linked list."""

    def __init__(self, data, next_node=None):
        """Initialize a new node through the data and next_node setters.

        Args:
            data: The integer value stored in the node.
            next_node: The next Node of the list, or None for the last one.
        """
        self.data = data
        self.next_node = next_node

    @property
    def data(self):
        """Retrieve the integer value stored in the node."""
        return self.__data

    @data.setter
    def data(self, value):
        """Set the value stored in the node after validating the given value.

        Args:
            value: The new integer value of the node.

        Raises:
            TypeError: If value is not an integer.
        """
        if not isinstance(value, int):
            raise TypeError("data must be an integer")
        self.__data = value

    @property
    def next_node(self):
        """Retrieve the node that follows this node in the list."""
        return self.__next_node

    @next_node.setter
    def next_node(self, value):
        """Set the node that follows this node after validating the value.

        Args:
            value: The next Node of the list, or None for the last node.

        Raises:
            TypeError: If value is neither None nor a Node object.
        """
        if value is not None and not isinstance(value, Node):
            raise TypeError("next_node must be a Node object")
        self.__next_node = value


class SinglyLinkedList:
    """This class defines a singly linked list kept in increasing order."""

    def __init__(self):
        """Initialize a new and empty singly linked list."""
        self.__head = None

    def __str__(self):
        """Return the data of every node of the list, one number per line."""
        values = []
        current = self.__head
        while current is not None:
            values.append(str(current.data))
            current = current.next_node
        return "\n".join(values)

    def sorted_insert(self, value):
        """Insert a new node holding value at its sorted position.

        The list stays in increasing order, so the new node is placed before
        the first node whose data is greater than or equal to value.

        Args:
            value: The integer to store in the new node.
        """
        new_node = Node(value)
        if self.__head is None or value <= self.__head.data:
            new_node.next_node = self.__head
            self.__head = new_node
            return
        current = self.__head
        while current.next_node is not None and current.next_node.data < value:
            current = current.next_node
        new_node.next_node = current.next_node
        current.next_node = new_node
