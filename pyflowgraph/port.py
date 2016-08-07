
#
# Copyright 2015 Horde Software Inc.
#

import json
from qtpy import QtGui, QtWidgets, QtCore


class PortLabel(QtWidgets.QGraphicsWidget):
    __font = QtGui.QFont('Decorative', 12)

    def __init__(self, port, text, hOffset, color, highlightColor):
        super(PortLabel, self).__init__(port)
        self.__port = port
        self.__text = text
        self.__textItem = QtWidgets.QGraphicsTextItem(text, self)
        self._labelColor = color
        self.__highlightColor = highlightColor
        self.__textItem.setDefaultTextColor(self._labelColor)
        self.__textItem.setFont(self.__font)
        self.__textItem.transform().translate(0, self.__font.pointSizeF() * -0.5)
        option = self.__textItem.document().defaultTextOption()
        option.setWrapMode(QtGui.QTextOption.NoWrap)
        self.__textItem.document().setDefaultTextOption(option)
        self.__textItem.adjustSize()

        self.setPreferredSize(self.textSize())
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.setWindowFrameMargins(0, 0, 0, 0)
        self.setHOffset(hOffset)

        self.setAcceptHoverEvents(True)
        self.__mousDownPos = None

    def text(self):
        return self.__text


    def setHOffset(self, hOffset):
        self.transform().translate(hOffset, 0)


    def setColor(self, color):
        self.__textItem.setDefaultTextColor(color)
        self.update()


    def textSize(self):
        return QtCore.QSizeF(
            self.__textItem.textWidth(),
            self.__font.pointSizeF()
            )


    def getPort(self):
        return self.__port


    def highlight(self):
        self.setColor(self.__highlightColor)


    def unhighlight(self):
        self.setColor(self._labelColor)


    def hoverEnterEvent(self, event):
        self.highlight()
        super(PortLabel, self).hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        self.unhighlight()
        super(PortLabel, self).hoverLeaveEvent(event)


    def mousePressEvent(self, event):
        self.__mousDownPos = self.mapToScene(event.pos())


    def mouseMoveEvent(self, event):
        self.unhighlight()
        scenePos = self.mapToScene(event.pos())

        # When clicking on an UI port label, it is ambigous which connection point should be activated.
        # We let the user drag the mouse in either direction to select the conneciton point to activate.
        delta = scenePos - self.__mousDownPos
        if delta.x() < 0:
            if self.__port.inCircle() is not None:
                self.__port.inCircle().mousePressEvent(event)
        else:
            if self.__port.outCircle() is not None:
                self.__port.outCircle().mousePressEvent(event)

    # def paint(self, painter, option, widget):
    #     super(PortLabel, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 255)))
    #     painter.drawRect(self.windowFrameRect())


