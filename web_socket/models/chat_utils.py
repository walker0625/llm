from openai import OpenAI 
import json 

# STEP1. 환경변수 불러오기
from dotenv import load_dotenv 
load_dotenv()

# STEP2. OpenAI 객체 생성
client = OpenAI()

# STEP3. 시스템 프롬프트 만들기
system_prompt = """
너는 실시간 응답에 능통한 번역가야
"""

# STEP4. 채팅하는 함수 만들기
def mychat(input_text):
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": input_text}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages,
        stream=True # 응답을 한번에 오는게 아니라 나오는대로(chunk) 응답
    )
    
    return response

def mystt(audio_path):
    
    # 오디오를 텍스트로 변환
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=file
        )

    return transcription.text

if __name__ == "__main__":
    
    response = mychat("안녕?")
    
    for chunk in response:
        token = chunk.choices[0].delta.content
        if token is None:
            break
        
        print(token, end="")