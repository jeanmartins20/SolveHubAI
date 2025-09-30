import json
import google.generativeai as genai
from openai import OpenAI
from openai import APIError, AuthenticationError
from google.api_core import exceptions as google_exceptions

CONFIG_FILE_PATH = 'config.json'

with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- GOOGLE GEMINI ---
google_provider = next((p for p in config.get("AI_PROVIDERS", []) if p.get("provider") == "google"), None)
if google_provider:
    google_key = google_provider.get("api_key")
    if google_key:
        try:
            print("=== Modelos disponíveis na sua chave Google Gemini ===")
            genai.configure(api_key=google_key)
            for m in genai.list_models():
                print(m.name)
        except google_exceptions.PermissionDenied as e:
            print("Falha de autenticação no Google Gemini:", e)
        except Exception as e:
            print("Erro ao listar modelos Google Gemini:", e)
    else:
        print("Chave Google Gemini não configurada.")
else:
    print("Nenhum provedor Google Gemini encontrado no config.json")

print("\n")

# --- OPENAI ---
openai_provider = next((p for p in config.get("AI_PROVIDERS", []) if p.get("provider") == "openai"), None)
if openai_provider:
    openai_key = openai_provider.get("api_key")
    if openai_key:
        try:
            print("=== Modelos disponíveis na sua chave OpenAI ===")
            client = OpenAI(api_key=openai_key)
            models = client.models.list()
            for m in models.data:
                print(m.id)
        except AuthenticationError as e:
            print("Falha de autenticação na OpenAI:", e)
        except APIError as e:
            print("Erro na API OpenAI:", e)
        except Exception as e:
            print("Erro ao listar modelos OpenAI:", e)
    else:
        print("Chave OpenAI não configurada.")
else:
    print("Nenhum provedor OpenAI encontrado no config.json")
