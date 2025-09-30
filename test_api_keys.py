import json
import requests
import google.generativeai as genai
from openai import OpenAI, APIError, AuthenticationError
from google.api_core import exceptions as google_exceptions

CONFIG_FILE_PATH = 'config.json'

with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

WEB_SEARCH_API_KEY = config.get("API_KEYS", {}).get("web_search_api_key", "")
FRESHDESK_API_KEY = config.get("FRESHDESK", {}).get("api_key", "")
FRESHDESK_DOMAIN = config.get("FRESHDESK", {}).get("domain", "")
AI_PROVIDERS = config.get("AI_PROVIDERS", [])

def test_all_api_keys():
    """Lista todas as chaves presentes no config.json."""
    results = []
    # API_KEYS genéricas
    for name, key in config.get("API_KEYS", {}).items():
        if not key or key.startswith("COLOQUE"):
            results.append(f"{name}: chave não configurada.")
        else:
            results.append(f"{name}: chave presente.")
    # Freshdesk
    if not FRESHDESK_API_KEY or FRESHDESK_API_KEY.startswith("COLOQUE"):
        results.append("Freshdesk: chave não configurada.")
    else:
        results.append("Freshdesk: chave presente.")
    # AI Providers
    for provider in AI_PROVIDERS:
        name = provider.get("provider")
        key = provider.get("api_key")
        if not key or key.startswith("SUA_CHAVE") or key.startswith("COLOQUE"):
            results.append(f"{name}: chave não configurada.")
        else:
            results.append(f"{name}: chave presente.")
    return "\n".join(results)

def test_web_search():
    """Teste simples para SerpAPI/GoogleSearch."""
    if not WEB_SEARCH_API_KEY or WEB_SEARCH_API_KEY.startswith("COLOQUE"):
        return "Web Search API: chave não configurada."
    try:
        from serpapi import GoogleSearch
        params = {
            "q": "OpenAI",
            "api_key": WEB_SEARCH_API_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        if "error" in results:
            return f"Web Search API ERRO: {results['error']}"
        return "Web Search API OK."
    except Exception as e:
        return f"Web Search API Falhou: {e}"

def test_freshdesk():
    if not FRESHDESK_API_KEY or FRESHDESK_API_KEY.startswith("COLOQUE"):
        return "Freshdesk: chave não configurada."
    try:
        url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets"
        r = requests.get(url, auth=(FRESHDESK_API_KEY, "X"))
        if r.status_code == 200:
            return "Freshdesk API OK."
        return f"Freshdesk API Falhou. Status {r.status_code} - {r.text}"
    except Exception as e:
        return f"Freshdesk API Falhou: {e}"

def test_ai_providers():
    results = []
    for provider in AI_PROVIDERS:
        name = provider.get("provider")
        key = provider.get("api_key")
        model = provider.get("model")
        if not key or key.startswith("SUA_CHAVE") or key.startswith("COLOQUE"):
            results.append(f"{name}: chave não configurada.")
            continue
        try:
            if name == "google":
                genai.configure(api_key=key)
                model_obj = genai.GenerativeModel(model)
                # prompt curto para não gastar muito
                resp = model_obj.generate_content("Diga 'ok'").text
                results.append(f"Google Gemini OK: {resp[:30]}...")
            elif name == "openai":
                client = OpenAI(api_key=key)
                resp = client.chat.completions.create(
                    model=model,
                    messages=[{"role":"user","content":"Diga 'ok'"}]
                )
                results.append(f"OpenAI OK: {resp.choices[0].message.content[:30]}...")
        except (google_exceptions.PermissionDenied, AuthenticationError) as e:
            results.append(f"{name} - Falha de autenticação: {e} \n")
        except (google_exceptions.ResourceExhausted, APIError) as e:
            results.append(f"{name} - Cota excedida: {e} \n")
        except Exception as e:
            results.append(f"{name} - Erro genérico: {e} \n")
    return "\n".join(results)

if __name__ == "__main__":
    print("== Teste das Chaves Configuradas ==")
    print(test_all_api_keys())
    print("\n== Teste Web Search ==")
    print(test_web_search())
    print("\n== Teste Freshdesk ==")
    print(test_freshdesk())
    print("\n== Teste Provedores de IA ==")
    print(test_ai_providers())
