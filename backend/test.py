import google.generativeai as genai

genai.configure(api_key="AIzaSyB_hbMrBbB4-O4sHuMWd1e6AFlYzgOtoZs")

for m in genai.list_models():
    print(m.name)