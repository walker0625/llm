# uv add fastapi[all]

from fastapi import FastAPI, WebSocket
from models.chat_utils import mychat

app = FastAPI()

# text <-> text / gpt
@app.websocket('/ws/streaming')
async def websocket_text(websocket: WebSocket):
    
    await websocket.accept()
    
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

# file(.wav) <-> text / stt