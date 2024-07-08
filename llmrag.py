"""
vector database utilities
"""

import requests
#from sentence_transformers import SentenceTransformer
import log, llm

# Load a pre-trained model
#model = SentenceTransformer('all-MiniLM-L6-v2')
doc_path = "C:\\youtube_transcripts"

# Define the base URL of your ChromaDB REST API
chroma_db_url = "http://localhost:8000/api/v1"
# Define the collection name and the query parameters
persist_directory = "youtube_db"
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
        #check if chunk already exists in the database to avoid duplicates
    #if not collection.get(ids=[f"{video_id}_{idx}"]):
        add_record(collection_id,
            {
                "documents":[chunk],
                "metadatas":[{"source": video_id}], # filter on these!
                "ids":[f"{video_id}_{idx}"], # unique for each chunk of the document
                "embeddings": [llm.embeddings(chunk)] # embed the chunk of text
                #"embeddings": model.encode([chunk]).tolist() # embed the chunk of text
            }
        )
        log.stdout(get_record(collection_id=collection_id, record_id=f"{video_id}_{idx}"))

def query (text, collection_name):
    collection_id = get_or_create_collection(collection_name)
    # Generate embeddings
    embeddings = llm.embeddings(text) # embed the chunk of text
    #embeddings = model.encode([text])
    # Perform the query by sending a POST request
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

# Function to upsert a record in a collection
# def upsert_record(collection_id, record):
#     endpoint = upsert_record_endpoint.replace("collection_id", collection_id)
#     print(endpoint)
#     payload = {
#         "ids": [record["id"]],
#         "records": [record["data"]]
#     }
#     response = requests.post(endpoint, json=payload)
#     if response.status_code == 200:
#         print("Record upserted successfully: " + response.text)
#     else:
#         print(f"Failed to upsert record with status code {response.status_code}: {response.text}")

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

    # record_to_upsert = {
    # "id": "1",
    # "metadatas": [{"source":"meta2"}],
    # "embeddings": model.encode("Updated Another text for the collection.").tolist(),
    # "data": {
    #     "text": "Updated Another text for the collection.",
    #     "embeddings": model.encode("Updated Another text for the collection.").tolist()
    # }
    # }
    # upsert_record(collection_id, record_to_upsert)
    # get_record(collection_id, "1")

    # # Example data for querying
    # texts = [
    #     "what is another text"
    # ]

    # # query_params = {
    # #     "parameter1": "another text",
    # #     # Add other parameters as required
    # # }
    # # response = requests.post(query_endpoint.replace('collection_id', collection_id), json=query_params)

    # # Generate embeddings
    # embeddings = model.encode(texts)
    # # Perform the query by sending a POST request
    # query_params = {
    #     "collection": collection_name,
    #     "n_results": 1,
    #     "query_embeddings": embeddings.tolist()  # Convert numpy array to list
    # }

    # # Perform the query by sending a POST request
    # response = requests.post(query_endpoint.replace('collection_id', collection_id), json=query_params)
    query('what is another text', collection_name)
    # Check if the request was successful
    # if response.status_code == 200:
    #     try:
    #         # Parse the JSON response
    #         query_result = response.json()
    #         # Print the result (or handle it as needed)
    #         log.stdout(query_result)
    #     except requests.exceptions.JSONDecodeError:
    #         log.stdout(f"Failed to decode JSON with status code {response.status_code}: {response.text}")
    # else:
    #     # log.stdout the error message if the request failed
    #     log.stdout(f"Query failed with status code {response.status_code}: {response.text}")

    # record_id_to_update = "1"
    # updated_record = {
    #     "field1": "new_value1",
    #     "field2": "new_value2"
    # }
    # update_record(collection_id, record_id_to_update, updated_record)

    record_id_to_remove = "1"
    remove_record(collection_id, record_id_to_remove)

    delete_collection(collection_name)
if __name__=='__main__':
    test()