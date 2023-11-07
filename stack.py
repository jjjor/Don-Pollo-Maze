import numpy as np

class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.next = None

class Stack:
    def __init__(self) -> None:
        self.head = Node("head")
        self.size = 0
        
    def is_empty(self):
        return self.size == 0
    
    def peek(self):
        if self.is_empty():
            raise Exception("Peeking from an empty stack")
        
        return self.head.next.data
        
    def push(self, data):
        node = Node(data)
        node.next = self.head.next
        self.head.next = node
        self.size += 1
        
        
    # Remove a value from the stack and return.
    def pop(self):
        if self.is_empty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.data
        
    def __str__(self):
        current = self.head.next
        out = ""
        while current:
            out += str(current.data) + "->"
            current = current.next
        return out[:-2]
    
    def reverse(self):
        stack = Stack()
        while not self.is_empty():
            stack.push(self.pop())
        return stack