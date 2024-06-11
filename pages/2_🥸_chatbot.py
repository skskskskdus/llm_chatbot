import streamlit as st
import zipfile
import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document
from streamlit_extras.let_it_rain import rain
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser

import time
from glob import glob
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

# OpenAI API 키 설정
OPENAI_API_KEY = "YOUR_API_KEY" # 실제 API 키를 설정하세요
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 페이지 설정
st.set_page_config(page_title="chatbot", page_icon="🥸")
st.title('🐈‍⬛나만의 집사님🐈‍⬛')

# 측면 바에 비디오 추가
st.sidebar.video("https://youtu.be/FoO7Pmx0bE4")

# 기본 모델 설정
if "model" not in st.session_state:
    st.session_state["model"] = "gpt-3.5-turbo"

# 채팅 기록 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ZIP 파일 해제 및 JSON 데이터 읽기
zip_file_path = os.path.join("ai_data", "TL_02. 추천직업 카테고리_01. 기술계열.zip")
extract_dir = os.path.join("data", "data")
json_file_path = os.path.join(extract_dir, "전문가_라벨링_데이터_기술계열.json")

if "retriever" not in st.session_state:

    loader=DirectoryLoader("data",glob="*.json",loader_cls=TextLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    from langchain_openai import OpenAIEmbeddings
    embeddings_model=OpenAIEmbeddings()
    embedding = embeddings_model
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embedding)
    st.session_state.retriever = vectordb.as_retriever()

# 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_template(
        """
    너는 진로 상담을 위한 챗봇이야. 
    기술 계열 상담 데이터를 사용해서 사용자의 질문에 답변할 수 있도록 학습되었어. 
    상담 데이터 외의 질문은 OpenAI의 모델을 사용하여 답변할 수 있도록 되어 있어.

    Answer the question based only on the following context:
    {context}

    Question: {question}
    """
)

def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)

llm = ChatOpenAI(api_key=OPENAI_API_KEY,model_name="gpt-3.5-turbo", temperature=0)

# RAG Chain 연결
rag_chain = (
    {'context':  st.session_state.retriever | format_docs, 'question': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 세션 상태 초기화
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# 응답 생성 함수 수정
def generate_response(input_text):
    input_string = str(input_text)
    # 이전 대화를 포함하는 BaseMessages 목록 생성
    #base_messages = create_base_messages(st.session_state.conversation)
    # RAG 체인에 전달하여 응답 생성
    response = rag_chain
    return response


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



