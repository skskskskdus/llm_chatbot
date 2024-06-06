import streamlit as st
from langchain.llms import OpenAI  # 수정된 import 문
from streamlit_extras.let_it_rain import rain
import os
import zipfile
import json
import openai

# 페이지 설정
st.set_page_config(
    page_title="chatbot",  # 페이지 제목 설정
    page_icon="🥸"  # 페이지 아이콘 설정
)
st.title('🐈‍⬛나만의 집사님🐈‍⬛')  # 제목 표시

# 측면 바에 비디오 추가
st.sidebar.video("https://youtu.be/FoO7Pmx0bE4")

# OpenAI API 키 설정
os.environ["OPENAI_API_KEY"]="YOUR_OPENAI_API_KEY"

# ZIP 파일 해제 및 JSON 데이터 읽기
zip_file_path = "data/TL_02. 추천직업 카테고리_01. 기술계열.zip"  # 파일 경로 설정
extract_dir = "extracted_data"  # 압축 해제된 데이터 저장 디렉토리
json_file_path = os.path.join(extract_dir, "전문가_라벨링_데이터_기술계열.json")  # JSON 파일 경로 설정

# 파일 압축 해제
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
except PermissionError:
    st.error("권한이 없습니다. 파일 경로와 권한을 확인하세요.")
except FileNotFoundError:
    st.error("ZIP 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")

# UTF-8 인코딩으로 JSON 파일 읽기
try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        career_data = json.load(file)
except FileNotFoundError:
    st.error(f"{json_file_path}에 JSON 파일을 찾을 수 없습니다. 압축 해제 과정을 확인하세요.")
except json.JSONDecodeError:
    st.error(f"{json_file_path}의 JSON 파일을 디코딩하는 중 오류가 발생했습니다.")
except UnicodeDecodeError:
    st.error(f"{json_file_path}의 JSON 파일을 읽는 중 인코딩 오류가 발생했습니다.")

# 응답 생성 함수
def generate_response(input_text):
    llm = OpenAI(model_name='gpt-3.5-turbo', temperature=0)
    response = llm(input_text)
    # 필요한 경우 career_data를 응답에 통합할 수 있습니다.
    # 여기서는 모델의 응답만 반환합니다.
    return response

# 세션 상태 초기화
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# 질문 양식
with st.form('Question'):
    text = st.text_area('오조사마 입력:', placeholder='야레 야레 또 질문하는 거예요?')
    submitted = st.form_submit_button("질문해볼까요?")
    if submitted:
        response = generate_response(text)
        st.session_state.conversation.insert(0, {'question': text, 'response': response})

# 대화 기록 표시
for chat in st.session_state.conversation:
    st.write(f"**오조사마:** {chat['question']}")
    st.info(f"**집사:** {chat['response']}")

# 대화 저장 버튼
if st.button("대화 저장"):
    # 'conversations' 디렉토리가 있는지 확인
    if not os.path.exists('conversations'):
        os.makedirs('conversations')
    
    file_path = os.path.join('conversations', 'conversation.py')
    
    # 파일이 존재하는 경우 이전 대화 불러오기
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            exec(file.read(), globals(), locals())
    
    with open(file_path, "w", encoding='utf-8') as file:
        file.write("# 대화 기록\n")
        file.write("conversation = [\n")
        for chat in st.session_state.conversation:
            file.write(f"    {{'question': '''{chat['question']}''', 'response': '''{chat['response']}'''}},\n")
        if 'conversation' in locals():
            for chat in conversation:
                file.write(f"    {{'question': '''{chat['question']}''', 'response': '''{chat['response']}'''}},\n")
        file.write("]\n")
    st.success(f"대화가 'conversations/conversation.py' 파일에 저장되었습니다!")

# 저장된 대화 표시 버튼
if st.button("저장된 대화 표시"):
    try:
        with open(os.path.join('conversations', 'conversation.py'), "r", encoding='utf-8') as file:
            exec(file.read(), globals(), locals())
            if 'conversation' in locals():
                for chat in conversation:
                    st.write(f"**오조사마:** {chat['question']}")
                    st.info(f"**집사:** {chat['response']}")
            else:
                st.error("파일에서 저장된 대화를 찾을 수 없습니다.")
    except FileNotFoundError:
        st.error("저장된 대화 파일을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")

# 시각적 효과 함수
def rose():
    rain(
        emoji="🌹",
        font_size=54,
        falling_speed=5,
        animation_length="infinite",
    )

rose()



