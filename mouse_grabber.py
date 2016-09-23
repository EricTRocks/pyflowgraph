
#
# Copyright 2015 Horde Software Inc.
#

from PySide import QtGui, QtCore
from port import PortCircle, PortLabel
from connection import Connection

class MouseGrabber(PortCircle):
    """docstring for MouseGrabber"""

    def __init__(self, graph, pos, otherPortCircle, connectionPointType):
        super(MouseGrabber, self).__init__(None, graph, 0, otherPortCircle.getPort().getColor(), connectionPointType)

        self._ellipseItem.setPos(0, 0)
        self._ellipseItem.setStartAngle(0)
        self._ellipseItem.setSpanAngle(360 * 16)

        self.__otherPortItem = otherPortCircle

        self._graph.scene().addItem(self)


        self.setZValue(-1)
        self.setTransform(QtGui.QTransform.fromTranslate(pos.x(), pos.y()), False)
        self.grabMouse()

        import connection
        if self.connectionPointType() == 'Out':
            self.__connection = connection.Connection(self._graph, self, otherPortCircle)
        elif self.connectionPointType() == 'In':
            self.__connection = connection.Connection(self._graph, otherPortCircle, self)
        # Do not emit a notification for this temporary connection.
        self._graph.addConnection(self.__connection, emitSignal=False)
        self.__mouseOverPortCircle = None
        self._graph.emitBeginConnectionManipulationSignal()


    def getColor(self):
        return self.__otherPortItem.getPort().getColor()


    def mouseMoveEvent(self, event):
        scenePos = self.mapToScene(event.pos())

        for connection in self.getConnections():
            connection.prepareGeometryChange()

        self.setTransform(QtGui.QTransform.fromTranslate(scenePos.x(), scenePos.y()), False)

        collidingItems = self.collidingItems(QtCore.Qt.IntersectsItemBoundingRect)
        collidingPortItems = filter(lambda item: isinstance(item, (PortCircle, PortLabel)), collidingItems)

        def canConnect(item):
            if isinstance(item, PortCircle):
                mouseOverPortCircle = item
            else:
                if self.connectionPointType() == 'In':
                    mouseOverPortCircle = item.getPort().inCircle()
                else:
                    mouseOverPortCircle = item.getPort().outCircle()

                if mouseOverPortCircle == None:
                    return False

            return mouseOverPortCircle.canConnectTo(self.__otherPortItem)


        collidingPortItems = filter(lambda port: canConnect(port), collidingPortItems)
        if len(collidingPortItems) > 0:

            if isinstance(collidingPortItems[0], PortCircle):
                self.setMouseOverPortCircle(collidingPortItems[0])
            else:
                if self.connectionPointType() == 'In':
                    self.setMouseOverPortCircle(collidingPortItems[0].getPort().inCircle())
                else:
                    self.setMouseOverPortCircle(collidingPortItems[0].getPort().outCircle())

        elif self.__mouseOverPortCircle != None:
            self.setMouseOverPortCircle(None)


    def mouseReleaseEvent(self, event):

        # Destroy the temporary connection.
        self._graph.removeConnection(self.__connection, emitSignal=False)
        self.__connection = None

        if self.__mouseOverPortCircle is not None:
            try:
                if self.connectionPointType() == 'In':
                    sourcePortCircle = self.__otherPortItem
                    targetPortCircle = self.__mouseOverPortCircle
                elif self.connectionPointType() == 'Out':
                    sourcePortCircle = self.__mouseOverPortCircle
                    targetPortCircle = self.__otherPortItem

                from connection import Connection
                connection = Connection(self._graph, sourcePortCircle, targetPortCircle)
                self._graph.addConnection(connection)
                self._graph.emitEndConnectionManipulationSignal()

            except Exception as e:
                print "Exception in MouseGrabber.mouseReleaseEvent: " + str(e)

            self.setMouseOverPortCircle(None)

        self.destroy()


    def setMouseOverPortCircle(self, portCircle):

        if self.__mouseOverPortCircle != portCircle:
            if self.__mouseOverPortCircle != None:
                self.__mouseOverPortCircle.unhighlight()
                self.__mouseOverPortCircle.getPort().labelItem().unhighlight()

            self.__mouseOverPortCircle = portCircle

            if self.__mouseOverPortCircle != None:
                self.__mouseOverPortCircle.highlight()
                self.__mouseOverPortCircle.getPort().labelItem().highlight()

    # def paint(self, painter, option, widget):
    #     super(MouseGrabber, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(self.getColor()))
    #     painter.drawRect(self.windowFrameRect())

    def destroy(self):
        self.ungrabMouse()
        scene = self.scene()
        if self.__connection is not None:
            self._graph.removeConnection(self.__connection, emitSignal=False)
        # Destroy the grabber.
        scene.removeItem(self)
