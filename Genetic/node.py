class Node() : 
    next_id = 0 
    def __init__(self , is_terminal , value , left=None, right=None,parent = None,depth=0):
        self.isTerminal = is_terminal
        self.value = value 
        self.left = left 
        self.right = right
        self.parent = parent 
        self.id = Node.next_id  # Assign a unique id to each instance
        Node.next_id += 1
        self.depth = depth

    def __eq__(self, other):
        if isinstance(other, Node):
            return id(self) == id(other)
        return False


# # Define a global string
# global_string = ""


# def inorder_traversal(node):
#     global global_string
#     if node is not None:
#         # Traverse the left subtree
#         global_string += "("
#         inorder_traversal(node.left)

#         # Print the value of the current node
#         global_string += str(node.value)

#         # Traverse the right subtree
#         inorder_traversal(node.right)
#         global_string += ")"


# # Example usage:
# # Create a sample tree
# root = Node(False, "/")
# root.left = Node(False, "x")
# root.right = Node(False, "sin")
# root.left.left = Node(True, 1)
# root.left.right = Node(True, 2)
# root.right.left = Node(True, 3)
# # root.right.right = Node(True, 4)

# # Perform inorder traversal
# inorder_traversal(root)

# # Access the global string
# print(global_string)