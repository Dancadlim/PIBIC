import os
import glob

backend_dir = 'backend'
for filepath in glob.glob(os.path.join(backend_dir, '*.py')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace gemini-2.5 with 3.6
    content = content.replace('gemini-2.5-flash', 'gemini-3.6-flash')
    content = content.replace('gemini-2.5-pro', 'gemini-3.6-flash')

    # Add vertex config
    content = content.replace('client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))', 'os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex-key.json"\n        client = genai.Client(vertexai=True, project="plataformas-aulas-ufba", location="us-central1")')
    content = content.replace('client = genai.Client(api_key=self.api_key)', 'os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex-key.json"\n        client = genai.Client(vertexai=True, project="plataformas-aulas-ufba", location="us-central1")')
    content = content.replace('self.client = genai.Client(api_key=self.api_key)', 'os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex-key.json"\n        self.client = genai.Client(vertexai=True, project="plataformas-aulas-ufba", location="us-central1")')
    content = content.replace('client = genai.Client(api_key=api_key)', 'os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex-key.json"\n        client = genai.Client(vertexai=True, project="plataformas-aulas-ufba", location="us-central1")')
    content = content.replace('client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])', 'os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex-key.json"\n        client = genai.Client(vertexai=True, project="plataformas-aulas-ufba", location="us-central1")')


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")
