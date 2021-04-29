from os import abort
import time
from flask import (Flask, g, redirect, render_template, request,
                   session, url_for, app)
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
app = Flask(__name__)
app.config["SECRET_KEY"] = "hello"
PEOPLE_FOLDER = os.path.join('static', 'result')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config["CACHE_TYPE"] = "null"
app.config["PERMANENT_SESSION_LIFETIME"] = False
class DataItem:

    def __init__(self, dd):
        self.dData = dd

    def displayItem(self):
        return self.dData


class Node:
    _ORDER = 4

    def __init__(self):
        self._numItems = 0
        self._pParent = None
        self._childArray = []
        self._itemArray = []
        for j in range(self._ORDER):
            self._childArray.append(None)
        for k in range(self._ORDER - 1):
            self._itemArray.append(None)

    def connectChild(self, childNum, pChild):
        self._childArray[childNum] = pChild
        if pChild:
            pChild._pParent = self

    def disconnectChild(self, childNum):
        pTempNode = self._childArray[childNum]
        self._childArray[childNum] = None
        return pTempNode

    def getChild(self, childNum):
        return self._childArray[childNum]

    def getParent(self):
        return self._pParent

    def isLeaf(self):
        return not self._childArray[0]

    def getNumItems(self):
        return self._numItems

    def getItem(self, index):
        return self._itemArray[index]

    def isFull(self):
        return self._numItems == self._ORDER - 1

    def findItem(self, key):
        for j in range(self._ORDER - 1):
            if not self._itemArray[j]:
                break
            elif self._itemArray[j].dData == key:
                return j
        return -1

    def insertItem(self, pNewItem):

        self._numItems += 1
        newKey = pNewItem.dData

        for j in reversed(range(self._ORDER - 1)):
            if self._itemArray[j] == None:
                pass
            else:
                itsKey = self._itemArray[j].dData
                if newKey < itsKey:
                    self._itemArray[j + 1] = self._itemArray[j]
                else:
                    self._itemArray[j + 1] = pNewItem
                    return j + 1
        self._itemArray[0] = pNewItem
        return 0

    def removeItem(self):

        pTemp = self._itemArray[self._numItems - 1]
        self._itemArray[self._numItems - 1] = None
        self._numItems -= 1
        return pTemp

    def displayNode(self):
        temp = []
        for j in range(self._numItems):
            temp.append(self._itemArray[j].displayItem())
        return temp


# end class Node

class Tree234:
    def __init__(self):
        self._pRoot = Node()

    def find(self, key):
        pCurNode = self._pRoot
        while True:
            childNumber = pCurNode.findItem(key)
            if childNumber != -1:
                return childNumber
            elif pCurNode.isLeaf():
                return -1
            else:
                pCurNode = self.getNextChild(pCurNode, key)

    def insert(self, dValue):
        pCurNode = self._pRoot
        pTempItem = DataItem(dValue)

        while True:
            if pCurNode.isFull():
                self.split(pCurNode)
                pCurNode = pCurNode.getParent()

                pCurNode = self.getNextChild(pCurNode, dValue)


            elif pCurNode.isLeaf():
                break
            else:
                pCurNode = self.getNextChild(pCurNode, dValue)

        pCurNode.insertItem(pTempItem)

    def split(self, pThisNode):

        pItemC = pThisNode.removeItem()
        pItemB = pThisNode.removeItem()
        pChild2 = pThisNode.disconnectChild(2)
        pChild3 = pThisNode.disconnectChild(3)

        pNewRight = Node()

        if pThisNode == self._pRoot:
            self._pRoot = Node()
            pParent = self._pRoot
            self._pRoot.connectChild(0, pThisNode)
        else:
            pParent = pThisNode.getParent()

        itemIndex = pParent.insertItem(pItemB)
        n = pParent.getNumItems()

        j = n - 1
        while j > itemIndex:
            pTemp = pParent.disconnectChild(j)
            pParent.connectChild(j + 1, pTemp)
            j -= 1

        pParent.connectChild(itemIndex + 1, pNewRight)

        pNewRight.insertItem(pItemC)
        pNewRight.connectChild(0, pChild2)
        pNewRight.connectChild(1, pChild3)

    def getNextChild(self, pNode, theValue):

        numItems = pNode.getNumItems()

        for j in range(numItems):
            if theValue < pNode.getItem(j).dData:
                return pNode.getChild(j)
        else:
            return pNode.getChild(j + 1)

    def displayTree(self):
        self.recDisplayTree(self._pRoot, 0, 0, None)

    def displayTree1(self, arr):
        self.recDisplayTree1(self._pRoot, 0, 0, None, arr)

    def recDisplayTree(self, pThisNode, level, childNumber, parent):
        global array
        array = []
        print('level=', level, 'child=', childNumber, pThisNode.displayNode())
        array.append([level, childNumber, pThisNode.displayNode(), parent])
        numItems = pThisNode.getNumItems()
        for j in range(numItems + 1):
            pNextNode = pThisNode.getChild(j)
            if pNextNode:
                self.recDisplayTree(pNextNode, level + 1, j, pThisNode.displayNode())
            else:
                print(array)
                return

    def recDisplayTree1(self, pThisNode, level, childNumber, parent, arr):
        print('level=', level, 'child=', childNumber, pThisNode.displayNode())
        arr.append([level, childNumber, pThisNode.displayNode(), parent])
        numItems = pThisNode.getNumItems()
        for j in range(numItems + 1):
            pNextNode = pThisNode.getChild(j)
            if pNextNode:
                self.recDisplayTree1(pNextNode, level + 1, j, pThisNode.displayNode(), arr)
            else:
                return

    def changetree(self, nTree):
        self._pRoot = nTree._pRoot


