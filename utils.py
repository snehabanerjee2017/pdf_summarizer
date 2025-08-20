from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from pypdf import PdfReader

def process_text(text:str):
    """Splits text into chunks. And converting these chunks into embeddings using HuggingFaceEmbeddings to form a knowledge base."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000, 
        chunk_overlap=200,
        length_function=len)
    
    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create a FAISS index from the text chunks using the embeddings. Performs similarity search.
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base

def summarizer(pdf):

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        knowledge_base = process_text(text)

        query = "Summarize the content of the uploaded PDF file in approximately 3-5 sentences."

        if query:
            docs = knowledge_base.similarity_search(query)

            openAI_model = "gpt-3.5-turbo-16k"
            llm = ChatOpenAI(model_name=openAI_model, temperature=0.8) # more the temperature, more the creativity of the response

            chain = load_qa_chain(llm, chain_type="stuff")

            with get_openai_callback():

                response = chain.run(input_documents=docs, question=query)

                return response