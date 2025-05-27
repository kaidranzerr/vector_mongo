import pymongo

client = pymongo.MongoClient("mongodb+srv://ashstark68:<db_password>@cluster0.bxfccpt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collections = db.movies
items = collections.find.limit(5)

for item in items:
    print(item)


# embedding creation function
hf_token = "HF_token"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embeddings(text: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text})
    
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

    return response.json()

# vector similarity search within a database collection
results = collection.aggregate([ # mongodb aggregation pipeline
    #  The aggregate method allows you to process data records and return computed results.
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100,
    "limit": 4,
    "index": "PlotSemanticSearch",
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')