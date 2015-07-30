
#
# Copyright 2015 Horde Software Inc.
#

import json
from PySide import QtGui, QtCore


class PortLabel(QtGui.QGraphicsWidget):
    __font = QtGui.QFont('Decorative', 12)

    def __init__(self, port, text, hOffset, color, highlightColor):
        super(PortLabel, self).__init__(port)
        self.__port = port
        self.__text = text
        self.__textItem = QtGui.QGraphicsTextItem(text, self)
        self._labelColor = color
        self.__highlightColor = highlightColor
        self.__textItem.setDefaultTextColor(self._labelColor)
        self.__textItem.setFont(self.__font)
        self.__textItem.translate(0, self.__font.pointSizeF() * -0.5)
        option = self.__textItem.document().defaultTextOption()
        option.setWrapMode(QtGui.QTextOption.NoWrap)
        self.__textItem.document().setDefaultTextOption(option)
        self.__textItem.adjustSize()

        self.translate(hOffset, 0)
        self.adjustSize()

        self.setAcceptHoverEvents(True)
        self.setPreferredSize(self.textSize())
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.setWindowFrameMargins(0, 0, 0, 0)

        self.__mousDownPos = None

    def text(self):
        return self.__text


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
        self.unhighlight()

        if self.__port.inCircle() is not None and self.__port.outCircle() is not None:
            self.__mousDownPos = self.mapToScene(event.pos())

        elif self.__port.inCircle() is not None:
            self.__port.inCircle().mousePressEvent(event)

        elif self.__port.outCircle() is not None:
            self.__port.outCircle().mousePressEvent(event)


    def mouseMoveEvent(self, event):
        scenePos = self.mapToScene(event.pos())

        # When clicking on an UI port label, it is ambigous which connection point should be activated.
        # We let the user drag the mous in either direction to select the conneciton point to activate.
        delta = scenePos - self.__mousDownPos
        if delta.x() < 0:
            self.__port.inCircle().mousePressEvent(event)
        else:
            self.__port.outCircle().mousePressEvent(event)

    # def paint(self, painter, option, widget):
    #     super(PortLabel, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 255)))
    #     painter.drawRect(self.windowFrameRect())


class PortCircle(QtGui.QGraphicsWidget):
    __radius = 4.5
    __diameter = 2 * __radius

    def __init__(self, port, graph, hOffset, color, connectionPointType):
        super(PortCircle, self).__init__(port)

        self.__port = port
        self._graph = graph
        self._connectionPointType = connectionPointType
        self.__connections = set()
        self._supportsOnlySingleConnections = connectionPointType == 'In'

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        size = QtCore.QSizeF(self.__diameter, self.__diameter)
        self.setPreferredSize(size)
        self.setWindowFrameMargins(0, 0, 0, 0)

        self.translate(self.__radius * hOffset, 0)

        self.__defaultPen = QtGui.QPen(QtGui.QColor(25, 25, 25), 1.0)
        self.__hoverPen = QtGui.QPen(QtGui.QColor(255, 255, 100), 1.5)

        self._ellipseItem = QtGui.QGraphicsEllipseItem(self)
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

        from mouse_grabber import MouseGrabber
        if self.isInConnectionPoint():
            MouseGrabber(self._graph, scenePos, self, 'Out')
        elif self.isOutConnectionPoint():
            MouseGrabber(self._graph, scenePos, self, 'In')


    # def paint(self, painter, option, widget):
    #     super(PortCircle, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0)))
    #     painter.drawRect(self.windowFrameRect())


class BasePort(QtGui.QGraphicsWidget):

    _labelColor = QtGui.QColor(25, 25, 25)
    _labelHighlightColor = QtGui.QColor(225, 225, 225, 255)

    def __init__(self, parent, graph, name, color, dataType, connectionPointType):
        super(BasePort, self).__init__(parent)

        self._node = parent
        self._graph = graph
        self._name = name
        self._dataType = dataType
        self._connectionPointType = connectionPointType

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))

        layout = QtGui.QGraphicsLinearLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        self._color = color

        self._inCircle = None
        self._outCircle = None
        self._labelItem = None

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

    def outCircle(self):
        return self._outCircle

    def labelItem(self):
        return self._labelItem

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
    """docstring for InputPort"""

    def __init__(self, parent, graph, name, color, dataType):
        super(InputPort, self).__init__(parent, graph, name, color, dataType, 'In')

        labelHOffset = -10
        circleHOffset = -2

        self._inCircle = PortCircle(self, graph, circleHOffset, color, 'In')
        self._labelItem = PortLabel(self, name, labelHOffset, self._labelColor, self._labelHighlightColor)

        self.layout().addItem(self._inCircle)
        self.layout().setAlignment(self._inCircle, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout().setContentsMargins(0, 0, 30, 0)
        self.layout().addItem(self._labelItem)
        self.layout().setAlignment(self._labelItem, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout().addStretch(2)

        self.__connection = None


class OutputPort(BasePort):
    """docstring for OutputPort"""

    def __init__(self, parent, graph, name, color, dataType):
        super(OutputPort, self).__init__(parent, graph, name, color, dataType, 'Out')

        labelHOffset = 10
        circleHOffset = 2

        self._labelItem = PortLabel(self, self._name, labelHOffset, self._labelColor, self._labelHighlightColor)
        self._outCircle = PortCircle(self, graph, circleHOffset, color, 'Out')

        self.layout().addStretch(2)
        self.layout().setContentsMargins(30, 0, 0, 0)
        self.layout().addItem(self._labelItem)
        self.layout().setAlignment(self._labelItem, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout().addItem(self._outCircle)
        self.layout().setAlignment(self._outCircle, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


class IOPort(BasePort):
    """docstring for OutputPort"""

    def __init__(self, parent, graph, name, color, dataType):
        super(IOPort, self).__init__(parent, graph, name, color, dataType, 'IO')

        labelHOffset = 0
        circleHOffset = -2

        self._inCircle = PortCircle(self, graph, circleHOffset, color, 'In')

        self._labelItem = PortLabel(self, name, labelHOffset, self._labelColor, self._labelHighlightColor)

        circleHOffset = 2
        self._outCircle = PortCircle(self, graph, circleHOffset, color, 'Out')

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addItem(self._inCircle)
        self.layout().setAlignment(self._inCircle, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout().addStretch(1)
        self.layout().addItem(self._labelItem)
        self.layout().setAlignment(self._labelItem, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout().addStretch(1)
        self.layout().addItem(self._outCircle)
        self.layout().setAlignment(self._outCircle, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

