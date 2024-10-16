import streamlit as st
import streamlit.components.v1 as components
import requests
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


# Naver API 설정
# Naver API 인증 정보 설정
CLIENT_ID = 'kOTwXT4d09oyxlqSO_Vg'
CLIENT_SECRET = 'uKa8vmVcsI'

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

# Streamlit UI
st.title('Dream Interpretation Blog & Encyclopedia Search')

# 검색어 입력 필드
query = st.text_input("Enter a keyword for dream interpretation:")

if query:
    # 블로그 검색과 백과사전 검색을 각각 호출
    blog_results = search_blog(query + ' 꿈 해몽')  # '꿈 해몽'을 검색어에 추가
    dream_results = search_dream(query + ' 꿈 해몽')

    # 블로그 검색 결과 출력
    if blog_results:
        st.subheader("Blog Search Results:")
        for item in blog_results:
            st.write(f"**Title:** {item['title']}")
            st.write(f"**Description:** {item['description']}")
            st.write(f"[Read more]({item['link']})")
            st.write("---")
    else:
        st.write("No blog results found.")

    # 백과사전 검색 결과 출력
    if dream_results:
        st.subheader("Encyclopedia Search Results:")
        for item in dream_results:
            st.write(f"**Title:** {item['title']}")
            st.write(f"**Description:** {item['description']}")
            st.write("---")
    else:
        st.write("No encyclopedia results found.")

# OpenAI API 설정
openai_api_key = "your_openai_api_key"

# 벡터 DB 설정 및 LangChain 체인 정의
embedding = OpenAIEmbeddings()
vectordb = Chroma(embedding_function=embedding)

memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
llm = OpenAI(openai_api_key=openai_api_key)

qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(), memory=memory)

# 별빛 애니메이션을 포함한 HTML/CSS
st.markdown("<h1 style='text-align: center; color: white;'>Dream Interpreter</h1>", unsafe_allow_html=True)

# custom JS for particles.js background
particles_html = """
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
  "particles": {
    "number": {
      "value": 80,
      "density": {
        "enable": true,
        "value_area": 800
      }
    },
    "color": {
      "value": "#ffffff"
    },
    "shape": {
      "type": "circle",
      "stroke": {
        "width": 0,
        "color": "#000000"
      },
    },
    "opacity": {
      "value": 0.5,
      "random": false,
    },
    "size": {
      "value": 3,
      "random": true,
    },
    "move": {
      "enable": true,
      "speed": 2,
      "direction": "none",
      "random": false,
    }
  }
});
</script>
"""

components.html(particles_html, height=500)

# light 모드와 dark 모드
light_theme = {"bgcolor": "#FFFFFF", "textcolor": "#000000"}
dark_theme = {"bgcolor": "#000000", "textcolor": "#FFFFFF"}

# 다크모드 스위치 버튼
theme_mode = st.sidebar.radio("Select Theme", ("Light", "Dark"))

# Apply selected theme
current_theme = light_theme if theme_mode == "Light" else dark_theme

st.markdown(f"""
    <style>
        .reportview-container {{
            background-color: {current_theme['bgcolor']};
        }}
        .markdown-text-container {{
            color: {current_theme['textcolor']};
        }}
    </style>
    """, unsafe_allow_html=True)

# Test content
st.title("Theme Switching Example")
st.write("This text will change color based on the selected theme.")

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
