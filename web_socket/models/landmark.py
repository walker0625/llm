import mediapipe as mp 
import joblib
import numpy as np
import cv2

# mediapipe의 Pose Landmark를 추출을 위한 옵션
mp_pose = mp.solutions.pose 
mp_drawing = mp.solutions.drawing_utils 

pose = mp_pose.Pose(
    static_image_mode=True, 
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# mediapipe의 Hand Landmark를 추출을 위한 옵션
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils 

hands = mp_hands.Hands(
    static_image_mode = True, 
    max_num_hands = 2,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

# 모델 불러오기 
model = joblib.load("./resources/rock_scissors_paper.pkl")
labels = ["rock", "scissors", "paper"]

def extract_pose_landmark(frame):
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 포즈 감지하기 
    results = pose.process(frame)
    
    # 추출
    landmarks = []
        
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
            
    return landmarks

def extract_hand_landmark(frame):
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 손 감지하기 
    results = hands.process(frame)
    
    # 추출
    landmarks = []
        
    # 리스트 버전
    # if results.multi_hand_landmarks:
    #     print(len(results.multi_hand_landmarks))
    #     for hand_landmark in results.multi_hand_landmarks:
    #         one_landmarks = []
    #         for landmark in hand_landmark.landmark:
    #             one_landmarks.extend([landmark.x, landmark.y, landmark.z])
    #         landmarks.append(one_landmarks)

    #         # 예측
    #         pred = model.predict(np.array([one_landmarks]))
    #         one_landmarks.append(pred[0])

    # 딕셔너리 버전
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            one_landmarks = {"landmarks": [], "pred": ""}
            for landmark in hand_landmark.landmark:
                one_landmarks["landmarks"].extend([landmark.x, landmark.y, landmark.z])
            landmarks.append(one_landmarks)

            # 예측
            pred = model.predict(np.array([one_landmarks["landmarks"]]))
            one_landmarks["pred"] = int(pred[0])
            
    return landmarks

if __name__ == "__main__":
    import cv2 
    image_path = "./resources/hand_image.jpg"
    frame = cv2.imread(image_path)
    print(extract_hand_landmark(frame))