import streamlit as st
import requests
import openai
from datetime import datetime
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

# OpenAI API 키 설정
openai_api_key = "your_openai_api_key"
openai.api_key = openai_api_key

# Naver API 설정
CLIENT_ID = 'kOTwXT4d09oyxlqSO_Vg'
CLIENT_SECRET = 'uKa8vmVcsI'

# Naver 백과사전 검색 API 호출 함수
def search_dream(query):
    url = f"https://openapi.naver.com/v1/search/encyc.json?query={query}"
    headers = {"X-Naver-Client-Id": CLIENT_ID, "X-Naver-Client-Secret": CLIENT_SECRET}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        st.error(f"백과사전 API 호출 중 오류가 발생했습니다: {e}")
        return None

# Naver 블로그 검색 API 호출 함수
def search_blog(keyword):
    url = f"https://openapi.naver.com/v1/search/blog.json?query={keyword}"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        st.error(f"블로그 API 호출 중 오류가 발생했습니다: {e}")
        return None

# LangChain 설정 함수: qa_chain 설정
def get_qa_chain():
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    llm = OpenAI(openai_api_key=openai_api_key)
    memory = ConversationBufferMemory()
    vectorstore = Chroma(embedding_function=embeddings)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return qa_chain

def run_ui(qa_chain, query):
    # qa_chain이 제대로 전달되지 않았을 경우 오류를 표시
    if qa_chain is None:
        st.error("qa_chain 인자가 전달되지 않았습니다.")
        return

    if query:
        # Naver API를 통한 꿈 해석
        blog_results = search_blog(query + ' 꿈 해몽')
        dream_results = search_dream(query + ' 꿈 해몽')

        if blog_results:
            st.subheader("Blog Search Results:")
            for item in blog_results:
                # 한 줄로 출력
                st.write(f"**{item['title']}**: {item['description']} [Read more]({item['link']})")
        else:
            st.write("No blog results found.")

        if dream_results:
            st.subheader("Encyclopedia Search Results:")
            for item in dream_results:
                # 한 줄로 출력
                st.write(f"**{item['title']}**: {item['description']} [Read more]({item['link']})")
        else:
            st.write("No encyclopedia results found.")

        # OpenAI LangChain을 통한 질의 응답
        st.subheader("AI Chatbot Response:")
        response = qa_chain.run({"question": query, "chat_history": []})
        if response:
            st.write(response)

if __name__ == "__main__":
    qa_chain = get_qa_chain()

    # CSS를 사용하여 배경색을 그라데이션으로 설정하고, 제목과 검색창의 색상을 변경
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(to bottom, #0b1e2e, #f8c9d4);
            }
            .stApp header h1 {
                color: #ffffff !important; /* 제목 색상 */
            }
            .stApp .stTextInput input {
                background-color: #333333 !important; /* 검색창 배경색 */
                color: #ffffff !important; /* 검색창 텍스트 색상 */
            }
            .stApp .stTextInput label {
                color: #ffffff !important; /* 검색창 라벨 색상 */
            }
            .css-1d391kg, .css-1d391kg * {
                color: #000000 !important; /* 사이드바 텍스트 색상 */
            }
        </style>
    """, unsafe_allow_html=True)

    # 제목과 검색창 추가
    st.title("Dream Interpretation Blog & Encyclopedia Search")
    query = st.text_input("Enter a keyword for dream interpretation")

    # 검색 기록을 저장할 리스트
    if 'search_history' not in st.session_state:
        st.session_state['search_history'] = []

    # 검색어 수신 및 처리
    if query:
        st.write(f"Received query: {query}")
        # 검색어를 사용하여 검색 수행
        run_ui(qa_chain, query)
        # 검색 기록에 날짜와 함께 추가
        search_record = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {query}"
        st.session_state['search_history'].append(search_record)

    # 사이드바에 검색 기록 표시
    st.sidebar.title("Search History")
    for i, record in enumerate(st.session_state['search_history']):
        if st.sidebar.button(f"{i + 1}. {record}"):
            st.session_state['selected_record'] = record

    # 선택된 검색 기록 표시
    if 'selected_record' in st.session_state:
        st.write(f"Selected Record: {st.session_state['selected_record']}")