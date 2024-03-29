import os
from langchain import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

load_dotenv()

conversation_retrieval_chain = None
chat_history = []
llm = None
llm_embeddings = None

def init_llm():
    global llm, llm_embeddings
    api_key="Rugi_Dong"
    llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key)
    llm_embeddings = OpenAIEmbeddings(openai_api_key = api_key)

def process_document(document_path):
    global conversation_retrieval_chain, llm, llm_embeddings
    loader = PyPDFLoader(document_path)    
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    db = Chroma.from_documents(texts, llm_embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    conversation_retrieval_chain = ConversationalRetrievalChain.from_llm(llm, retriever)

def process_prompt(prompt):
    global conversation_retrieval_chain
    global chat_history
    result = conversation_retrieval_chain({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result["answer"]))
    return result['answer']


init_llm()

#-_-#
