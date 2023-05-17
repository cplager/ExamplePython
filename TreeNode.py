from functools import cache

def intPow(val, pow):
    if pow < 0:
        return 0
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
        self._value = val
        self.left   = None
        self.right  = None
        self.height = 1

    def stringify(self, maxWidth=2):
        grid = TreeNode.add_node_to_grid(self)
        return TreeNode.stringify_grid(grid, maxWidth)
    

    def __str__(self):
        return self.stringify()
    

    @property
    def value(self):
        # in derived classes, we may want to override this
        return self._value
    

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
    def stringify_grid(grid, maxWidth=2, verbose=False):
        # how many layers deep is this grid
        deep   = len(grid)
        fmtStr = '{:<%d}' % maxWidth
        retStr = ''
        empty  = ' ' * maxWidth
        left   = fmtStr.format(' ' * ( maxWidth      // 2) + '/' )
        right  = fmtStr.format(' ' * ((maxWidth - 0) // 2) + '\\')
        for layer, row in sorted(grid.items()):
            # TODO: put in /\ where appropriate
            # should be 0 for last row
            fromBot = deep - layer - 1
            if fromBot:
                before  = intPow(2, fromBot    ) - 1
                between = intPow(2, fromBot + 1) - 1
                midSlsh = intPow(2, fromBot    ) - 2
                aftSlsh = befSlsh = doublePlusOne(fromBot) + 1
                befSlsh = doublePlusOne(fromBot - 1)
            else:
                before  = 0
                between = 1
                # won't get used
                midSlsh = 0
                aftSlsh = 0
                befSlsh = 0
            ## if layer == 1:
            ##     between = before
            numSlsh = intPow(2, layer)
            maxPos  = intPow(2, layer - 1)
            if verbose:
                print(f'{layer=} {maxPos=} {deep=} {fromBot=} {before=:2} ' +
                      f'{between=:2} {befSlsh=} {midSlsh=:2} {aftSlsh=:2}')
            if before:
                retStr += empty * before
            for pos in range(-maxPos, maxPos + 1):
                node = row.get(pos)
                if node is None and not pos:
                    continue
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


