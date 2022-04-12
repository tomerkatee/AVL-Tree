import avl_skeleton
import random

def main():
    t1 = random_tree(10, 10, 19)
    t2 = random_tree(5, 20, 29)
    t1.concat(t2)
    print("\n".join(printree(t1.getRoot(), bykey=False)))
    t3 = avl_skeleton.AVLTreeList()
    for i in range(10):
        t3.insert(i, i)
    t4 = avl_skeleton.AVLTreeList()
    for i in range(10, 20):
        t4.insert(i-10, i)

    print("\n".join(printree(t3.getRoot(), bykey=False)))
    print("\n".join(printree(t4.getRoot(), bykey=False)))
    t3.concat(t4)
    print("\n".join(printree(t3.getRoot(), bykey=False)))


def printree(t, bykey=True):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    # for row in trepr(t, bykey):
    #        print(row)
    return trepr(t, bykey)

def trepr(t, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if t == None:
        return ["#"]

    thistr = str(t.key) if bykey else str(t.getValue())

    return conc(trepr(t.left, bykey), thistr, trepr(t.right, bykey))

def conc(left, root, right):
    """Return a concatenation of textual represantations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result



def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1

def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i

def try_random_tree(length, min, max):
    t = avl_skeleton.AVLTreeList()
    inserts = []
    while t.length() < length:
        print("\n".join(printree(t.getRoot(), bykey=False)))
        action = random.randint(0, t.length()), random.randint(min, max)
        inserts.append(action)
        try:
            t.insert(action[0], action[1])
        except:
            return inserts
    return t

def random_tree(length, min, max):
    t = avl_skeleton.AVLTreeList()
    while t.length() < length:
        t.insert(random.randint(0, t.length()), random.randint(min, max))
    return t

if __name__ == '__main__':
    main()