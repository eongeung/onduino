import cv2
import math
import time
import mediapipe as mp
from transparent_overlay import TransparentOverlay

def run_pose_landmark(app):
    print("Pose Landmark 시작")

    overlay = TransparentOverlay()
    overlay.hide()
    overlay_launched = False
    bad_start_time = None
    good_start_time = None  # 오타 수정: gootd → good

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            image = frame
            results = pose.process(image)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing_styles.get_default_pose_landmarks_style()
                )

                image_height, image_width, _ = image.shape
                landmarks = results.pose_landmarks.landmark

                nose = landmarks[0]
                left_shoulder = landmarks[11]
                right_shoulder = landmarks[12]

                shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
                shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
                neck_forward_distance = nose.x - shoulder_center_x

                dx = nose.x - shoulder_center_x
                dy = shoulder_center_y - nose.y
                angle_rad = math.atan2(dy, dx)
                angle_deg = abs(math.degrees(angle_rad))

                cv2.putText(
                    image,
                    f"Neck Angle: {angle_deg:.1f} deg",
                    (30, image_height - 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 255),
                    2
                )

                if -0.20 <= neck_forward_distance <= 0.01:
                    # GOOD 자세
                    cv2.putText(
                        image,
                        "GOOD!",
                        (30, image_height - 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 255, 0),
                        3
                    )
                    if good_start_time is None:
                        good_start_time = time.time()
                    elif time.time() - good_start_time >= 3:
                        if overlay.isVisible():
                            overlay.clear_ondys()
                            overlay.bad_timer.stop()
                            overlay.hide()
                            overlay_launched = False
                    bad_start_time = None  # BAD 초기화

                else:
                    # BAD 자세
                    cv2.putText(
                        image,
                        "BAD!",
                        (30, image_height - 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 0, 255),
                        3
                    )
                    if bad_start_time is None:
                        bad_start_time = time.time()
                    elif time.time() - bad_start_time >= 5:
                        if not overlay_launched:
                            overlay.show()
                            overlay.bad_timer.start()
                            overlay_launched = True
                    good_start_time = None  # GOOD 초기화

            cv2.imshow('Pose Landmark', image)

            key = cv2.waitKey(5) & 0xFF
            if key == 27:
                print("ESC 눌림 - 종료합니다.")
                break

            # Qt 이벤트 생략
            # if app is not None:
            #     app.processEvents()

    cap.release()
    cv2.destroyAllWindows()
