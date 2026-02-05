import json
import os
import chromadb
from sentence_transformers import SentenceTransformer
from colorama import Fore, Style, init

# Initialize Colorama for War Mode Output
init(autoreset=True)

# CONFIGURATION
BRAIN_FILE = os.path.join("data", "processed", "ashish_kapoor_brain.json")
VECTOR_DB_PATH = os.path.join("data", "vector_store")
MODEL_NAME = "all-MiniLM-L6-v2" # Fast, free, local embedding model

def setup_brain():
    print(Fore.YELLOW + "[*] Initializing the Intuition Engine...")
    
    # 1. Initialize Vector DB (Persistent - saves to disk)
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    
    # Create or get collection
    try:
        # We try to get it first
        collection = client.get_collection(name="physics_intuition")
        print(Fore.CYAN + "[*] Found existing memory matrix.")
    except:
        # If not found, create it
        print(Fore.CYAN + "[*] Creating new neural matrix...")
        collection = client.create_collection(name="physics_intuition")
    
    # 2. Check if we need to load data
    if collection.count() > 0:
        print(Fore.GREEN + f"[+] Brain already has {collection.count()} memories loaded. Skipping ingestion.")
        return collection

    # 3. Load the JSON Brain
    if not os.path.exists(BRAIN_FILE):
        print(Fore.RED + f"[!] CRITICAL: {BRAIN_FILE} not found. Run refinery.py first.")
        return None

    with open(BRAIN_FILE, 'r', encoding='utf-8') as f:
        knowledge_base = json.load(f)
        
    print(Fore.CYAN + f"[*] Embedding {len(knowledge_base)} concepts (This will take ~30 seconds)...")
    
    # 4. Embed and Index
    ids = []
    documents = []
    metadatas = []
    
    for i, item in enumerate(knowledge_base):
        ids.append(item['id'])
        # Embed topic + content for context
        documents.append(f"{item['topic']}: {item['content']}")
        metadatas.append({"source": item['lesson'], "type": "analogy"})
        
    # Add to ChromaDB
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(Fore.GREEN + "[SUCCESS] Brain Indexed. The Engine is online.")
    return collection

def consult_oracle(collection):
    print(Fore.WHITE + "\n" + "="*50)
    print(Fore.YELLOW + "   EXAM SENSE AI - INTUITION PROTOTYPE (v0.1)")
    print(Fore.WHITE + "="*50)
    
    while True:
        query = input(Fore.CYAN + "\n[Student asks]: " + Style.RESET_ALL)
        if query.lower() in ['exit', 'quit']:
            break
            
        print(Fore.MAGENTA + "[*] Thinking (Retrieving Analogies)...")
        
        # Search the vector DB
        results = collection.query(
            query_texts=[query],
            n_results=1 # Just get the best one for now
        )
        
        # Display the "Ashish Kapoor" Result
        if results['documents'][0]:
            print(Fore.GREEN + "\n--- RETRIEVED INTUITION ---")
            story = results['documents'][0][0]
            source = results['metadatas'][0][0]['source']
            
            print(f"{Fore.YELLOW}Source: {source}")
            print(Fore.WHITE + story[:1000] + "...") # Preview
            
            print(Fore.BLUE + "\n[AI Internal Monologue]:")
            print(f"Found a match. Now I would explain '{query}' using the story from '{source}'.")
        else:
            print(Fore.RED + "[!] No intuition found. I need more data.")

if __name__ == "__main__":
    col = setup_brain()
    if col:
        consult_oracle(col)