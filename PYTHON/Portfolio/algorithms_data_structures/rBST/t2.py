class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return True
        temp = self.root
        while (True):
            if new_node.value == temp.value:
                return False
            if new_node.value < temp.value:
                if temp.left is None:
                    temp.left = new_node
                    return True
                temp = temp.left
            else:
                if temp.right is None:
                    temp.right = new_node
                    return True
                temp = temp.right

    def dfs_in_order(self):
        results = []
        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            results.append(current_node.value)
            if current_node.right is not None:
                traverse(current_node.right)

        traverse(self.root)
        return results

    def is_valid_bst(self):
        tree = self.dfs_in_order()
        m_index = 0

        while m_index + 1 < len(tree):
            slow = tree[m_index]
            fast = tree[m_index + 1]
            if not slow < fast:
                return False
            m_index += 1
        return True

    def kth_smallest(self, k):
        stack = []
        node = self.root

        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()

            k -= 1
            if k == 0:
                return node.value
            print(f'before value assigment ')
            node = node.right

        return None


my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print("BST is valid:")
print(my_tree.kth_smallest(2))

"""
    EXPECTED OUTPUT:
    ----------------
    BST is valid:
    True

 """