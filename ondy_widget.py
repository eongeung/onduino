import math
import random
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

class OndyWidget(QLabel):
    def __init__(self, parent, image_path, x, y):
        super().__init__(parent)
        self.parent = parent
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.resize(100, 100)
        self.move(x, y)
        self.show()

        speed = random.uniform(1.5, 4.5)
        angle = random.uniform(0, 360)
        radian = angle * math.pi / 180
        self.dx = speed * math.cos(radian)
        self.dy = speed * math.sin(radian)

    def move_step(self, max_width, max_height):
        mouse_pos = QCursor.pos()
        parent_mouse_pos = self.parent.mapFromGlobal(mouse_pos)

        cx = self.x() + self.width() / 2
        cy = self.y() + self.height() / 2

        dx = parent_mouse_pos.x() - cx
        dy = parent_mouse_pos.y() - cy

        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist

        speed = min(max(dist / 20, 3), 10)
        self.dx = dx * speed
        self.dy = dy * speed

        for other in self.parent.ondys:
            if other is self:
                continue
            ox = other.x() + other.width() / 2
            oy = other.y() + other.height() / 2
            d = math.hypot(ox - cx, oy - cy)
            if d < 110 and d > 0:
                repel_strength = (110 - d) / 110
                rx = (cx - ox) / d
                ry = (cy - oy) / d
                self.dx += rx * repel_strength * 2
                self.dy += ry * repel_strength * 2

        new_x = self.x() + self.dx
        new_y = self.y() + self.dy

        if new_x < 0 or new_x + self.width() > max_width:
            self.dx *= -1
        if new_y < 0 or new_y + self.height() > max_height:
            self.dy *= -1

        self.move(int(self.x() + self.dx), int(self.y() + self.dy))

    def mouseDoubleClickEvent(self, event):
        self.deleteLater()
