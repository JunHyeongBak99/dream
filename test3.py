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

# OpenAI API 키를 직접 설정
openai_api_key = "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"  # 여기에 실제 OpenAI API 키를 입력하세요.
openai.api_key = openai_api_key

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
        return response.json()
    except Exception as e:
        print(f"Naver API 호출 중 오류가 발생했습니다: {e}")
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

# 별빛 애니메이션 설정
def setup_particles_via_iframe():
    # tsParticles 별빛 애니메이션을 위한 HTML 코드
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Particles</title>
        <style>
            #particles-js {
                position: fixed;
                width: 100%;
                height: 100%;
                z-index: -1;
                background: linear-gradient(to bottom, #0b1e2e, #f8c9d4); /* 그라데이션 배경 */
            }
            body {
                margin: 0;
                overflow: hidden;
                height: 100vh;
            }
            .content {
                position: relative;
                z-index: 1;
                color: white;
                text-align: center;
                padding-top: 50px;
            }
        </style>
    </head>
    <body>
        <div id="particles-js"></div>
        <div class="content">
            <h1>Dream Interpretation Blog & Encyclopedia Search</h1>
            <input type="text" id="query" placeholder="Enter a keyword for dream interpretation">
            <button onclick="search()">Search</button>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.0.0/tsparticles.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@tsparticles/preset-stars@3/tsparticles.preset.stars.bundle.min.js"></script>
        <script>
            (async () => {
                await loadStarsPreset(tsParticles);
                tsParticles.load("particles-js", {
                    particles: {
                        number: {
                            value: 150,
                            density: {
                                enable: true,
                                value_area: 800
                            }
                        },
                        color: { value: "#ffffff" },
                        shape: { type: "circle", stroke: { width: 0, color: "#000000" } },
                        opacity: { value: 0.7, random: false },
                        size: { value: 4, random: true },
                        move: { enable: true, speed: 3, direction: "none", random: false }
                    },
                    interactivity: {
                        detect_on: "canvas",
                        events: {
                            onhover: { enable: true, mode: "repulse" },
                            onclick: { enable: true, mode: "push" },
                            resize: true
                        },
                        modes: {
                            repulse: { distance: 100, duration: 0.4 },
                            push: { particles_nb: 4 }
                        }
                    },
                    retina_detect: true
                });
            })();
            function search() {
                const query = document.getElementById('query').value;
                if (query) {
                    window.parent.postMessage({ type: 'search', query: query }, '*');
                }
            }
        </script>
    </body>
    </html>
    """
    # HTML 코드 삽입
    components.html(html_code, height=700)

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
            .stApp {{
                background: transparent;
            }}
        </style>
    """, unsafe_allow_html=True)

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
    setup_theme()  # 테마 설정
    setup_particles_via_iframe()  # 별빛 애니메이션

    # JavaScript 메시지 수신 설정
    st.markdown("""
        <script>
            window.addEventListener("message", (event) => {
                if (event.data.type === "search") {
                    const query = event.data.query;
                    window.parent.postMessage({ type: "streamlit:setQuery", query: query }, "*");
                }
            });
        </script>
    """, unsafe_allow_html=True)

    # 검색어 수신 및 처리
    if "streamlit:setQuery" in st.session_state:
        query = st.session_state["streamlit:setQuery"]
        st.write(f"Received query: {query}")
        # 검색어를 사용하여 검색 수행
        run_ui(qa_chain, query)
    else:
        run_ui(qa_chain, None)