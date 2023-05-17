import random
from TreeNode import TreeNode

# AVL tree class which supports the
# Insert operation
class AVL_Tree(object):
    """AVL Tree with insert implementation.  (Delete not implemented)"""

    def __init__(self, maxWidth=2):
        self.root     = None
        self.maxWidth = maxWidth


    def __str__(self):
        return str(self.root)
    

    def stringify(self):
        grid = TreeNode.add_node_to_grid(self.root)
        return TreeNode.simple_stringify_grid(grid)


    # Recursive function to insert key in
    # subtree rooted with node and returns
    # new root of subtree.
    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        # Step 1 - Perform normal BST
        if not root:
            return TreeNode(key)
        elif key < root.value:
            root.left = self._insert(root.left, key)
        else:
            root.right = self._insert(root.right, key)
 
        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self._getHeight(root.left),
                           self._getHeight(root.right))
 
        # Step 3 - Get the balance factor
        balance = self._getBalance(root)
 
        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and key < root.left.value:
            return self._rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and key > root.right.value:
            return self._leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and key > root.left.value:
            root.left = self._leftRotate(root.left)
            return self._rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and key < root.right.value:
            root.right = self._rightRotate(root.right)
            return self._leftRotate(root)
 
        return root


    def _leftRotate(self, alpha):
        beta         = alpha.right
        gamma        = beta.left
        # Perform rotation
        beta.left    = alpha
        alpha.right  = gamma
        # Update heights
        alpha.height = 1 + max(self._getHeight(alpha.left ),
                               self._getHeight(alpha.right))
        beta.height  = 1 + max(self._getHeight(beta .left ),
                               self._getHeight(beta .right))
        # Return the new root
        return beta


    def _rightRotate(self, alpha):
        beta         = alpha.left
        gamma        = beta.right
        # Perform rotation
        beta.right   = alpha
        alpha.left   = gamma
        # Update heights
        alpha.height = 1 + max(self._getHeight(alpha.left ),
                               self._getHeight(alpha.right))
        beta.height  = 1 + max(self._getHeight(beta .left ),
                               self._getHeight(beta .right))
        # Return the new root
        return beta


    def _getHeight(self, root):
        if not root:
            return 0
        return root.height


    def _getBalance(self, root):
        if not root:
            return 0
        return self._getHeight(root.left) - self._getHeight(root.right)


if __name__ == '__main__':
    # Driver program to test above function
    myTree = AVL_Tree()
    
    myTree.insert(10)
    myTree.insert(20)
    myTree.insert(30)
    myTree.insert(40)
    myTree.insert(50)
    myTree.insert(25)

    # Preorder Traversal
    print("constructed AVL tree is")
    print(f'\n{myTree}\n')

    numbers = [x for x in range(1, 33)]
    random.shuffle(numbers)
    otherTree = AVL_Tree()
    for num in numbers:
        otherTree.insert(num)
    print(f"{min(numbers)} to {max(numbers)} in random order added to tree\n{otherTree}")
    print(f'\n\n{otherTree.stringify()}')