import random
from functools import cache

def intPow(val, pow):
    assert pow >= 0
    return int(val ** pow + 0.0001)

@cache
def doublePlusOne(val):
    assert val >= 0
    if val == 0:
        return 0
    return 2 * doublePlusOne(val - 1) + 1

class TreeNode(object):
    """Note of tree"""
    def __init__(self, val):
        self.value  = val
        self.left   = None
        self.right  = None
        self.height = 1

    def stringify(self, maxWidth=2):
        grid = TreeNode.add_node_to_grid(self)
        return TreeNode.stringify_grid(grid, maxWidth)
    

    def __str__(self):
        return self.stringify()
    

    @staticmethod
    def add_node_to_grid(node, grid=None, yPos=0, xPos=0):
        """Used to print out tree at end"""
        if grid is None:
            grid = {}
        grid.setdefault(yPos, {})
        grid[yPos][xPos] = node
        if node.left is not None:
            # are we positive or negative?
            newXpos = -1 # only true in root case
            if xPos < 0:
                newXpos = 2 * xPos
            elif xPos > 0:
                newXpos = 2 * xPos - 1
            TreeNode.add_node_to_grid(node.left, grid, yPos + 1, newXpos)
        if node.right is not None:
            # are we positive or negative?
            newXpos = 1 # only true in root case
            if xPos < 0:
                newXpos = 2 * xPos + 1
            elif xPos > 0:
                newXpos = 2 * xPos
            TreeNode.add_node_to_grid(node.right, grid, yPos + 1, newXpos)
        return grid
    

    @staticmethod
    def simple_stringify_grid(grid):
        """Diagnostic stringification to make sure grid setup correctly."""
        retStr = ''
        for layer, row in sorted(grid.items()):
            retStr += f'{layer} :  '
            for xPos, node in sorted(row.items()):
                nodeVal = f'{node.value:2}'
                extra   = ''
                if node.left:
                    extra += f'L{node.left.value:2}'
                if node.right:
                    if extra:
                        extra += ' '
                    extra += f'R{node.right.value:2}'
                if extra:
                    nodeVal += f' ({extra})'
                retStr += f'{xPos:3} {nodeVal},  '
            retStr += '\n'
        return retStr


    @staticmethod
    def stringify_grid(grid, maxWidth=2):
        # how many layers deep is this grid
        deep   = len(grid)
        fmtStr = '{:<%d}' % maxWidth
        retStr = ''
        empty  = ' ' * maxWidth
        left   = fmtStr.format(' ' * ( maxWidth      // 2) + '/' )
        right  = fmtStr.format(' ' * ((maxWidth - 1) // 2) + '\\')
        for layer, row in sorted(grid.items()):
            # TODO: put in /\ where appropriate
            # should be 0 for last row
            fromBot = deep - layer - 1
            if fromBot:
                before  = intPow(2, fromBot    ) - 1
                between = intPow(2, fromBot    ) - 1
                midSlsh = before
                aftSlsh = befSlsh = doublePlusOne(fromBot + 1)    
                befSlsh = doublePlusOne(fromBot - 1)
            else:
                before  = 0
                between = 1
                # won't get used
                midSlsh = None
                aftSlsh = None
                befSlsh = None
            numSlsh = intPow(2, layer)
            print(f'{layer=} {deep=} {fromBot=} {before=} {between=}')
            maxPos  = int(2 ** (layer - 1) + 0.01)
            retStr += empty * before
            for pos in range(-maxPos, maxPos + 1):
                node = row.get(pos)
                if node:
                    value = node.value
                else:
                    value = ''
                retStr += fmtStr.format(value) + empty * between
            retStr += '\n'
            if not fromBot:
                # don't put toothpicks on bottom row
                break
            retStr += empty * befSlsh
            for _ in range(numSlsh):
                retStr += left + empty * midSlsh + right + empty * aftSlsh
            retStr += '\n'

        return retStr


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

    numbers = [x for x in range(1, 16)]
    random.shuffle(numbers)
    otherTree = AVL_Tree()
    for num in numbers:
        otherTree.insert(num)
    print(f"1 to 100 in random order added to tree\n{otherTree}")
    print(f'\n\n{otherTree.stringify()}')