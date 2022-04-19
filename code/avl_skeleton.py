# username - tomerkatee
# id1      - 214166027
# name1    - tomer katee
# id2      - complete info
# name2    - complete info


"""A class represnting a node in an AVL tree"""

"""@inv: virtual nodes cannot have virtual sons nor a virtual parent"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    @type value: AVLNode
    @param parent: the parent of the node
    """

    def __init__(self, value=None, parent=None, virtual=False):
        self.parent = parent
        if virtual:  # creating a virtual node
            self.value = None
            self.height = -1
            self.size = 0
            self.left = None
            self.right = None
        else:  # creating a normal node with virtual sons
            self.value = value
            self.height = 0
            self.size = 1
            self.left = AVLNode(parent=self, virtual=True)
            self.right = AVLNode(parent=self, virtual=True)

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

    """returns whether self has a parent 

    @rtype: bool
    """

    def hasParent(self):
        return self.parent is not None

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

    """sets the height of self by the maximum of its direct sons heights."""

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

    """sets the size of self by the sum of its direct sons sizes."""

    def setSizeBySons(self):
        self.set_size(1 + self.getRight().size + self.getLeft().size)

    """sets the size and height of self according to its direct sons."""

    def setHeightAndSizeBySons(self):
        self.setSizeBySons()
        self.setHeightBySons()

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

    @type root: AVLNode
    @param root: the root node of the new tree, None by default
    """

    def __init__(self, root=None, firstVal=None, lastVal=None):
        if root is not None and not root.isRealNode():  # if root is virtual then an empty tree will be created
            self.root = None
        else:
            self.root = root
        self.firstVal = firstVal
        self.lastVal = lastVal


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
        if 0 <= i < self.length():
            return self.select(i + 1).getValue()  # select the relevant node reference and return its value

    """selects the node of rank i in the rank tree representing the list

    @type i: int
    @param i: rank in the rank tree
    @rtype: AVLNode
    @returns: reference to the node of rank i, or the last node's right virtual son if non existent.
    """

    def select(self, i):
        if not self.empty():
            return AVLTreeList.select_from_subtree(self.root, i)

    """selects the node of rank i in the given subtree

    @comp: O(log(n))
    @type i: int
    @param i: rank in the subtree
    @rtype: AVLNode
    @returns: reference to the node of rank i, or the last node's right virtual son if non existent.
    """

    @staticmethod
    def select_from_subtree(node, i):  # implements select on a rank tree as taught in class
        if not node.isRealNode():
            return node
        if node.getLeft().getSize() + 1 == i:
            return node
        if node.getLeft().getSize() < i:
            return AVLTreeList.select_from_subtree(node.getRight(), i - node.getLeft().getSize() - 1)
        return AVLTreeList.select_from_subtree(node.getLeft(), i)

    """inserts val at position i in the list

    @comp: O(log(n))
    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        if i == 0:
            self.firstVal = val
        if i == self.length():
            self.lastVal = val
        if 0 <= i <= self.length():
            if self.empty():
                self.root = AVLNode(val)
                return 0
            next = self.select(i + 1)  # selecting the current node of rank i+1 which will become rank i+2
            if (next.getLeft() is not None) and (not next.getLeft().isRealNode()):  # meaning that next has no left son
                next.setLeft(AVLNode(val, next))
                return self.fix_tree(next)
            else:  # next has a left son so we insert to the right of node i
                predecessor = self.select(i)
                predecessor.setRight(AVLNode(val, predecessor))
                return self.fix_tree(predecessor)

    """inserts a new node with the given value at the end of the list"""

    def insert_last(self, val):
        return self.insert(self.length(), val)

    """inserts a new node with the given value at the beginning of the list"""

    def insert_first(self, val):
        return self.insert(0, val)

    """ fixes the tree by rotations and size/height sets to maintain AVL rank tree properties from a given start node
    complexity: O(log(n))

    @pre: node is not None
    @type node: AVLNode
    @param node: the node to begin fixing from, climbing upwards to the root
    @rtype: int
    @returns: the number of actions needed to maintain AVL balance and the height field.
    """

    def fix_tree(self, node: AVLNode):
        fix_cnt = 0
        while node is not None:
            new_root = node
            rotated=False
            if abs(node.getBalanceFactor()) > 1:
                fix_cnt += AVLTreeList.perform_rotation(node)
                rotated = True
            height_before = node.getHeight()
            node.setHeightAndSizeBySons()
            if not rotated and height_before != node.getHeight():
                fix_cnt += 1
            node = node.getParent()
        self.root = new_root
        return fix_cnt

    """ performs a rotation on the given node according to its balance factor (as taught in class)

    @pre: node is not None
    @type node: AVLNode
    @param node: the node on which we rotate
    @rtype: int
    @returns: the number of mini-rotations in the rotation perform
    """

    @staticmethod
    def perform_rotation(node: AVLNode):
        if node.getBalanceFactor() == 2:
            if node.getLeft().getBalanceFactor() == -1:
                AVLTreeList.rotate_left_then_right(node)
                return 2
            else:
                AVLTreeList.rotate_right(node)
                return 1
        else:
            if node.getRight().getBalanceFactor() == 1:
                AVLTreeList.rotate_right_then_left(node)
                return 2
            else:
                AVLTreeList.rotate_left(node)
                return 1

    @staticmethod
    def rotate_right(father_node: AVLNode):
        left = father_node.getLeft()
        father_node.setLeft(left.getRight())
        father_node.getLeft().setParent(father_node)
        left.setRight(father_node)
        left.setParent(father_node.getParent())
        father_node.setParent(left)
        if left.hasParent():
            if left.getParent().getRight() == father_node:
                left.getParent().setRight(left)
            else:
                left.getParent().setLeft(left)
        father_node.setHeightAndSizeBySons()
        left.setHeightAndSizeBySons()

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
        if leftRight.hasParent():
            if leftRight.getParent().getRight() == father_node:
                leftRight.getParent().setRight(leftRight)
            else:
                leftRight.getParent().setLeft(leftRight)
        left.setHeightAndSizeBySons()
        father_node.setHeightAndSizeBySons()
        leftRight.setHeightAndSizeBySons()

    @staticmethod
    def rotate_left(father_node: AVLNode):
        right = father_node.getRight()
        father_node.setRight(right.getLeft())
        father_node.getRight().setParent(father_node)
        right.setLeft(father_node)
        right.setParent(father_node.getParent())
        father_node.setParent(right)
        if right.hasParent():
            if right.getParent().getLeft() == father_node:
                right.getParent().setLeft(right)
            else:
                right.getParent().setRight(right)
        father_node.setHeightAndSizeBySons()
        right.setHeightAndSizeBySons()

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
        if rightLeft.hasParent():
            if rightLeft.getParent().getLeft() == father_node:
                rightLeft.getParent().setLeft(rightLeft)
            else:
                rightLeft.getParent().setRight(rightLeft)
        right.setHeightAndSizeBySons()
        father_node.setHeightAndSizeBySons()
        rightLeft.setHeightAndSizeBySons()

    """returns the predecessor of the given node
    complexity: O(log(n))

    @pre: node.isRealNode() == True
    @type node: AVLNode
    @param node: the node of which we return the predecessor
    @rtype: AVLNode
    @returns: a reference to the predecessor
    """

    @staticmethod
    def predecessor(node):
        if node.getLeft().isRealNode():
            return AVLTreeList.subtree_max(node.getLeft())
        parent = node.getParent()
        while parent is not None and parent.getRight() != node:
            node = parent
            parent = node.getParent()
        return parent

    """returns the successor of the given node
    complexity: O(log(n))

    @pre: node.isRealNode() == True
    @type node: AVLNode
    @param node: the node of which we return the successor
    @rtype: AVLNode
    @returns: a reference to the successor
    """

    @staticmethod
    def successor(node):
        if node.getRight().isRealNode():
            return AVLTreeList.subtree_min(node.getRight())
        parent = node.getParent()
        while parent is not None and parent.getLeft() != node:
            node = parent
            parent = node.getParent()
        return parent

    """ returns the leftmost offspring of the given node
    complexity: O(log(n))

    @pre node.isRealNode() == True
    @type node: AVLNode
    @param node: the node of which we return the leftmost offspring
    @rtype: AVLNode
    @returns: a reference to the leftmost offspring or the node himself if it has no left sons
    """

    @staticmethod
    def subtree_min(node):
        while node.getLeft().isRealNode():
            node = node.getLeft()
        return node

    """ returns the rightmost offspring of the given node
    complexity: O(log(n))

    @pre node.isRealNode() == True
    @type node: AVLNode
    @param node: the node of which we return the rightmost offspring
    @rtype: AVLNode
    @returns: a reference to the rightmost offspring or the node himself if it has no right sons
    """

    @staticmethod
    def subtree_max(node):
        while node.getRight().isRealNode():
            node = node.getRight()
        return node

    """deletes the i'th item in the list
    complexity: O(log(n))

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        if 0 <= i < self.length():
            target = self.select(i + 1)  # selecting the target of deletion
            if target.getLeft().isRealNode() and target.getRight().isRealNode():  # if target has two children delete the successor
                succ = AVLTreeList.successor(target)
                target.setValue(succ.getValue())
                target = succ                       # now target has only one son or no sons
            if i == 0:
                succ = AVLTreeList.successor(target)
                self.firstVal = None if succ is None else succ.getValue()
            if i == self.length() - 1:
                pred = AVLTreeList.predecessor(target)
                self.lastVal = None if pred is None else pred.getValue()
            if target == self.root:
                if target.getLeft().isRealNode():
                    target.getLeft().setParent(None)
                    self.root = target.getLeft()
                elif target.getRight().isRealNode():
                    target.getRight().setParent(None)
                    self.root = target.getRight()
                else:
                    self.root = None
                return 0
            elif target.getParent().getLeft() == target:  # deleting the successor according to its parent and son
                if target.getLeft().isRealNode():
                    target.getParent().setLeft(target.getLeft())
                    target.getLeft().setParent(target.getParent())
                else:
                    target.getParent().setLeft(target.getRight())
                    target.getRight().setParent(target.getParent())
            else:
                if target.getLeft().isRealNode():
                    target.getParent().setRight(target.getLeft())
                    target.getLeft().setParent(target.getParent())
                else:
                    target.getParent().setRight(target.getRight())
                    target.getRight().setParent(target.getParent())
            return self.fix_tree(target.getParent())
        return -1

    """returns the value of the first item in the list
    complexity: O(1)
    
    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        return self.firstVal

    """returns the value of the last item in the list
    complexity: O(1)
    
    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        return self.lastVal

    """returns an array representing list 
    complexity: O(n)

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        list_of_elements = []

        def listToArray_rec(root):  # appends to the list all the elements in the tree from left to right "inorder"
            if root:
                listToArray_rec(root.left)
                if root.isRealNode():
                    list_of_elements.append(root.getValue())
                listToArray_rec(root.right)

        listToArray_rec(self.root)
        return list_of_elements

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return 0 if self.getRoot() is None else self.root.getSize()

    """splits the list at the i'th index
    complexity: O(log(n))

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    """

    def split(self, i):
        splitter = self.select(i + 1)  # the node that splits the list
        splitter.getLeft().setParent(None)
        splitter.getRight().setParent(None)
        small_tree = AVLTreeList(splitter.getLeft())  # tree that will contain the list until the splitter
        big_tree = AVLTreeList(splitter.getRight())  # tree that will contain the list from the splitter to the end
        parent = splitter.getParent()
        before = splitter
        while parent is not None:  # climbing upwards from the splitter to the root
            if parent.getRight() == before:  # if we climbed leftwards it means that parent and parent.left are smaller than splitter
                parent.getLeft().setParent(None)
                left_subtree = AVLTreeList(parent.getLeft())
                left_subtree.insert_last(parent.getValue())
                left_subtree.concat(small_tree)  # adding parent and parent.left to the small tree
                small_tree = left_subtree
            else:  # we climbed rightwards than parent and parent.right are bigger than splitter
                parent.getRight().setParent(None)
                right_subtree = AVLTreeList(parent.getRight())
                big_tree.insert_last(parent.getValue())
                big_tree.concat(right_subtree)  # adding parent and parent.right to the big tree
            before = parent
            parent = parent.getParent()
        small_tree.firstVal = small_tree.retrieve(0)
        small_tree.lastVal = small_tree.retrieve(small_tree.length() - 1)
        big_tree.firstVal = big_tree.retrieve(0)
        big_tree.lastVal = big_tree.retrieve(big_tree.length() - 1)
        return [small_tree, splitter.getValue(), big_tree]

    """concatenates lst to self
    complexity: O(log(n))

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        selfHeight = -1 if self.root is None else self.root.getHeight()
        lstHeight = -1 if lst.root is None else lst.root.getHeight()
        height_diff = abs(selfHeight - lstHeight)
        if lst.empty():  # treating empty-tree corner cases
            return height_diff
        if self.empty():
            self.root = lst.root
            self.firstVal = lst.firstVal
            self.lastVal = lst.lastVal
            return height_diff
        max_node = self.select(self.length())  # getting the last node that will become the seperator between self and lst
        original_first = self.firstVal
        self.delete(self.length() - 1)  # deleting the last node from self
        if self.root is None:  # if self contained only max_node
            lst.insert_first(max_node.getValue())
            self.root = lst.getRoot()
        elif self.root.getHeight() > lst.root.getHeight():
            # on the right branch of self, looking for the first node that its height is smaller/equals lst.root.height
            similar_height_node = self.root
            while similar_height_node.getHeight() > lst.root.getHeight():
                similar_height_node = similar_height_node.getRight()
            # setting max_node.right to lst and max_node.left to SHN and thus fitting lst to the end of self
            max_node.setParent(similar_height_node.getParent())
            if max_node.hasParent():
                max_node.getParent().setRight(max_node)
            similar_height_node.setParent(max_node)
            max_node.setLeft(similar_height_node)
            max_node.setRight(lst.root)
            lst.root.setParent(max_node)
            self.fix_tree(max_node)
        else:  # the symmetrical action, self and lst switch roles
            similar_height_node = lst.root
            while similar_height_node.getHeight() > self.root.getHeight():
                similar_height_node = similar_height_node.getLeft()
            max_node.setParent(similar_height_node.getParent())
            if max_node.hasParent():
                max_node.getParent().setLeft(max_node)
            similar_height_node.setParent(max_node)
            max_node.setRight(similar_height_node)
            max_node.setLeft(self.root)
            self.root.setParent(max_node)
            self.fix_tree(max_node)
        self.lastVal = lst.lastVal
        self.firstVal = original_first
        return abs(height_diff)

    """searches for a *value* in the list
    complexity: O(n)

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        list_of_values = self.listToArray()
        for i in range(len(list_of_values)):
            if list_of_values[i] == val:
                return i
        return -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root