class PortCircle(QtWidgets.QGraphicsWidget):

    __radius = 4.5
    __diameter = 2 * __radius

    def __init__(self, port, graph, hOffset, color, connectionPointType):
        super(PortCircle, self).__init__(port)

        self.__port = port
        self._graph = graph
        self._connectionPointType = connectionPointType
        self.__connections = set()
        self._supportsOnlySingleConnections = connectionPointType == 'In'

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        size = QtCore.QSizeF(self.__diameter, self.__diameter)
        self.setPreferredSize(size)
        self.setWindowFrameMargins(0, 0, 0, 0)

        self.transform().translate(self.__radius * hOffset, 0)

        self.__defaultPen = QtGui.QPen(QtGui.QColor(25, 25, 25), 1.0)
        self.__hoverPen = QtGui.QPen(QtGui.QColor(255, 255, 100), 1.5)

        self._ellipseItem = QtWidgets.QGraphicsEllipseItem(self)
        self._ellipseItem.setPen(self.__defaultPen)
        self._ellipseItem.setPos(size.width()/2, size.height()/2)
        self._ellipseItem.setRect(
            -self.__radius,
            -self.__radius,
            self.__diameter,
            self.__diameter,
            )
        if connectionPointType == 'In':
            self._ellipseItem.setStartAngle(270 * 16)
            self._ellipseItem.setSpanAngle(180 * 16)

        self.setColor(color)
        self.setAcceptHoverEvents(True)

    def getPort(self):
        return self.__port


    def getColor(self):
        return self.getPort().getColor()


    def centerInSceneCoords(self):
        return self._ellipseItem.mapToScene(0, 0)


    def setColor(self, color):
        self._color = color
        self._ellipseItem.setBrush(QtGui.QBrush(self._color))


    def setDefaultPen(self, pen):
        self.__defaultPen = pen
        self._ellipseItem.setPen(self.__defaultPen)


    def setHoverPen(self, pen):
        self.__hoverPen = pen


    def highlight(self):
        self._ellipseItem.setBrush(QtGui.QBrush(self._color.lighter()))
        # make the port bigger to highlight it can accept the connection.
        self._ellipseItem.setRect(
            -self.__radius * 1.3,
            -self.__radius * 1.3,
            self.__diameter * 1.3,
            self.__diameter * 1.3,
            )


    def unhighlight(self):
        self._ellipseItem.setBrush(QtGui.QBrush(self._color))
        self._ellipseItem.setRect(
            -self.__radius,
            -self.__radius,
            self.__diameter,
            self.__diameter,
            )


    # ===================
    # Connection Methods
    # ===================
    def connectionPointType(self):
        return self._connectionPointType

    def isInConnectionPoint(self):
        return self._connectionPointType == 'In'

    def isOutConnectionPoint(self):
        return self._connectionPointType == 'Out'

    def supportsOnlySingleConnections(self):
        return self._supportsOnlySingleConnections

    def setSupportsOnlySingleConnections(self, value):
        self._supportsOnlySingleConnections = value

    def canConnectTo(self, otherPortCircle):

        if self.connectionPointType() == otherPortCircle.connectionPointType():
            return False

        if self.getPort().getDataType() != otherPortCircle.getPort().getDataType():
            return False

        # Check if you're trying to connect to a port on the same node.
        # TODO: Do propper cycle checking..
        otherPort = otherPortCircle.getPort()
        port = self.getPort()
        if otherPort.getNode() == port.getNode():
            return False

        return True

    def addConnection(self, connection):
        """Adds a connection to the list.
        Arguments:
        connection -- connection, new connection to add.
        Return:
        True if successful.
        """

        if self._supportsOnlySingleConnections and len(self.__connections) != 0:
            # gather all the connections into a list, and then remove them from the graph.
            # This is because we can't remove connections from ports while
            # iterating over the set.
            connections = []
            for c in self.__connections:
                connections.append(c)
            for c in connections:
                self._graph.removeConnection(c)

        self.__connections.add(connection)

        return True

    def removeConnection(self, connection):
        """Removes a connection to the list.
        Arguments:
        connection -- connection, connection to remove.
        Return:
        True if successful.
        """

        self.__connections.remove(connection)

        return True

    def getConnections(self):
        """Gets the ports connections list.
        Return:
        List, connections to this port.
        """

        return self.__connections

    # ======
    # Events
    # ======
    def hoverEnterEvent(self, event):
        self.highlight()
        super(PortCircle, self).hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        self.unhighlight()
        super(PortCircle, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):

        self.unhighlight()

        scenePos = self.mapToScene(event.pos())

        from .mouse_grabber import MouseGrabber
        if self.isInConnectionPoint():
            MouseGrabber(self._graph, scenePos, self, 'Out')
        elif self.isOutConnectionPoint():
            MouseGrabber(self._graph, scenePos, self, 'In')


    # def paint(self, painter, option, widget):
    #     super(PortCircle, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0)))
    #     painter.drawRect(self.windowFrameRect())


class ItemHolder(QtWidgets.QGraphicsWidget):
    """docstring for ItemHolder"""
    def __init__(self, parent):
        super(ItemHolder, self).__init__(parent)

        layout = QtWidgets.QGraphicsLinearLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def setItem(self, item):
        item.setParentItem(self)
        self.layout().addItem(item)

    # def paint(self, painter, option, widget):
    #     super(ItemHolder, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0)))
    #     painter.drawRect(self.windowFrameRect())



