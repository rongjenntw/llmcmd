import chromadb

persist_directory = "youtube_db"
collection_name = "peristed_collection"
doc_path = "C:\\youtube_transcripts"

client = chromadb.PersistentClient(path=persist_directory)
# collection = client.get_or_create_collection(name=collection_name)
#client = chromadb.Client()
collection = client.get_or_create_collection(name=collection_name)

# Function to chunk a large document
def chunk_document(document, chunk_size=512):
    words = document.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def add_youtub_transcript_to_db(video_id):
    with open(f"{doc_path}\\{video_id}.txt", "r") as f:
        document = f.read()
    for idx, chunk in enumerate(chunk_document(document, chunk_size=512)):
        #check if chunk already exists in the database to avoid duplicates
    #if not collection.get(ids=[f"{video_id}_{idx}"]):
        collection.add(
        documents=[chunk],
        metadatas=[{"source": video_id}], # filter on these!
        ids=[f"{video_id}_{idx}"], # unique for each chunk of the document
        )
    #    print(f'Added chunk {idx} of video {video_id}')
    #else:
    #    print(f'Chunk {idx} of video {video_id} already exists in the database')

def query(text):
    results = collection.query(
        query_texts=[text],
        n_results=2,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )
    return results

if __name__ == "__main__":
    # read text from file and add to collection


    print (query(input('> '))) # returns the id of most similar document to "What is pytorch?"'''