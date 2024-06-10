import json
import os
import streamlit as st
from streamlit_lottie import st_lottie

# 페이지 설정
st.set_page_config(
    page_title="project",
    page_icon="✨"
)
st.title("🦜우리들의 프로젝트🦜")

# 팀 프로젝트 정보
with st.expander("인공지능 서비스 개발 기말 팀원"):
    st.write("""
    - 김나연 202284046
    - 박소윤 202284050
    - 박채현 202284054
    """)

# 열(column) 생성
col1, col2 = st.columns(2)

# col1에 문장 추가
with col1:
    st.write("""
    많은 사람들이 적성검사, 핵심 역량 검사, 성격 5요인 검사, MBTI 검사 등 자신의 성향에 대한 검사를 하며 진로 찾기 위해 많은 노력을 한다.

    그러나 종합적으로 잘 맞는 진로를 찾기엔 쉽지 않다.

    우리는 이 프로젝트를 통해 방황하는 이들에게 계열 각각의 정보와 적성에 맞는 진로 상담해주는 서비스를 제공하고자 한다.

    이 챗봇은 LLM을 사용한 AI 서비스이며, 'AI-Hub'에 올라와있는 "인공지능 기반 학생 진로탐색을 위한 상담 데이터 구축" 데이터를 사용한 RAG 기반의 챗봇이다.

    또한 이목을 집중시키기 위해 인터넷 밈을 접목시켰다.
    """)

# Lottie 파일을 로드하는 함수
def load_lottiefile(filepath: str):
    # 디버깅을 위한 파일 경로 및 현재 작업 디렉토리 출력
    print("Lottie 파일 경로:", filepath)
    print("현재 작업 디렉토리:", os.getcwd())
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"경로에 파일이 존재하지 않습니다: {filepath}")
    
    with open(filepath, "r") as f:
        return json.load(f)

# Lottie 파일 경로 정의 (상위 디렉토리의 images 폴더에 있는 경우)
lottie_file_path = os.path.join(os.path.dirname(__file__), "../images", "chat.json")

# Lottie 파일 로드
try:
    lottie_chat = load_lottiefile(lottie_file_path)
except FileNotFoundError as e:
    st.error(f"오류: {e}")
    lottie_chat = None

# Lottie 애니메이션을 성공적으로 로드한 경우 표시
if lottie_chat:
    with col2:
        st_lottie(
            lottie_chat,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=None,
            width=None,
            key=None,
        )