class BasePort(QtWidgets.QGraphicsWidget):

    _labelColor = QtGui.QColor(25, 25, 25)
    _labelHighlightColor = QtGui.QColor(225, 225, 225, 255)

    def __init__(self, parent, graph, name, color, dataType, connectionPointType):
        super(BasePort, self).__init__(parent)

        self._node = parent
        self._graph = graph
        self._name = name
        self._dataType = dataType
        self._connectionPointType = connectionPointType

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))

        layout = QtWidgets.QGraphicsLinearLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._color = color

        self._inCircle = None
        self._outCircle = None
        self._labelItem = None

        self._inCircleHolder = ItemHolder(self)
        self._outCircleHolder = ItemHolder(self)
        self._labelItemHolder = ItemHolder(self)

        self.layout().addItem(self._inCircleHolder)
        self.layout().setAlignment(self._inCircleHolder, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.layout().addItem(self._labelItemHolder)
        self.layout().setAlignment(self._labelItemHolder, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.layout().addItem(self._outCircleHolder)
        self.layout().setAlignment(self._outCircleHolder, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


    def getName(self):
        return self._name


    def getDataType(self):
        return self._dataType


    def getNode(self):
        return self._node


    def getGraph(self):
        return self._graph


    def getColor(self):
        return self._color


    def setColor(self, color):
        if self._inCircle is not None:
            self._inCircle.setColor(color)
        if self._outCircle is not None:
            self._outCircle.setColor(color)
        self._color = color


    def inCircle(self):
        return self._inCircle


    def setInCircle(self, inCircle):
        self._inCircleHolder.setItem(inCircle)
        self._inCircle = inCircle
        self.layout().insertStretch(2, 2)
        self.updatecontentMargins()

    def outCircle(self):
        return self._outCircle


    def setOutCircle(self, outCircle):
        self._outCircleHolder.setItem(outCircle)
        self._outCircle = outCircle
        self.layout().insertStretch(1, 2)
        self.updatecontentMargins()

    def updatecontentMargins(self):
        left = 0
        right = 0
        if self._inCircle is None:
            left = 30
        if self._outCircle is None:
            right = 30
        self.layout().setContentsMargins(left, 0, right, 0)


    def labelItem(self):
        return self._labelItem


    def setLabelItem(self, labelItem):
        self._labelItemHolder.setItem(labelItem)
        self._labelItem = labelItem


    # ===================
    # Connection Methods
    # ===================
    def connectionPointType(self):
        return self._connectionPointType

    # def paint(self, painter, option, widget):
    #     super(BasePort, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0)))
    #     painter.drawRect(self.windowFrameRect())


class InputPort(BasePort):

    def __init__(self, parent, graph, name, color, dataType):
        super(InputPort, self).__init__(parent, graph, name, color, dataType, 'In')

        self.setInCircle(PortCircle(self, graph, -2, color, 'In'))
        self.setLabelItem(PortLabel(self, name, -10, self._labelColor, self._labelHighlightColor))



class OutputPort(BasePort):

    def __init__(self, parent, graph, name, color, dataType):
        super(OutputPort, self).__init__(parent, graph, name, color, dataType, 'Out')

        self.setLabelItem(PortLabel(self, self._name, 10, self._labelColor, self._labelHighlightColor))
        self.setOutCircle(PortCircle(self, graph, 2, color, 'Out'))



class IOPort(BasePort):

    def __init__(self, parent, graph, name, color, dataType):
        super(IOPort, self).__init__(parent, graph, name, color, dataType, 'IO')

        self.setInCircle(PortCircle(self, graph, -2, color, 'In'))
        self.setLabelItem(PortLabel(self, self._name, 0, self._labelColor, self._labelHighlightColor))
        self.setOutCircle(PortCircle(self, graph, 2, color, 'Out'))


