# 🧠 Exam Sense AI — The Intuition Engine  
> **“Don’t memorize. Understand.”**

---

## 🚀 What Is Exam Sense AI?

Exam Sense AI is **not** a traditional AI tutor.

It does **not** retrieve textbook paragraphs.

Instead, it retrieves *“Aha!” moments of discovery*.

This system is designed to teach physics and mathematics through **intuition, visualization, and guided reasoning** — not rote memorization.

At its core, Exam Sense AI is a **Retrieval-Augmented Generation (RAG)** engine that turns conceptual insights into Socratic-style explanations.

---

## ❤️ Core Philosophy (The *Why*)

Most AI tutors fail because they are trained on **textbooks**.

They start with definitions.

Humans don’t learn that way.

We learn by *seeing*, *feeling*, and *discovering*.

### The Guiding Principles

### 🧩 Math Is a Sense, Not a Language

Standard education treats math as symbols:


Exam Sense treats math as a **sense**, like sight or touch.

You first visualize the *moving machinery* of an idea.  
Only later do formulas appear.

---

### 🔍 Discovery Over Definition

Instead of giving rules upfront, the system presents contradictions that force understanding.

**Textbook:**
> Here is the formula for a limit.

**Exam Sense AI:**
> How can a car have speed at a single instant if time doesn’t pass?  
> That’s a contradiction.  
> So we must invent a new tool.

You *discover* the concept before naming it.

---

### 🎥 Code-Generated Intuition

The core intuition comes from programmatically generated mathematical animations (not hand-drawn illustrations).

This ensures:

- Mathematical rigor  
- Precise geometry  
- Reproducible visual reasoning  

---

## 🧠 How It Works

Exam Sense AI uses:

- Semantic search to retrieve **atomic intuition cards**
- A Large Language Model (Google Gemini)
- Socratic synthesis to build explanations

This creates a learning flow like:


Not the reverse.

---

## 🏗 Architecture

This is a **full ETL + RAG pipeline**, not a wrapper.

### Pipeline

1. **Extract** — Scrape intuition-rich educational sources
2. **Transform** — Clean + chunk into conceptual units
3. **Load** — Embed into vector space
4. **Retrieve** — Semantic search
5. **Generate** — Gemini synthesizes dialogue

---

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **LLM:** Google Gemini (`google-generativeai`)
- **Vector Database:** ChromaDB
- **Embeddings:** Sentence Transformers (HuggingFace)
- **Frontend:** Streamlit

---

Yep — your Markdown broke because multiple sections got merged into one code block and headings lost their structure.

Here’s the **fixed, clean, copy-paste-ready LAST PART** starting from **Installation & Setup onward** — just replace everything from `## 🚀 Installation & Setup` downward with this:

---

````markdown
## 🚀 Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/Sulemankhannit/exam-sense-core.git
cd exam-sense-core
````

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Secrets

Create this file:

```
.streamlit/secrets.toml
```

Add your Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"
```

---

### 4. (Optional) Build the Brain From Scratch

```bash
# Extract raw data
python miner.py

# Clean + chunk
python refinery.py

# Create embeddings
python engine.py
```

---

### 5. Run the App

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
data/        → Raw text + ChromaDB indexes

miner.py     → Extraction layer
refinery.py  → Transformation (cleaning + chunking)
engine.py    → Embedding + indexing
app.py       → Streamlit UI + RAG logic
```

---

## 🔮 Future Roadmap

* [ ] Add Feynman Lectures as a data source
* [ ] Quiz mode for active recall
* [ ] LaTeX rendering for equations
* [ ] Cloud vector DB (Pinecone / equivalent)
* [ ] Behavioral diagnostics (JEE Doctor)

---

## 🤝 Credits

**Core intuition source:** 3Blue1Brown open educational content

**Developed by:** Suleman Khan

```

