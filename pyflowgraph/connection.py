
#
# Copyright 2015 Horde Software Inc.
#

from qtpy import QtGui, QtWidgets, QtCore


class Connection(QtWidgets.QGraphicsPathItem):
    __defaultPen = QtGui.QPen(QtGui.QColor(168, 134, 3), 1.5)

    def __init__(self, graph, srcPortCircle, dstPortCircle):
        super(Connection, self).__init__()

        self.__graph = graph
        self.__srcPortCircle = srcPortCircle
        self.__dstPortCircle = dstPortCircle
        penStyle = QtCore.Qt.DashLine

        self.__connectionColor = QtGui.QColor(0, 0, 0)
        self.__connectionColor.setRgbF(*self.__srcPortCircle.getColor().getRgbF())
        self.__connectionColor.setAlpha(125)

        self.__defaultPen = QtGui.QPen(self.__connectionColor, 1.5, style=penStyle)
        self.__defaultPen.setDashPattern([1, 2, 2, 1])

        self.__connectionHoverColor = QtGui.QColor(0, 0, 0)
        self.__connectionHoverColor.setRgbF(*self.__srcPortCircle.getColor().getRgbF())
        self.__connectionHoverColor.setAlpha(255)

        self.__hoverPen = QtGui.QPen(self.__connectionHoverColor, 1.5, style=penStyle)
        self.__hoverPen.setDashPattern([1, 2, 2, 1])

        self.setPen(self.__defaultPen)
        self.setZValue(-1)

        self.setAcceptHoverEvents(True)
        self.connect()


    def setPenStyle(self, penStyle):
        self.__defaultPen.setStyle(penStyle)
        self.__hoverPen.setStyle(penStyle)
        self.setPen(self.__defaultPen) # Force a redraw


    def setPenWidth(self, width):
        self.__defaultPen.setWidthF(width)
        self.__hoverPen.setWidthF(width)
        self.setPen(self.__defaultPen) # Force a redraw


    def getSrcPortCircle(self):
        return self.__srcPortCircle


    def getDstPortCircle(self):
        return self.__dstPortCircle


    def getSrcPort(self):
        return self.__srcPortCircle.getPort()


    def getDstPort(self):
        return self.__dstPortCircle.getPort()


    def boundingRect(self):
        srcPoint = self.mapFromScene(self.__srcPortCircle.centerInSceneCoords())
        dstPoint = self.mapFromScene(self.__dstPortCircle.centerInSceneCoords())
        penWidth = self.__defaultPen.width()

        return QtCore.QRectF(
            min(srcPoint.x(), dstPoint.x()),
            min(srcPoint.y(), dstPoint.y()),
            abs(dstPoint.x() - srcPoint.x()),
            abs(dstPoint.y() - srcPoint.y()),
            ).adjusted(-penWidth/2, -penWidth/2, +penWidth/2, +penWidth/2)


    def paint(self, painter, option, widget):
        srcPoint = self.mapFromScene(self.__srcPortCircle.centerInSceneCoords())
        dstPoint = self.mapFromScene(self.__dstPortCircle.centerInSceneCoords())

        dist_between = dstPoint - srcPoint

        self.__path = QtGui.QPainterPath()
        self.__path.moveTo(srcPoint)
        self.__path.cubicTo(
            srcPoint + QtCore.QPointF(dist_between.x() * 0.4, 0),
            dstPoint - QtCore.QPointF(dist_between.x() * 0.4, 0),
            dstPoint
            )
        self.setPath(self.__path)
        super(Connection, self).paint(painter, option, widget)


    def hoverEnterEvent(self, event):
        self.setPen(self.__hoverPen)
        super(Connection, self).hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        self.setPen(self.__defaultPen)
        super(Connection, self).hoverLeaveEvent(event)


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.__dragging = True
            self._lastDragPoint = self.mapToScene(event.pos())
            event.accept()
        else:
            super(Connection, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self.__dragging:
            pos = self.mapToScene(event.pos())
            delta = pos - self._lastDragPoint
            if delta.x() != 0:

                self.__graph.removeConnection(self)

                from . import mouse_grabber
                if delta.x() < 0:
                    mouse_grabber.MouseGrabber(self.__graph, pos, self.__srcPortCircle, 'In')
                else:
                    mouse_grabber.MouseGrabber(self.__graph, pos, self.__dstPortCircle, 'Out')

        else:
            super(Connection, self).mouseMoveEvent(event)


    def disconnect(self):
        self.__srcPortCircle.removeConnection(self)
        self.__dstPortCircle.removeConnection(self)


    def connect(self):
        self.__srcPortCircle.addConnection(self)
        self.__dstPortCircle.addConnection(self)
