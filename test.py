import streamlit as st
import requests
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Naver API 설정
CLIENT_ID = 'kOTwXT4d09oyxlqSO_Vg'
CLIENT_SECRET = 'uKa8vmVcsI'

def search_dream(query):
    url = f"https://openapi.naver.com/v1/search/encyc.json?query={query}"
    headers = {"X-Naver-Client-Id": CLIENT_ID, "X-Naver-Client-Secret": CLIENT_SECRET}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        st.error(f"API 호출 중 오류가 발생했습니다: {e}")
        return None

# OpenAI API 설정
openai_api_key = "your_openai_api_key"

# 벡터 DB 설정 및 LangChain 체인 정의
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectordb = Chroma(embedding_function=embedding)

memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
llm = OpenAI(openai_api_key=openai_api_key)

qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(), memory=memory)

# Streamlit UI
st.title('Dream Interpreter & Chatbot')

query = st.text_input('Enter your dream description or question:')
if query:
    # Naver API를 통해 꿈 해석
    
    result = search_dream(query)
    if result:
        st.write("Dream Interpretation:")
        for item in result:
            st.write(f"**Title:** {item['title']}")
            st.write(f"**Description:** {item['description']}")
    else:
        st.write('No dream results found.')

    # LangChain을 통한 질의 응답
    st.write("AI Chatbot Response:")
    response = qa_chain.run({"query": query})
    st.write(response)
