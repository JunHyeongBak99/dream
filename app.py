from flask import Flask, request, jsonify, render_template
import requests
import openai
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import OpenAI

app = Flask(__name__)

CLIENT_ID = 'kOTwXT4d09oyxlqSO_Vg'
CLIENT_SECRET = 'uKa8vmVcsI'
openai_api_key = "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"
openai.api_key = openai_api_key

# Naver 백과사전 검색 API 호출 함수
def search_dream(query):
    url = f"https://openapi.naver.com/v1/search/encyc.json?query={query}"
    headers = {"X-Naver-Client-Id": CLIENT_ID, "X-Naver-Client-Secret": CLIENT_SECRET}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

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
        return {"error": str(e)}

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        dream_results = search_dream(query + ' 꿈 해몽')
        blog_results = search_blog(query + ' 꿈 해몽')
        qa_chain = get_qa_chain()
        openai_response = qa_chain.run({"query": query})
        return jsonify({
            "dream_results": dream_results,
            "blog_results": blog_results,
            "openai_response": openai_response
        })
    return jsonify({"error": "No query provided"})

if __name__ == '__main__':
    app.run(debug=True)