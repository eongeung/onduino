import os
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from ondy_widget import OndyWidget

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, "ondyicon")

class TransparentOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setFocusPolicy(Qt.StrongFocus)

        self.ondys = []
        self.icon_paths = [os.path.join(ICON_DIR, f"cat{str(i).zfill(2)}.png") for i in range(1, 10)]
        random.shuffle(self.icon_paths)
        self.icon_index = 0

        self.ondy_count = 0
        self.max_ondy = 8
        self.is_bad_state = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ondys)
        self.timer.start(30)

        self.bad_timer = QTimer()
        self.bad_timer.timeout.connect(self.add_ondy)
        self.bad_timer.setInterval(1500)

        self.show()

    def add_ondy(self):
        if self.ondy_count >= self.max_ondy:
            self.bad_timer.stop()
            return

        width, height = 100, 100
        max_attempts = 100

        for _ in range(max_attempts):
            x = random.randint(0, self.width() - width)
            y = random.randint(0, self.height() - height)

            overlap = False
            for other in self.ondys:
                if (x < other.x() + other.width() and x + width > other.x() and
                    y < other.y() + other.height() and y + height > other.y()):
                    overlap = True
                    break

            if not overlap:
                image_path = self.icon_paths[self.icon_index % len(self.icon_paths)]
                self.icon_index += 1
                ondy = OndyWidget(self, image_path, x, y)
                self.ondys.append(ondy)
                self.ondy_count += 1
                return

        print("겹치지 않는 위치 찾기 실패")

    def clear_ondys(self):
        for ondy in self.ondys:
            ondy.fade_out_and_delete()  # 부드럽게 사라지도록 처리
        self.ondys.clear()
        self.ondy_count = 0

    def update_ondys(self):
        for ondy in self.ondys:
            ondy.move_step(self.width(), self.height())

    def fade_out_and_hide(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(1000)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.finished.connect(self.hide)
        animation.start()
        self._fade_animation = animation  # prevent garbage collection

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()
            QApplication.quit()
            sys.exit(0)
