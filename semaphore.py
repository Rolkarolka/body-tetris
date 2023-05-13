import mediapipe as mp
import cv2
from enum import Enum
from math import atan2, degrees


class Move(Enum):
    LEFT = 0
    RIGHT = 1
    JUMP = 2


class PoseExtractor:
    DEFAULT_LANDMARKS_STYLE = mp.solutions.drawing_styles.get_default_pose_landmarks_style()
    VISIBILITY_THRESHOLD = .8
    JUMP_THRESHOLD = .0001
    FRAME_HISTORY = 8
    HALF_HISTORY = int(FRAME_HISTORY / 2)
    EMPTY_FRAME_STRUCT = {
        'hipL_y': 0,
        'hipR_y': 0,
        'hips_dy': 0,
        'dxL_thrust_hipL': 0,
        'dxL_thrust_hipR': 0,
        'dxR_thrust_hipL': 0,
        'dxR_thrust_hipR': 0,
        'signed': False,
    }

    def __init__(self):
        self.last_frames = PoseExtractor.FRAME_HISTORY * [PoseExtractor.EMPTY_FRAME_STRUCT.copy()]
        self.draw_landmarks = True
        self.is_right_hand_raised = False
        self.is_left_hand_raised = False
        self.cap = cv2.VideoCapture(0)
        self.pose_model = mp.solutions.pose.Pose()

    @staticmethod
    def is_missing(part):
        return any(joint['visibility'] < PoseExtractor.VISIBILITY_THRESHOLD for joint in part)

    def is_arm_lifted(self, arm, move):
        if self.is_missing(arm):
            return False
        dy = arm[1]['y'] - arm[0]['y']
        dx = arm[1]['x'] - arm[0]['x']
        angle = degrees(atan2(dy, dx))
        if move == Move.RIGHT:
            return -50 < angle < 50
        elif move == Move.LEFT:
            return (130 < angle < 180) or (-180 < angle < -130)
        return False

    def is_jumping(self, hipL, hipR):
        if self.is_missing([hipL, hipR]):
            return False

        self.last_frames[-1]['hipL_y'] = hipL['y']
        self.last_frames[-1]['hipR_y'] = hipR['y']

        if (hipL['y'] > self.last_frames[-2]['hipL_y'] + PoseExtractor.JUMP_THRESHOLD) and (
                hipR['y'] > self.last_frames[-2]['hipR_y'] + PoseExtractor.JUMP_THRESHOLD):
            self.last_frames[-1]['hips_dy'] = 1  # rising
        elif (hipL['y'] < self.last_frames[-2]['hipL_y'] - PoseExtractor.JUMP_THRESHOLD) and (
                hipR['y'] < self.last_frames[-2]['hipR_y'] - PoseExtractor.JUMP_THRESHOLD):
            self.last_frames[-1]['hips_dy'] = -1  # falling
        else:
            self.last_frames[-1]['hips_dy'] = 0  # not significant dy

        # consistently rising first half, lowering second half
        jump_up = all(frame['hips_dy'] == 1 for frame in self.last_frames[:PoseExtractor.HALF_HISTORY])
        get_down = all(frame['hips_dy'] == -1 for frame in self.last_frames[PoseExtractor.HALF_HISTORY:])

        return jump_up and get_down

    def get_pose(self):
        if self.cap.isOpened():
            success, image = self.cap.read()
            if not success: return
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pose_results = self.pose_model.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if self.draw_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image,
                    pose_results.pose_landmarks,
                    mp.solutions.pose.POSE_CONNECTIONS,
                    PoseExtractor.DEFAULT_LANDMARKS_STYLE)
                cv2.imshow('Youtine', image)
            # print([id(x) for x in self.last_frames])
            if pose_results.pose_landmarks:
                self.last_frames = self.last_frames[1:] + [PoseExtractor.EMPTY_FRAME_STRUCT.copy()]
                body = []
                for point in pose_results.pose_landmarks.landmark:
                    body.append({
                        'x': 1 - point.x,
                        'y': 1 - point.y,
                        'visibility': point.visibility
                    })

                shoulder_l, elbow_l, wrist_l = body[11], body[13], body[15]
                arm_l = (shoulder_l, elbow_l, wrist_l)
                if self.is_arm_lifted(arm_l, Move.LEFT):
                    if self.is_left_hand_raised is False:
                        self.is_left_hand_raised = True
                        return Move.LEFT
                elif self.is_left_hand_raised is True:
                    self.is_left_hand_raised = False

                shoulder_r, elbow_r, wrist_r = body[12], body[14], body[16]
                arm_r = (shoulder_r, elbow_r, wrist_r)
                if self.is_arm_lifted(arm_r, Move.RIGHT):
                    if self.is_right_hand_raised is False:
                        self.is_right_hand_raised = True
                        return Move.RIGHT
                elif self.is_right_hand_raised is True:
                    self.is_right_hand_raised = False

                hip_l, hip_r = body[23], body[24]
                if self.is_jumping(hip_l, hip_r):
                    return Move.JUMP

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def is_end():
        return cv2.waitKey(5) & 0xFF == 27

if __name__ == '__main__':
    poseExtractor = PoseExtractor()
    while poseExtractor.is_end() is False:
        m = poseExtractor.get_pose()
        if m is not None:
            print(m)