def show():
    pTree.displayTree()


def insert(val):
    value = int(val)
    # for i in value:
    pTree.insert(value)
    iplist.append(value)
    pTree.displayTree()
    return "Inserted"


def find(val):
    value = int(val)
    found = pTree.find(value)
    if found != -1:
        return "Found"
    else:
        return "Couldn't find"


def remove(val):
    nTree = Tree234()
    if len(iplist) == 0:
        return "Can't remove,the tree is empty"
    else:
        value = int(val)
        if iplist.__contains__(value):
            iplist.remove(value)
            pTree.changetree(nTree)
            for i in range(0, len(iplist)):
                pTree.insert(iplist[i])
            pTree.displayTree()
            return "Removed"
        else:
            return "Could not find"


# '''
# case = {
#     'i' : insert,
#     'f' : find,
#     'r'	: remove}


# while True:
#     choice = input('Enter first letter of show, insert, remove, find or exit: ')
#     if choice=='e':
#         break
#     if case.get(choice, None):
#         case[choice]()
#     else:
#         print( 'Invalid entry')'''
def result():
    c = m = 0
    arr = []
    pTree.displayTree1(arr)
    array = arr
    from graphviz import Digraph, nohtml, render
    s = Digraph(name='structs', filename='static/result/structs.gv', node_attr={'shape': 'record'}, format='png')
    for i in range(len(array)):
        if m < array[i][0]:
            m = array[i][0]
        if len(array[i][2]) == 3:
            s.node('struct{}{}{}'.format(array[i][0], array[i][1], array[i][3]),
                   '<f0> {}|<f1> {}|<f2> {}'.format(array[i][2][0], array[i][2][1], array[i][2][2]))
            c += 1
        if len(array[i][2]) == 2:
            s.node('struct{}{}{}'.format(array[i][0], array[i][1], array[i][3]),
                   '<f0> {}|<f1> {}'.format(array[i][2][0], array[i][2][1]))
            c += 1
        if len(array[i][2]) == 1:
            s.node('struct{}{}{}'.format(array[i][0], array[i][1], array[i][3]), '<f0> {}'.format(array[i][2][0]))
            c += 1
    # for i in range(m):
    # s.edges([('struct{}{}:f0'.format(i,0), 'struct{}{}:f0'.format(i+1,0)), ('struct{}{}:f0'.format(i,0), 'struct{}{}:f0'.format(i+1,1))])
    # s.edges([('struct{}{}:f0'.format(i,1), 'struct{}{}:f0'.format(i+1,0)), ('struct{}{}:f0'.format(i,1), 'struct{}{}:f0'.format(i+1,1))])
    stack = []
    stack.append(array[0])
    for i in range(1, len(array)):
        while len(stack) != 0 and stack[-1][2] != array[i][3]:
            tmp = stack.pop()
        s.edges([('struct{}{}{}:f0'.format(stack[-1][0], stack[-1][1], stack[-1][3]),
                  'struct{}{}{}:f0'.format(array[i][0], array[i][1], array[i][3]))])
        stack.append(array[i])
    #  print(stack)
    s.render(filename="static/result/structs", view=False)


# s.edges([('struct{}{}:f0'.format(0,0), 'struct{}{}:f0'.format(1,0)), ('struct{}{}:f0'.format(0,0), 'struct{}{}:f0'.format(1,1))])
# s.edges([('struct{}{}:f0'.format(1,0), 'struct{}{}:f0'.format(2,0)), ('struct{}{}:f0'.format(1,0), 'struct{}{}:f0'.format(2,1))])

#  1 2 3 4 5 6 7 8 9 10 11

# del pTree

@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method =='POST':
         num = request.form.get('insert')
         print(num)
         return "number,{num}"
    return render_template('index.html')


@app.route('/sendkey', methods=['POST'])
def sendkey():
    if not request.form or not 'ki' in request.form:
        abort(400, 'required parameters not present')
        return
    ki = request.form['ki']
    x = insert(ki)
    result()
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'structs.png')
    return render_template('index.html', ima=full_filename, ki=x)
    for file in os.listdir('C:\\Users\\Sai Rajaram\\Desktop\\test\\static\\result'):
        if file.endswith('.png'):
            os.remove(file)


@app.route('/remove', methods=['POST'])
def rem():
    if not request.form or not 'ki' in request.form:
        abort(400, 'required parameters not present')
        return
    ki = request.form['ki']
    x = remove(ki)
    result()
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'structs.png')
    return render_template('index.html', ima=full_filename, ki=x)


@app.route('/find', methods=['POST'])
def findk():
    if not request.form or not 'ki' in request.form:
        abort(400, 'required parameters not present')
        return
    ki = request.form['ki']
    x = find(ki)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'structs.png')
    return render_template('index.html', ima=full_filename, ki=x)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == "__main__":
    pTree = Tree234()
    iplist = []
    nTree = Tree234()
    array = []
    app.run(port=8000, debug=True)
