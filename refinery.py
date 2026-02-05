import json
import re
import os

# CONFIG
INPUT_FILE = os.path.join("data", "raw", "3b1b_intuition_gold.json")
OUTPUT_FILE = os.path.join("data", "processed", "ashish_kapoor_brain.json")

def clean_text(text):
    # Remove markdown image links like ![](...)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def chunk_content(lesson_title, raw_text):
    """
    Splits a lesson into atomic chunks based on Markdown headers (##).
    """
    chunks = []
    # Split by "## " (Header 2) or "# " (Header 1) to catch main titles too
    sections = re.split(r'(^|\n)#{1,2}\s+', raw_text)
    
    for section in sections:
        if not section or not section.strip():
            continue
            
        # The first line is usually the section title
        lines = section.strip().split('\n')
        header_title = lines[0].strip()
        body = "\n".join(lines[1:])
        
        if len(body) < 50: # Skip empty/tiny sections
            continue
            
        # Create a Unique ID
        chunk_id = f"{lesson_title} - {header_title}"
        
        chunks.append({
            "id": chunk_id,
            "lesson": lesson_title,
            "topic": header_title,
            "content": clean_text(body),
            "type": "story_analogy"
        })
        
    return chunks

def run_refinery():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_lessons = json.load(f)
        
    knowledge_base = []
    seen_ids = set() # Safety tracker
    
    print(f"[*] Refining {len(raw_lessons)} raw lessons...")
    
    for lesson in raw_lessons:
        # INTELLIGENT NAMING:
        # If filename is 'index.mdx', use the parent folder name (e.g., '3d-transformations')
        if 'index' in lesson['filename'].lower():
            # Extract parent folder from path
            # Windows path fix: handle both / and \
            clean_path = lesson['path'].replace('\\', '/')
            path_parts = clean_path.split('/')
            # Parent is usually -2 (file is -1)
            if len(path_parts) > 1:
                title = path_parts[-2]
            else:
                title = "Unknown_Lesson"
        else:
            title = lesson['filename']
            
        # Clean title formatting
        title = title.replace('.mdx', '').replace('.md', '').replace('-', ' ').title()
        
        # Chunk it
        lesson_chunks = chunk_content(title, lesson['content'])
        
        # Deduplication check
        for chunk in lesson_chunks:
            if chunk['id'] not in seen_ids:
                knowledge_base.append(chunk)
                seen_ids.add(chunk['id'])
        
    print(f"[+] Created {len(knowledge_base)} atomic intuition cards.")
    
    # Save the Brain
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
        
    print(f"[SUCCESS] Brain saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_refinery()