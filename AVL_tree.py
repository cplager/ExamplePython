import random
from TreeNode import TreeNode

# AVL tree class which supports the
# Insert operation
class AVL_Tree(object):
    """AVL Tree with insert and delete implementation.
    https://en.wikipedia.org/wiki/AVL_tree"""

    def __init__(self, maxWidth=2):
        self.root     = None
        self.maxWidth = maxWidth


    def __str__(self):
        return str(self.root)
    

    def raw_stringify(self):
        grid = TreeNode.add_node_to_grid(self.root)
        return TreeNode.simple_stringify_grid(grid)


    def insert(self, key):
        self.root = self._insert(self.root, key)


    def _insert(self, root, key):
        """Recursive function to insert key in
        subtree rooted with node and returns
        new root of subtree."""
        # Step 1 - Perform normal BST
        if not root:
            return TreeNode(key)
        elif key < root.value:
            root.left = self._insert(root.left, key)
        else:
            root.right = self._insert(root.right, key)
 
        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self._get_height(root.left),
                              self._get_height(root.right))
 
        # Step 3 - Get the balance factor
        balance = self._get_balance(root)
 
        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and key < root.left.value:
            return self._right_rotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and key > root.right.value:
            return self._left_rotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and key > root.left.value:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and key < root.right.value:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)
 
        return root
    

    def delete_node(self, key):
        self.root = self._delete_node(self.root, key)
    

    def _delete_node(self, root, key):
        # Find the node to be deleted and remove it
        if not root:
            return root
        elif key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self._delete_node(root.right,
                                          temp.key)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self._get_height(root.left),
                              self._get_height(root.right))

        balanceFactor = self._get_balance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self._right_rotate(root)
            else:
                root.left = self._left_rotate(root.left)
                return self._right_rotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self._left_rotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self._left_rotate(root)
        return root    


    def _left_rotate(self, alpha):
        beta         = alpha.right
        gamma        = beta.left
        # Perform rotation
        beta.left    = alpha
        alpha.right  = gamma
        # Update heights
        alpha.height = 1 + max(self._get_height(alpha.left ),
                               self._get_height(alpha.right))
        beta.height  = 1 + max(self._get_height(beta .left ),
                               self._get_height(beta .right))
        # Return the new root
        return beta


    def _right_rotate(self, alpha):
        beta         = alpha.left
        gamma        = beta.right
        # Perform rotation
        beta.right   = alpha
        alpha.left   = gamma
        # Update heights
        alpha.height = 1 + max(self._get_height(alpha.left ),
                               self._get_height(alpha.right))
        beta.height  = 1 + max(self._get_height(beta .left ),
                               self._get_height(beta .right))
        # Return the new root
        return beta


    def _get_height(self, root):
        if not root:
            return 0
        return root.height


    def _get_balance(self, root):
        if not root:
            return 0
        return self._get_height(root.left) - self._get_height(root.right)


if __name__ == '__main__':
    tree1 = AVL_Tree()
    values = (10, 20, 30, 40, 50, 25)
    for val in values:
        tree1.insert(val)

    print(f"constructed AVL tree from {values} is")
    print(f'\n{tree1}\n')

    numbers = [x for x in range(1, 32 + 1)]
    random.shuffle(numbers)
    tree2 = AVL_Tree()
    for num in numbers:
        tree2.insert(num)
    print(f"{min(numbers)} to {max(numbers)} in random order added to tree\n{tree2}")
    print(f'\n\nRaw tree information:\n{tree2.raw_stringify()}')
