import websockets
import asyncio
import json

# 클라이언트에게 공유할 end point
WEBSOCKET_URL = 'ws://localhost:8000/ws/streaming'

async def send_message(question):
    
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        
        json_data = json.dumps(
            {'question': question}, 
            ensure_ascii=False
        )
        
        await websocket.send(json_data)
        
        while True:
            token = await websocket.recv()
        
            if token == '[END]':
                break
            
            yield token
            
async def main():
    
    question = '안녕하세요라는 말을 번역해줘'
    
    async for token in send_message(question):
        print(token, end='', flush=True)
        
asyncio.run(main())
    