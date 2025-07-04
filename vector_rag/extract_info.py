from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader 
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import gradio as gr 
from gradio.theme.base import Base 
import key_param  

client = MongoClient(key_param.MONGO_URI)
dbName = "langchain_demo"
collectionName = "collection_of_text_blobs"
collection = client[dbName][collectionName]


embeddings = OpenAIEmbeddings(openai_api_key = key_param.open_api_key)

# vectorize the text from document using specified embedding model and insert them into specified mongoDB collection
vectorStore = MongoDBAtlasVectorSearch( collection , embeddings )

def query_data(query):
    docs = vectorStore.similarity_search(query , K = 1)
    as_output = docs[0].page_content

    llm = OpenAI(openai_api_key=key_param.open_api_key,temperature=0)
    retriever = vectorStore.as_retriever()
    qa = RetrievalQA.from_chain_type(llm , chain_type="stuff" , retriever=retriever)
    retriever_output = qa.run(query)
    return as_output , retriever_output

with gr.Blocks(theme=Base() , title="Question Answering App using vector search + RAG") as demo:
    gr.Markdown(
        """
        # Question Answering App using Atlas Vector Search 
        """
    )
    textbox = gr.Textbox(label="Enter your question")
    with gr.Row():
        button = gr.Button("Submit" , variant="primary")
    with gr.Column():
        output1 = gr.Textbox(lines=1 , max_lines=10 , label="Output with just Atlas Vector Search")
        output2 = gr.Textbox(lines=1 , max_lines=10 , label="Output generated by changing Atlas Vector Search")

    button.click(query_data , textbox , outputs=[output1 , output2])
demo.launch()