class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node

    def append(self, value):
        new_node = Node(value)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        return True

    def find_middle_node(self):
        fast = self.head
        slow = self.head
        while fast.next is not None:
            temp = fast.next
            if temp.next is not None:
                fast = temp.next
            else:
                fast = temp
            slow = slow.next
        return slow

    def has_loop(self):
        fast = self.head
        slow = self.head
        while( fast is not None
               and fast.next is not None
            ):
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                return True
        return False

    def find_kth_from_end(self,k):
        fast = self.head
        slow = self.head
        for i in range(k):
            if fast is not None:
                fast = fast.next
            else:
                return None
        while fast is not None:
            slow = slow.next
            fast = fast.next
        return slow

    def delete_duplicates(self):
        temp = self.head
        if temp:
            values_list = list()
            while temp is not None:
                values_list.append(temp.value)
                temp = temp.next
            temp_val = [values_list.remove(item) for item in list(set(values_list))]
            print(values_list)
            if values_list:
                curr = self.head
                prev1 = self.head
                prev_met = list()
                while curr is not None:
                    if curr.value in values_list and curr.value in prev_met:
                        prev1.next = curr.next
                    prev_met.append(curr.value)

                    prev1 = curr
                    curr = curr.next

    def print_list(self):
        if self.head is None:
            print("empty list")
        else:
            temp = self.head
            values = []
            while temp is not None:
                values.append(str(temp.value))
                temp = temp.next
            print(" -> ".join(values))

    def reverse_between(self, start_index, end_index):
        start_chain_1_b = self.head
        fast = self.head
        for i in range(end_index):
            if i < start_index - 1:
                start_chain_1_b = start_chain_1_b.next
            fast = fast.next
        if fast.next is not None:
            rest_chain = fast.next
            fast.next = None
        else:
            rest_chain = None
        start_chain = start_chain_1_b.next
        for i in range(end_index-start_index):
            slow = start_chain
            fast = start_chain.next
            while fast.next is not None:
                fast = fast.next
                slow = slow.next
            start_chain_1_b.next = fast
            start_chain_1_b = fast
            slow.next = None
        start_chain_1_b.next = start_chain
        start_chain_1_b.next.next = rest_chain

    def swap(self):
        self.head.value,self.tail.value = self.tail.value, self.head.value







my_linked_list = LinkedList(1)
my_linked_list.append(2)
my_linked_list.append(3)
my_linked_list.append(4)

my_linked_list.print_list()

my_linked_list.swap()

my_linked_list.print_list()



