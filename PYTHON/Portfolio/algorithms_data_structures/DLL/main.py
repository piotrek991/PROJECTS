import time
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.length = 1

    def print_list(self):
        output = []
        current_node = self.head
        while current_node is not None:
            output.append(str(current_node.value))
            current_node = current_node.next
        print(" <-> ".join(output))

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = new_node
            new_node.prev = temp
        self.length += 1
        return True

    def swap_pairs(self):
        fast = self.head.next
        slow = self.head

        if fast:
            self.head = fast
        temp_s = slow

        while slow:
            if slow.next:
                slow = slow.next.next

                fast.next = temp_s
                fast.prev = temp_s.prev
                temp_s.prev = fast
                temp_s.next = slow

                if fast.prev:
                    fast.prev.next = fast
                if slow:
                    slow.prev = temp_s
                    fast = slow.next
                temp_s = slow
            else:
                slow = slow.next

my_dll = DoublyLinkedList(1)
my_dll.append(2)



print('my_dll before swap_pairs:')
my_dll.print_list()

my_dll.swap_pairs()

print('my_dll after swap_pairs:')
my_dll.print_list()

"""
    EXPECTED OUTPUT:
    ----------------
    my_dll before swap_pairs:
    1 <-> 2 <-> 3 <-> 4
    ------------------------
    my_dll after swap_pairs:
    2 <-> 1 <-> 4 <-> 3

"""