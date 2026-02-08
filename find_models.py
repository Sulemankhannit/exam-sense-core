import google.generativeai as genai
import os

# 1. Load the key manually (since we aren't in Streamlit)
# Open your secrets file to get the key
key = "YOUR KEY HERE"  # <--- PASTE YOUR KEY inside the quotes, find models supported by your free key

genai.configure(api_key=key)

print("Searching for available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
