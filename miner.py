import os
import re
import json

# CONFIGURATION
SOURCE_DIR = os.path.join("data", "raw", "3Blue1Brown.com")
OUTPUT_FILE = "data/raw/3b1b_intuition_gold.json"

def clean_mdx_content(text):
    """
    Strips code, imports, and metadata to leave only the 'Ashish Kapoor' style text.
    """
    # 1. Remove imports (e.g., import { ... } from ...)
    text = re.sub(r'import\s+.*?from\s+.*?;', '', text, flags=re.DOTALL)
    
    # 2. Remove metadata blocks (lines between ---)
    text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
    
    # 3. Remove React components/HTML tags (e.g., <Lesson ...>, </div>)
    # We keep the content inside, just remove the tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # 4. Remove LaTeX delimiters (optional, but keeps reading cleaner)
    # Keeping them for now as they are math context
    
    # 5. Clean up extra whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return "\n".join(lines)

def mine_directory(root_dir):
    extracted_data = []
    
    print(f"[*] Mining {root_dir} for gold...")
    
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            # Look for Markdown or MDX files
            if file.endswith(('.md', '.mdx')):
                filepath = os.path.join(subdir, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        raw_content = f.read()
                        
                    # Extract the gold
                    cleaned_text = clean_mdx_content(raw_content)
                    
                    # Only save if we found substantial text (not just a config file)
                    if len(cleaned_text) > 200:
                        entry = {
                            "source": "3Blue1Brown",
                            "filename": file,
                            "path": filepath,
                            "content": cleaned_text[:2000] + "..." # Truncating for preview, remove this slice for full extraction
                        }
                        extracted_data.append(entry)
                        print(f"  [+] Found Gold: {file} ({len(cleaned_text)} chars)")
                        
                except Exception as e:
                    print(f"  [!] Error reading {file}: {e}")

    return extracted_data

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    data = mine_directory(SOURCE_DIR)
    
    # Dump to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"\n[SUCCESS] Extracted {len(data)} intuition lessons.")
    print(f"[SAVED] Gold stored in: {OUTPUT_FILE}")