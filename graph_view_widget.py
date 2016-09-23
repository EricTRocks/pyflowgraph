
#
# Copyright 2015 Horde Software Inc.
#

import sys
from PySide import QtGui, QtCore

from graph_view import GraphView

class GraphViewWidget(QtGui.QWidget):

    rigNameChanged = QtCore.Signal()

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)
        self.openedFile = None
        self.setObjectName('graphViewWidget')
        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)


    def setGraphView(self, graphView):

        self.graphView = graphView

        # Setup Layout
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.graphView)
        self.setLayout(layout)

        #########################
        ## Setup hotkeys for the following actions.
        deleteShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.graphView.deleteSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        frameShortcut.activated.connect(self.graphView.frameSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        frameShortcut.activated.connect(self.graphView.frameAllNodes)


    def getGraphView(self):
        return self.graphView



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    widget = GraphViewWidget()
    graph = GraphView(parent=widget)

    from node import Node
    from port import InputPort, OutputPort, IOPort

    node1 = Node(graph, 'Short')
    node1.addPort(InputPort(node1, graph, 'InPort1', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node1.addPort(InputPort(node1, graph, 'InPort2', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node1.addPort(OutputPort(node1, graph, 'OutPort', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node1.addPort(IOPort(node1, graph, 'IOPort1', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node1.addPort(IOPort(node1, graph, 'IOPort2', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node1.setGraphPos(QtCore.QPointF( -100, 0 ))

    graph.addNode(node1)

    node2 = Node(graph, 'ReallyLongLabel')
    node2.addPort(InputPort(node2, graph, 'InPort1', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node2.addPort(InputPort(node2, graph, 'InPort2', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node2.addPort(OutputPort(node2, graph, 'OutPort', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node2.addPort(IOPort(node2, graph, 'IOPort1', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node2.addPort(IOPort(node2, graph, 'IOPort2', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node2.setGraphPos(QtCore.QPointF( 100, 0 ))

    graph.addNode(node2)

    widget.setGraphView(graph)
    widget.show()

    sys.exit(app.exec_())