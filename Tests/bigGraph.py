
#
# Copyright 2015 Horde Software Inc.
#

import sys
from PySide import QtGui, QtCore

# Add the pyflowgraph module to the current environment if it does not already exist
import imp
try:
    imp.find_module('pyflowgraph')
    found = True
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")))

from pyflowgraph.graph_view import GraphView
from pyflowgraph.graph_view_widget import GraphViewWidget
from pyflowgraph.node import Node
from pyflowgraph.port import InputPort, OutputPort, IOPort

print GraphView

app = QtGui.QApplication(sys.argv)

widget = GraphViewWidget()
graph = GraphView(parent=widget)

# generate a diamod shape graph.
totalCount = 0
def generateNodes(count, offset, depth):
    for i in range(count):
        node1 = Node(graph, 'node' + str(depth) + str(i))
        node1.addPort(InputPort(node1, graph, 'InPort', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
        node1.addPort(OutputPort(node1, graph, 'OutPort', QtGui.QColor(32, 255, 32, 255), 'MyDataX'))
        node1.setGraphPos(QtCore.QPointF(offset, i * 80 ))

        graph.addNode(node1)

        global totalCount
        totalCount += 1

    if depth < 6:
        generateNodes( count * 2, offset+160, depth+1)

        for i in range(count):
            graph.connectPorts('node' + str(depth) + str(i), 'OutPort', 'node' + str(depth+1) + str(i*2), 'InPort')
            graph.connectPorts('node' + str(depth) + str(i), 'OutPort', 'node' + str(depth+1) + str(i*2+1), 'InPort')
    elif depth < 12:
        generateNodes( int(count / 2), offset+160, depth+1)

        for i in range(count/2):
            graph.connectPorts('node' + str(depth) + str(i), 'OutPort', 'node' + str(depth+1) + str(int(i)), 'InPort')


generateNodes( 1, 0, 0)
print "totalCount:" + str(totalCount)

widget.setGraphView(graph)
widget.show()

sys.exit(app.exec_())