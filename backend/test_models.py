import os
import re
from google import genai

path = os.path.join('.streamlit', 'secrets.toml')
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        for linha in f:
            if 'GEMINI_API_KEY' in linha:
                m = re.search(r'GEMINI_API_KEY\s*=\s*["\'](.*?)["\']', linha)
                if m:
                    os.environ['GEMINI_API_KEY'] = m.group(1).strip()

api_key = os.environ.get('GEMINI_API_KEY')
print("API Key status:", "FOUND" if api_key else "NOT FOUND")

if api_key:
    # 1. Test Developer API client
    print("\n--- Testing Developer API (api_key) ---")
    try:
        client = genai.Client(api_key=api_key)
        res = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents='Responda apenas com: OK Funciona'
        )
        print("Developer API gemini-3.5-flash-lite SUCCESS:", res.text.strip())
    except Exception as e:
        print("Developer API gemini-3.5-flash-lite FAIL:", e)

    # 2. Test Vertex AI client
    print("\n--- Testing Vertex AI (vertexai=True) ---")
    try:
        client_v = genai.Client(vertexai=True, location='us-central1')
        res = client_v.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents='Responda apenas com: OK Funciona'
        )
        print("Vertex AI gemini-3.5-flash-lite SUCCESS:", res.text.strip())
    except Exception as e:
        print("Vertex AI gemini-3.5-flash-lite FAIL:", e)
