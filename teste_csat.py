import requests
import json
import os

# --- CONFIGURAÇÃO ---
# O ID do ticket que você quer testar.
# Altere este número para o ticket que deseja consultar.
TICKET_ID_TO_TEST = "460467" 
# --------------------

CONFIG_FILE_PATH = 'config.json'

def load_credentials():
    """Lê as credenciais do Freshdesk a partir do arquivo config.json."""
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"❌ ERRO: Arquivo '{CONFIG_FILE_PATH}' não encontrado.")
        print("Certifique-se de que o arquivo de configuração está na mesma pasta que este script.")
        return None, None

    try:
        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        freshdesk_config = config.get("FRESHDESK", {})
        domain = freshdesk_config.get("domain")
        api_key = freshdesk_config.get("api_key")
        
        # Validação para garantir que as credenciais foram preenchidas
        if not domain or "seudominio" in domain or not api_key or "COLOQUE_SUA_CHAVE" in api_key:
            print("❌ ERRO: As credenciais do Freshdesk no arquivo 'config.json' não parecem estar preenchidas.")
            return None, None
            
        return domain, api_key
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ ERRO ao ler o arquivo de configuração: {e}")
        return None, None

def fetch_ticket_data(domain, api_key, ticket_id):
    """Busca e exibe os dados de um ticket específico do Freshdesk."""
    
    print(f"--- Buscando dados para o Ticket ID: {ticket_id} ---")
    
    # Monta a URL para o endpoint de um ticket específico
    url = f"https://{domain}/api/v2/tickets/{ticket_id}"
    
    # A autenticação da API do Freshdesk usa a chave como nome de usuário e 'X' como senha
    auth = (api_key, "X")

    try:
        # Realiza a chamada GET para a API
        response = requests.get(url, auth=auth, timeout=10)
        
        # Lança um erro para respostas com status 4xx (erro do cliente) ou 5xx (erro do servidor)
        response.raise_for_status()

        # Converte a resposta de texto JSON para um dicionário Python
        ticket_data = response.json()
        
        print("✅ Dados do ticket capturados com sucesso!\n")
        
        # Exibe o JSON completo de forma organizada
        print("--- Resposta Completa da API (JSON) ---")
        print(json.dumps(ticket_data, indent=2))
        print("--------------------------------------\n")
        
        # Exibe alguns campos importantes de forma mais direta
        print("--- Principais Dados do Ticket ---")
        print(f"Assunto: {ticket_data.get('subject')}")
        print(f"Status: {ticket_data.get('status')} (Lembre-se: 2=Aberto, 4=Resolvido, etc.)")
        print(f"Prioridade: {ticket_data.get('priority')}")
        print(f"Criado em: {ticket_data.get('created_at')}")
        print(f"ID do Solicitante: {ticket_data.get('requester_id')}")
        
        # Mostra como acessar um campo personalizado
        custom_fields = ticket_data.get('custom_fields', {})
        servico = custom_fields.get('cf_services', 'Não preenchido')
        print(f"Campo Personalizado 'Serviço': {servico}")
        print("--------------------------------\n")

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            print(f"❌ ERRO: Ticket com ID '{ticket_id}' não encontrado.")
        elif err.response.status_code in [401, 403]:
            print("❌ ERRO: Falha na autenticação. Verifique se sua API Key e Domínio estão corretos no 'config.json'.")
        else:
            print(f"❌ ERRO HTTP: Ocorreu um erro na requisição: {err}")
            
    except requests.exceptions.RequestException as err:
        print(f"❌ ERRO DE CONEXÃO: Não foi possível se conectar ao Freshdesk. Verifique sua rede.")
        print(f"   Detalhe: {err}")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    # 1. Carrega as credenciais
    freshdesk_domain, freshdesk_api_key = load_credentials()
    
    # 2. Se as credenciais foram carregadas com sucesso, busca o ticket
    if freshdesk_domain and freshdesk_api_key:
        fetch_ticket_data(freshdesk_domain, freshdesk_api_key, TICKET_ID_TO_TEST)