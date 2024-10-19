import streamlit as st
import streamlit.components.v1 as components
import requests
import openai
import os
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI


# OpenAI API를 직접 호출하는 함수
def get_openai_response(prompt):
    try:
        # GPT-3.5 또는 GPT-4 모델을 호출하는 부분
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 또는 gpt-4 사용 가능
            messages=[
                {"role": "system", "content": "당신의 밤은 안녕한가요?"},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"OpenAI API 호출 중 오류가 발생했습니다: {e}")
        return None

openai.api_key = os.getenv("OPENAI_API_KEY")  # 또는 직접 API 키를 넣어도 됩니다.

# Naver API 설정
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
# LangChain 설정 함수: qa_chain 설정
def get_qa_chain():
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(embedding_function=embedding)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    llm = OpenAI()
    
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(), memory=memory)
    return qa_chain

# 별빛 애니메이션 설정
def setup_particles():
    particles_html = """
    <div id="particles-js" style="position:fixed; width:100%; height:100%; z-index:-1;"></div>
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

# 테마 설정 함수
def setup_theme():
    light_theme = {"bgcolor": "#FFFFFF", "textcolor": "#000000"}
    dark_theme = {"bgcolor": "#000000", "textcolor": "#FFFFFF"}

    theme_mode = st.sidebar.radio("Select Theme", ("Light", "Dark"))

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

def run_ui(qa_chain):
    # qa_chain이 제대로 전달되지 않았을 경우 오류를 표시
    if qa_chain is None:
        st.error("qa_chain 인자가 전달되지 않았습니다.")
        return
    

    st.title('Dream Interpretation Blog & Encyclopedia Search')

    query = st.text_input("Enter a keyword for dream interpretation:")
    
    if query:
        # Naver API를 통한 꿈 해석
        
        blog_results = search_blog(query + ' 꿈 해몽')
        dream_results = search_dream(query + ' 꿈 해몽')

        if blog_results:
            st.subheader("Blog Search Results:")
            for item in blog_results:
                st.write(f"**Title:** {item['title']}")
                st.write(f"**Description:** {item['description']}")
                st.write(f"[Read more]({item['link']})")
                st.write("---")
        else:
            st.write("No blog results found.")

         # OpenAI LangChain을 통한 질의 응답
        st.subheader("AI Chatbot Response:")
        response = qa_chain.run({"query": query})
        if response:
            st.write(response)

if __name__ == "__main__":
    qa_chain = get_qa_chain()
    print("qa_chain:", qa_chain)  # qa_chain이 제대로 생성되었는지 확인
    setup_particles()  # 별빛 애니메이션
    setup_theme()  # 테마 설정
    run_ui(qa_chain)  # UI 실행

