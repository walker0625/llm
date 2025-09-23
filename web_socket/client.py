import websockets
import asyncio
import json
import cv2

# 1. text <-> text / gpt 

#WEBSOCKET_URL = 'ws://localhost:8000/ws/streaming'
#
#async def send_message(question):
#    
#    async with websockets.connect(WEBSOCKET_URL) as websocket:
#        
#        json_data = json.dumps(
#            {'question': question}, 
#            ensure_ascii=False
#        )
#        
#        await websocket.send(json_data)
#        
#        while True:
#            token = await websocket.recv()
#        
#            if token == '[END]':
#                break
#            
#            yield token
#            
#async def main():
#    
#    question = '안녕하세요라는 말을 번역해줘'
#    
#    async for token in send_message(question):
#        print(token, end='', flush=True)
#        
#asyncio.run(main())


# 2. image <-> text / mediapipe

#SERVER_URL = "ws://127.0.0.1:8000/ws/image"
#IMAGE_PATH = "./resources/hand_image.jpg"
#
#async def send_image_once():
#    
#    # 이미지를 JPEG 바이트로 준비
#    img = cv2.imread(IMAGE_PATH)
#    
#    if img is None:
#        raise FileNotFoundError(f"이미지를 읽지 못했어요: {IMAGE_PATH}")
#    
#    ok, buf = cv2.imencode(".jpg", img)  # JPEG로 인코딩
#    
#    if not ok:
#        raise RuntimeError("이미지 JPEG 인코딩 실패")
#    data = buf.tobytes()
#    
#    async with websockets.connect(SERVER_URL, max_size=None) as ws:
#        
#        # 바이너리 메시지로 한 방에 전송
#        await ws.send(data)
#        
#        # 서버가 보내는 JSON 응답 받기
#        reply = await ws.recv()  # 텍스트 메시지
#        print("서버 응답:", reply)
#        
#if __name__ == "__main__":
#    asyncio.run(send_image_once())

# 3. file(.wav) <-> text / stt

SERVER_URL = "ws://127.0.0.1:8000/ws/audio"
AUDIO_PATH = "./resources/input.wav"

async def send_audio_once():
    
    # WAV 파일 로드
    with open(AUDIO_PATH, "rb") as f:
        data = f.read()

    async with websockets.connect(SERVER_URL, max_size=None) as ws:
        
        # 1) WAV 데이터 전송
        await ws.send(data)

        # 2) 서버 응답 받기
        reply = await ws.recv()
        print("서버 응답:", reply)

if __name__ == "__main__":
    asyncio.run(send_audio_once())