import os
import streamlit as st
import openai
import requests
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

# OpenAI API 키 설정
openai_api_key = "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"
openai.api_key = openai_api_key

# 네이버 API 설정
CLIENT_ID = "uh2AfBPLQDIUkXpkvnQC"
CLIENT_SECRET = "dXBin21ECU"

# 네이버 검색 결과를 가져오는 함수
def search_dream_with_naver(query):
    url = f"https://openapi.naver.com/v1/search/encyc.json?query={query}"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        items = response.json().get("items", [])
        return [f"{item['title']} - {item['description']}" for item in items]
    except requests.exceptions.RequestException as e:
        st.error(f"네이버 API 호출 오류: {e}")
        return []

# LangChain RAG 구성 함수
def initialize_rag_system(naver_results):
    if not naver_results:
        st.warning("네이버 검색 결과가 없습니다. 기본 데이터를 사용합니다.")
        naver_results = ["기본 데이터 예시"]

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = Chroma.from_texts(naver_results, embeddings)

    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    return ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, memory=memory
    )

# Streamlit UI 구성
def run_ui():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to bottom, #0b1e2e, #f8c9d4);
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🌙 당신의 밤은 안녕하신가요?")
    st.markdown("네이버 검색 결과와 GPT를 활용한 통합 해석 시스템입니다.")

    dream_description = st.text_area("꿈 설명을 입력하세요", placeholder="예: 숲 속에서 길을 잃고 어둠 속에서 쫓기는 꿈을 꾸었습니다.")
    stress_score = st.slider("스트레스 수준을 선택하세요", 0, 100, 50)

    if st.button("해석 요청"):
        if dream_description:
            st.subheader("💬 GPT 해몽 및 조언")
            question = f"꿈 설명: {dream_description}\n스트레스 수준: {stress_score}/100\n"
            llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

            try:
                #question 변수가 리스트인지 확인
                st.write(f"전달된 질문: {question}")
                st.write(f"질문 타입: {type(question)}")
                response = llm.generate([question])
                st.write(response.generations[0][0].text.strip())
            except openai.OpenAIError as e:
                st.error(f"OpenAI API 호출 오류: {e}")
            except ValueError as ve:
                st.error(f"입력 값 오류: {ve}")
            except Exception as e:
                st.error(f"예기치 못한 오류 발생: {e}")

            st.subheader("🔍 네이버 검색 결과")
            naver_results = search_dream_with_naver(dream_description + " 꿈 해몽")
            if naver_results:
                for result in naver_results:
                    st.write(f"- {result}")
            else:
                st.write("네이버 검색 결과가 없습니다.")
        else:
            st.warning("꿈 설명을 입력해주세요!")

# 실행
if __name__ == "__main__":
    run_ui()
