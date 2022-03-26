# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        if value is None:
            self.height = -1
            self.size = 0
            self.left = None
            self.right = None
        else:
            self.height = 0
            self.size = 1
            self.left = AVLNode(None, self)
            self.right = AVLNode(None, self)



    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """returns the balance factor
    
    @pre: self.isRealNode() == True
    @rtype: int
    @returns: the balance factor of self, -1 if the node is virtual
    """
    def getBalanceFactor(self):
        return self.getLeft().getHeight() - self.getRight().getHeight()


    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    def setHeightBySons(self):
        self.height = 1 + max(self.left.height, self.right.height)

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        return self.size != 0

    """sets the size of the node

    @type h: int
    @param h: the height
    """
    def set_size(self, size):
        self.size = size


    """returns the size

    @rtype: int
    @returns: the size of self, 0 if the node is virtual
    """
    def getSize(self):
        return self.size




"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None

    # add your fields here

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.getRoot() is None

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):
        return self.select(i+1).val

    def select(self, i):
        return AVLTreeList.select_from_subtree(self.root, i)

    @staticmethod
    def select_from_subtree(node, i):
        if not node.isRealNode():
            return node
        if node.getLeft().getSize() + 1 == i:
            return node
        if node.getLeft().getSize() < i:
            return AVLTreeList.select_from_subtree(node.getRight(), i - node.getLeft().getSize() - 1)
        return AVLTreeList.select_from_subtree(node.getLeft(), i)


    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        if 0 <= i <= self.length():
            if self.root is None:
                self.root = AVLNode(val)
                return 0
            next = AVLTreeList.select_from_subtree(self.root, i + 1)
            if (next.getLeft() is not None) and (not next.getLeft().isRealNode()):  # meaning that next has no left son
                next.setLeft(AVLNode(val, next))
                self.root, rot_cnt = AVLTreeList.fix_tree(next)
                return rot_cnt
            else:
                predecessor = AVLTreeList.select_from_subtree(self.root, i)
                predecessor.setRight(AVLNode(val, predecessor))
                self.root, rot_cnt = AVLTreeList.fix_tree(predecessor)
                return rot_cnt



    @staticmethod
    def fix_tree(node: AVLNode):
        rot_cnt = 0
        while node is not None:
            new_root = node
            if abs(node.getBalanceFactor()) > 1:
                AVLTreeList.perform_rotation(node)
                rot_cnt += 1
            node.set_size(1 + node.getRight().size + node.getLeft().size)
            node.setHeightBySons()
            node = node.getParent()
        return new_root, rot_cnt

    @staticmethod
    def perform_rotation(node: AVLNode):
        if node.getBalanceFactor() == 2:
            if node.getLeft().getBalanceFactor() == -1:
                AVLTreeList.rotate_left_then_right(node)
            else:
                AVLTreeList.rotate_right(node)
        else:
            if node.getRight().getBalanceFactor() == 1:
                AVLTreeList.rotate_right_then_left(node)
            else:
                AVLTreeList.rotate_left(node)

    @staticmethod
    def rotate_right(father_node: AVLNode):
        left = father_node.getLeft()
        father_node.setLeft(left.getRight())
        father_node.getLeft().setParent(father_node)
        left.setRight(father_node)
        left.setParent(father_node.getParent())
        father_node.setParent(left)
        if left.getParent() is not None:
            if left.getParent().getRight() == father_node:
                left.getParent().setRight(left)
            else:
                left.getParent().setLeft(left)
        father_node.setHeightBySons()
        left.setHeightBySons()

    @staticmethod
    def rotate_left_then_right(father_node: AVLNode):
        left = father_node.getLeft()
        leftRight = left.getRight()
        father_node.setLeft(leftRight.getRight())
        father_node.getLeft().setParent(father_node)
        left.setRight(leftRight.getLeft())
        left.getRight().setParent(left)
        left.setParent(leftRight)
        leftRight.setParent(father_node.getParent())
        leftRight.setLeft(left)
        leftRight.setRight(father_node)
        father_node.setParent(leftRight)
        if leftRight.getParent is not None:
            if leftRight.getParent().getRight() == father_node:
                leftRight.getParent().setRight(leftRight)
            else:
                leftRight.getParent().setLeft(leftRight)
        left.setHeightBySons()
        father_node.setHeightBySons()
        leftRight.setHeightBySons()

    @staticmethod
    def rotate_left(father_node: AVLNode):
        right = father_node.getRight()
        father_node.setRight(right.getLeft())
        father_node.getRight().setParent(father_node)
        right.setLeft(father_node)
        right.setParent(father_node.getParent())
        father_node.setParent(right)
        if right.getParent() is not None:
            if right.getParent().getLeft() == father_node:
                right.getParent().setLeft(right)
            else:
                right.getParent().setRight(right)
        father_node.setHeightBySons()
        right.setHeightBySons()

    @staticmethod
    def rotate_right_then_left(father_node: AVLNode):
        right = father_node.getRight()
        rightLeft = right.getLeft()
        father_node.setRight(rightLeft.getLeft())
        father_node.getRight().setParent(father_node)
        right.setLeft(rightLeft.getRight())
        right.getLeft().setParent(right)
        right.setParent(rightLeft)
        rightLeft.setParent(father_node.getParent())
        rightLeft.setRight(right)
        rightLeft.setLeft(father_node)
        father_node.setParent(rightLeft)
        if rightLeft.getParent() is not None:
            if rightLeft.getParent().getLeft() == father_node:
                rightLeft.getParent().setLeft(rightLeft)
            else:
                rightLeft.getParent().setRight(rightLeft)
        right.setHeightBySons()
        father_node.setHeightBySons()
        rightLeft.setHeightBySons()



    @staticmethod
    def predecessor(node):
        if node.getLeft().isRealNode():
            return AVLTreeList.tree_max(node.getLeft())
        parent = node.getParent()
        while parent is not None and parent.getLeft() != node:
            node = parent
            parent = node.getParent()
        return parent

    @staticmethod
    def successor(node):
        if node.getRight().isRealNode():
            return AVLTreeList.tree_min(node.getRight())
        parent = node.getParent()
        while parent is not None and parent.getRight() != node:
            node = parent
            parent = node.getParent()
        return parent

    """
    @pre node.isRealNode() == True
    """
    @staticmethod
    def tree_min(node):
        while node.getLeft().isRealNode():
            node = node.getLeft()
        return node

    """
    @pre node.isRealNode() == True
    """
    @staticmethod
    def tree_max(node):
        while node.getRight().isRealNode():
            node = node.getRight()
        return node



    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        if 0 <= i < self.length():
            target = self.select(i+1)
            if target.getLeft().isRealNode() and target.getRight().isRealNode():
                succ = AVLTreeList.successor(target)
                target.setValue(succ.getValue())
                target = succ
            if target.getParent().getLeft() == target:  # now target has only one son
                if target.getLeft().isRealNode():
                    target.getParent().setLeft(target.getLeft())
                else:
                    target.getParent().setLeft(target.getRight())
            else:
                if target.getLeft().isRealNode():
                    target.getParent().setRight(target.getLeft())
                else:
                    target.getParent().setRight(target.getRight())
            self.root, rot_cnt = self.fix_tree(target.getParent())
            return rot_cnt
        return -1


    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        return self.retrieve(0)

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        return None

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        return None

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.root.getSize()

    """splits the list at the i'th index

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    """

    def split(self, i):
        return None

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        return None

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        return None

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root


