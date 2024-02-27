import os
import json
from flask import Flask, render_template, request, jsonify
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAI


def cargar_configuracion():
    with open('config.json') as f:
        config = json.load(f)
    return config

config = cargar_configuracion()
os.environ["openai_api_key"] = config['openai_api_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    
    # Procesar la entrada del usuario y obtener la respuesta del chatbot
    result = chain({"question": user_input, "chat_history": chat_history})
    response = result['answer']
    
    # Agregar la pregunta y la respuesta al historial de chat
    chat_history.append((user_input, response))
    
    return jsonify({'response': response})

if __name__ == '__main__':
    query = None
    chat_history = []
    
    loader = DirectoryLoader("informacion/")
    documents = loader.load()
 
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(documents, embeddings)
 
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())
 
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-4"),
        retriever=docsearch.as_retriever(search_kwargs={"k": 1})
    )

    app.run(debug=True)
