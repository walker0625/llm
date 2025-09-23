# uv add fastapi[all]

import os
import tempfile
import json 

import numpy as np 
import cv2

from fastapi import FastAPI, WebSocket
from models.chat_utils import mychat, mystt
from models.landmark import extract_hand_landmark

app = FastAPI()

# text <-> text / gpt
@app.websocket('/ws/streaming')
async def websocket_text(websocket: WebSocket):
    
    await websocket.accept()
    print("WebSocket 연결됨")
    
    try:
        #data = await websocket.receive_text()
        json = await websocket.receive_json()
        response = mychat(json['question'])
        
        print(response)
        
        for chunk in response:
            print(chunk)
            chunk_text = chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end='')
            
            # 마지막 응답은 None이라 클라이언트엔 보낼 필요가 없음
            if chunk_text is None:
                continue
            
            await websocket.send_text(chunk_text)
            
        # 클라이언트 측에 끝을 알리는 키워드 전송(클라이언트와 협의)
        await websocket.send_text("[END]") 
            
    except Exception as e:
        print(f'Exception: {e}')
        
    finally:
        await websocket.close()
        print('Websocket closed')
        
# image <-> text / mediapipe
@app.websocket("/ws/image")
async def websocket_image(websocket: WebSocket):
    
    await websocket.accept()
    print("WebSocket 연결됨")

    try:
        # 클라이언트 메시지 받기
        data = await websocket.receive_bytes()  
        np_data = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        print(f"클라이언트가 준 이미지: {len(data)}")

        # Mediapipe 추론
        landmarks = extract_hand_landmark(frame)
        print(f"이미지 탐지했어요: {landmarks}")
        json_data = json.dumps({"results": landmarks}, ensure_ascii=False)

        await websocket.send_text(json_data)

    except Exception as e:
        print(f"WebSocket 에러 발생: {e}")
    finally:
        await websocket.close()
        print("WebSocket 연결 종료")

# file(.wav) <-> text / stt
@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    
    await websocket.accept()
    print("WebSocket 연결됨")

    try:
        data = await websocket.receive_bytes()

        # 2) 바이너리 프레임 받아 임시 파일에 저장
        with tempfile.NamedTemporaryFile(prefix="wav_", suffix=".wav", delete=False) as tmpfile:
            tmp_path = tmpfile.name
            tmpfile.write(data)
                
        # 여기서 tmp 경로의 WAV로 STT 실행 가능
        stt_result = mystt(tmp_path)
        json_data = json.dumps({"result": stt_result}, ensure_ascii=False)

        await websocket.send_text(json_data)

    except Exception as e:
        print(f"WebSocket 에러 발생: {e}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

        await websocket.close()
        print("WebSocket 연결 종료")