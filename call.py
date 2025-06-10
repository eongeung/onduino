import sys
from PyQt5.QtWidgets import QApplication
from transparent_overlay import TransparentOverlay
import pose

if __name__ == '__main__':
    print("Ondy 시작")
    app = QApplication(sys.argv)
    overlay = TransparentOverlay()
    overlay.hide()  # 시작할 땐 숨김
    pose.run_pose_landmark(overlay)  # overlay 넘김
    sys.exit(app.exec_())  # 이벤트 루프 실행
