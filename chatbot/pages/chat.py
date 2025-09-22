import streamlit as st
import chat_utils as utils # 모듈을 불러올 때 경로 기준은 실행한 python 파일(st_mian.py)의 위치

# 프로필 설정
profile = {
    "user": "chatbot/resources/user.jpeg",
    "ai": "chatbot/resources/ai.png"
}

# session state 정의
if not "messages" in st.session_state:
    st.session_state["messages"] = []

history = st.session_state["messages"]

# 챗봇 제목 
st.title("히스토리가 반영된 챗봇 만들기")

## 과거 메시지 출력 
if len(st.session_state["messages"]) > 0:
    for chat in st.session_state["messages"]:
        name = chat["role"]
        avatar = profile[name]
        st.chat_message(name=name, avatar=avatar).markdown(chat["content"])

# 사용자 입력
input_text = st.chat_input("메세지를 입력하세요...")

# 사용자 입력 이후
if input_text:
    
    st.chat_message(name="user", avatar=profile["user"]).markdown(input_text)

    with st.chat_message(name="ai", avatar=profile["ai"]):
        container = st.empty() # 빈공간
        
        with container:
            with st.spinner("답변 중..."):
                answer = utils.mychat(input_text, history)
            
            st.markdown(answer)

    # 대화 저장    
    st.session_state["messages"].extend(
        [
            {"role": "user", "content": input_text},
            {"role": "ai", "content": answer}
        ]
    )