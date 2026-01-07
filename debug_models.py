import google.generativeai as genai
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyC2308grwzzyhpyySy8WUCCuEe3zMmHf4M"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("Listing EMBEDDING models...")
try:
    for m in genai.list_models():
        if "embedContent" in m.supported_generation_methods:
            print(f"Name: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
