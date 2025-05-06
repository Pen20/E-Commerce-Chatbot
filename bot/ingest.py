from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from bot.data_converter import dataconverter  # Import your data conversion function

# Load environment variables from .env
load_dotenv()

# Fetch environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

# Validate environment variables early
if not all([OPENAI_API_KEY, ASTRA_DB_API_ENDPOINT, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_KEYSPACE]):
    raise EnvironmentError("One or more required environment variables are missing.")

# Set up OpenAI embeddings
embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def ingestdata(status=None):
    """Ingests data into AstraDBVectorStore and returns the vector store and inserted document IDs (if any)."""
    vstore = AstraDBVectorStore(
        embedding=embedding,
        collection_name="chatbotecommerce",
        api_endpoint=ASTRA_DB_API_ENDPOINT,        
        token=ASTRA_DB_APPLICATION_TOKEN,          
        namespace=ASTRA_DB_KEYSPACE,               
    )

    if status is None:
        docs = dataconverter()
        inserted_ids = vstore.add_documents(docs)
        return vstore, inserted_ids

    return vstore, None

if __name__ == '__main__':
    try:
        # Ingest data
        vstore, inserted_ids = ingestdata()

        if inserted_ids:
            print(f"\nInserted {len(inserted_ids)} documents.")

        # Perform similarity search
        query = "can you tell me the low budget sound basshead."
        results = vstore.similarity_search(query)

        print("\nSearch Results:")
        for res in results:
            print(f"* {res.page_content} [{res.metadata}]")

    except Exception as e:
        print(f"Error during ingestion or search: {e}")
