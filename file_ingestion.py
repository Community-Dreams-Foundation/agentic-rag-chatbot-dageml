from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
import chromadb.utils.embedding_functions as embedding_functions

#import .env
from dotenv import load_dotenv

API_KEY = load_dotenv("API_KEY")

#configurations
DATA_PATH = r"sample_docs"
CHROMA_PATH = r"chroma_db"


huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=API_KEY,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)




#define embeddings model

#embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

#vector store
vector_store = Chroma(
    collection_name = "example_collection",
    embedding_function = huggingface_ef,
    persist_directory=CHROMA_PATH

)
print("Vector store initialized")

#load documents
loader = PyPDFDirectoryLoader(DATA_PATH)
raw_documents = loader.load()
print(f"Loaded {len(raw_documents)} documents")


#split documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size= 200,
    chunk_overlap = 20,
    length_function = len,
    is_separator_regex=False
)

print("Splitting documents into chunks...")

#split documents into chunks
chunks = text_splitter.split_documents(raw_documents)
print(f"Created {len(chunks)} chunks")

uuids = [str(uuid4()) for _ in range(len(chunks))]

vector_store.add_documents(chunks, ids=uuids)
print("Documents added to vector store")
print(vector_store.get_collection("example_collection").count())




         




