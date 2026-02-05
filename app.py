import streamlit as st
import chromadb
import google.generativeai as genai
import os

# PAGE CONFIG
st.set_page_config(page_title="Exam Sense AI", page_icon="🧠", layout="centered")

# SETUP GOOGLE AI (Using Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing Gemini API Key. Please add it to .streamlit/secrets.toml")

# PATHS
VECTOR_DB_PATH = os.path.join("data", "vector_store")

# CACHED BRAIN LOADING
@st.cache_resource
def load_brain():
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    collection = client.get_collection(name="physics_intuition")
    return collection

# THE ASHISH KAPOOR GENERATOR
def generate_intuition(concept, story_text):
    """
    Takes the raw story and uses Gemini to teach it SOCRATICALLY.
    """
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""
    You are Ashiesh Kapoor, a physics mentor who hates rote memorization and loves deep intuition.
    
    The Student is confused about: "{concept}"
    
    I have retrieved this relevant story/analogy from the archives:
    "{story_text}"
    
    YOUR TASK:
    Explain the concept to the student using this story.
    1. Do NOT start with definitions. Start with the story or the physical intuition.
    2. Be conversational, encouraging, and slightly philosophical (like a mentor).
    3. Use bolding for key 'aha!' moments.
    4. End with a reflective question to check their understanding.
    
    Keep it under 200 words.
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- UI LAYER ---
st.title("🧠 Exam Sense AI")
st.caption("The Intuition Engine | Prototype v0.2")

st.markdown("""
<style>
.big-font { font-size:20px !important; }
</style>
""", unsafe_allow_html=True)

query = st.text_input("What concept is confusing you?", placeholder="e.g. Why is euler's number useful?")

if query:
    with st.spinner("🔍 Searching the archives of intuition..."):
        collection = load_brain()
        results = collection.query(
            query_texts=[query],
            n_results=1
        )
        
        if results['documents'][0]:
            # 1. Retrieve
            raw_story = results['documents'][0][0]
            source = results['metadatas'][0][0]['source']
            
            # 2. Synthesize (The "Voice")
            with st.spinner("💡 Synthesizing insight..."):
                try:
                    explanation = generate_intuition(query, raw_story)
                    
                    # 3. Display
                    st.success("Insight Found!")
                    
                    st.markdown("### The Intuition")
                    st.markdown(f'<p class="big-font">{explanation}</p>', unsafe_allow_html=True)
                    
                    with st.expander(f"See Original Source ({source})"):
                        st.write(raw_story)
                        
                except Exception as e:
                    st.error(f"AI Error: {e}")
            
        else:
            st.warning("No specific intuition found for this. Try 'Derivative' or 'Neural Network'.")

# FOOTER
st.markdown("---")
st.caption("Built by Suleman | Powered by Gemini & ChromaDB")