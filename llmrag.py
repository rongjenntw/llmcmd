"""
vector database utilities
"""

import requests, json
#from sentence_transformers import SentenceTransformer
import log, llm

with open('config.json', 'r') as file:
    config = json.load(file)
# Load a pre-trained model
#model = SentenceTransformer('all-MiniLM-L6-v2')
doc_path = config.get('rag_doc_dir')

# Define the base URL of your ChromaDB REST API
chroma_db_url = config.get('ragdb_url')
# Define the collection name and the query parameters
persist_directory = config.get('ragdb_path')
#collection_name = "peristed_collection"

# Define the endpoints for various operations
collections_endpoint = f"{chroma_db_url}/collections"
create_collection_endpoint = f"{chroma_db_url}/collections"
query_endpoint = f"{chroma_db_url}/collections/collection_id/query"
add_record_endpoint = f"{chroma_db_url}/collections/collection_id/add"
upsert_record_endpoint = f"{chroma_db_url}/collections/collection_id/upsert"
update_record_endpoint = f"{chroma_db_url}/collections/collection_id/update"
remove_record_endpoint = f"{chroma_db_url}/collections/collection_id/delete"
get_record_endpoint = f"{chroma_db_url}/collections/collection_id/get"


def add_youtub_transcript_to_db(video_id, collection_name):
    collection_id = get_or_create_collection(collection_name)
    with open(f"{doc_path}\\{video_id}.txt", "r") as f:
        document = f.read()
    for idx, chunk in enumerate(chunk_document(document, chunk_size=512)):
        add_record(collection_id,
            {
                "documents":[chunk],
                "metadatas":[{"source": video_id}], # filter on these!
                "ids":[f"{video_id}_{idx}"], # unique for each chunk of the document
                "embeddings": [llm.embeddings(chunk)] # embed the chunk of text
            }
        )
        log.stdout(get_record(collection_id=collection_id, record_id=f"{video_id}_{idx}"))

def query (text, collection_name):
    collection_id = get_or_create_collection(collection_name)
    # Generate embeddings
    embeddings = llm.embeddings(text) # embed the chunk of text
    query_params = {
        "collection": collection_name,
        "n_results": 2,
        "query_embeddings": [embeddings] # Convert numpy array to list
    }
    log.stdout(query_params)
    # Perform the query by sending a POST request
    response = requests.post(query_endpoint.replace('collection_id', collection_id), json=query_params)
    log.stdout(response.text)
    return response.json()

def get_or_create_collection(collection_name):
    isexist, collection_id = check_collection_exists(collection_name)
    if not isexist:
        collection_id = create_collection(collection_name)
    return collection_id

# Function to chunk a large document
def chunk_document(document, chunk_size=512):
    words = document.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

# Function to check if a collection exists
def check_collection_exists(collection_name):
    response = requests.get(collections_endpoint)
    if response.status_code == 200:
        collections = response.json()
        for collection in collections:
            if collection['name'] == collection_name:
                log.stdout('collection found: ' + str(collection))
                return True, collection['id']
        return False, None
    else:
        log.stdout(f"Failed to retrieve collections with status code {response.status_code}: {response.text}")
        return False, None

# Function to create a collection
def create_collection(collection_name):
    payload = {
        "name": collection_name,
        # Add other collection configuration as required
    }
    response = requests.post(create_collection_endpoint, json=payload)
    if response.status_code == 200:
        log.stdout(f"Collection '{response.text}' created successfully.")
        return response.json()['id']
    else:
        log.stdout(f"Failed to create collection with status code {response.status_code}: {response.text}")
        return None

# Function to get a record to a collection
def get_record(collection_id, record_id):
    payload = {
        "ids": [record_id]
    }
    response = requests.post(get_record_endpoint.replace("collection_id", collection_id), json=payload)
    if response.status_code == 200:
        log.stdout("get records: " + response.text)
    else:
        log.stdout(f"Failed to get records with status code {response.status_code}: {response.text}")

# Function to add a record to a collection
def add_record(collection_id, record):
    response = requests.post(add_record_endpoint.replace("collection_id", collection_id), json=record)
    if response.status_code == 201:
        log.stdout("Record added successfully: " + response.text)
    else:
        log.stdout(f"Failed to add record with status code {response.status_code}: {response.text}")

# Function to update a record in a collection
def update_record(collection_id, record_id, updated_record):
    endpoint = update_record_endpoint.replace("collection_id", collection_id)
    payload = {
        "id": record_id,
        "updated_record": updated_record
    }
    response = requests.put(endpoint, json=payload)
    if response.status_code == 200:
        log.stdout("Record updated successfully.")
    else:
        log.stdout(f"Failed to update record with status code {response.status_code}: {response.text}")

# Function to remove a record from a collection
def remove_record(collection_id, record_id):
    endpoint = remove_record_endpoint.replace("collection_id", collection_id)
    payload = {
        "ids": [record_id]
    }
    response = requests.post(endpoint, json=payload)
    if response.status_code == 200:
        log.stdout("Record removed successfully.")
    else:
        log.stdout(f"Failed to remove record with status code {response.status_code}: {response.text}")

# Function to delete a collection
def delete_collection(collection_name):
    delete_collection_endpoint = f"{chroma_db_url}/collections/{collection_name}"
    response = requests.delete(delete_collection_endpoint.replace("{collection_name}", collection_name))
    if response.status_code == 200:
        log.stdout(f"Collection '{collection_name}' deleted successfully.")
    else:
        log.stdout(f"Failed to delete collection with status code {response.status_code}: {response.text}")

def test():
    collection_name="test_collection"
    # Check if the collection exists, and create it if it does not
    isexist, collection_id = check_collection_exists(collection_name)
    if not isexist:
        collection_id = create_collection(collection_name)

    # Example usage of add, update, remove, and delete functions
    doc1 = "Another text for the collection."
    doc2 = "Second Another text for the collection."
    record_to_add = {
    "ids": ["4","3"],
    "metadatas": [{"source":"meta1"},{"source":"meta2"}],
    "documents": [doc1, doc2],
    "embeddings":[llm.embeddings(doc1), llm.embeddings(doc2)]
    #"embeddings":[model.encode(doc1).tolist(), model.encode(doc2).tolist()]
}
    add_record(collection_id, record_to_add)

    get_record(collection_id, "4")

    query('what is another text', collection_name)

    record_id_to_remove = "1"
    remove_record(collection_id, record_id_to_remove)

    delete_collection(collection_name)
if __name__=='__main__':
    test()