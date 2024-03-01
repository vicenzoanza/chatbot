import os
from flask import Flask, render_template, request, jsonify
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from scraping import extraer_informacion

# Primero llamar extraer_informacion()
extraer_informacion()

app = Flask(__name__)

# Clave de la API de OpenAI
os.environ["OPENAI_API_KEY"] = ''

# Inicialización de variables globales
query = None
chat_history = []

# Cargar documentos y configurar models
loader = DirectoryLoader("informacion/")
documents = loader.load()

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(documents, embeddings)

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=docsearch.as_retriever(search_kwargs={"k": 1})
)

# Ruta raíz
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar solicitudes POST
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    
    # Entrada del usuario y obtener respuesta del chatbot
    result = chain({"question": user_input, "chat_history": chat_history})
    response = result['answer']
    
    # Agregar pregunta y respuesta al historial de chat
    chat_history.append((user_input, response))
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)


