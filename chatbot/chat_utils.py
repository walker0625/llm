from openai import OpenAI
import json
from  dotenv import load_dotenv

load_dotenv()

client = OpenAI()

system_prompt = """
너는 경험이 풍부한 시니어 개발자야
[대화 히스토리]는 사용자가 너가 나눈 대화야
이 대화를 참고해서 사용자 질문에 대답해줘

[대화 히스토리]
"""

def mychat(input_text, history):
    
    history_str = json.dumps(
        history, 
        ensure_ascii=False # 한글을 ascii가 아니라 문자로 저장
    )
    
    print(history_str)
    print('-'*100)
    
    messages = [
        {"role": "system", "content": system_prompt + history_str},
        {"role": "user", "content": input_text},
    ]
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages,
    )
    
    return response.choices[0].message.content