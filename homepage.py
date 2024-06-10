"""
# 출처: 책[랭체인으로 LLM 기반의 AI 서비스 개발하기], 서지영
# 출처: https://github.com/scmpevatrons/ai-chatverse
# 출처: https://arnaudmiribel.github.io/streamlit-extras/
# 출처: https://docs.streamlit.io/develop/api-reference
# 출처: https://streamlit.io/gallery?category=llms
# 출처: https://youtu.be/YClmpnpszq8?si=efs6QVexPMjwZ97O
# 출처: https://youtu.be/TXSOitGoINE?si=eAgI9KdB5sdkJ9t3
# 출처: chat-gpt
# 출처: 뤼튼
# 출처:https://wikidocs.net/234009
# 출처:https://wikidocs.net/231431
"""
import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

#### 페이지 설정
st.set_page_config(
    page_title="homepage",
    page_icon="👋"
)
st.title("🤖서비스개발I 기말팀플🤖")

#### 사이트바 설정
st.sidebar.success("위 페이지를 선택하세요.")

#### 로티파일 넣기
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# 로티 파일 경로 설정 (윈도우 스타일)
lottie_file_path = "images\coding.json"
# 로티 파일 로드
lottie_coding = load_lottiefile(lottie_file_path)

# 로티 애니메이션 표시
st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
    height=None,
    width=None,
    key=None,
)
