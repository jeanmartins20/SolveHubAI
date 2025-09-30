# SolveHubAI
SolveHub é uma aplicação de desktop robusta, desenvolvida em Python com Tkinter, projetada para otimizar o fluxo de trabalho de equipes de suporte técnico. 

============================================================
                SolveHub - Sistema de Gestão de Tickets
============================================================

DESCRIÇÃO GERAL
---------------
O SolveHub é uma aplicação desktop em Python (Tkinter) para gestão e análise de tickets,
integração com Freshdesk e uso de Inteligência Artificial (Google Gemini e OpenAI GPT).
O sistema permite importar tickets, gerar relatórios, analisar satisfação de clientes (CSAT)
e muito mais.

ESTRUTURA DO PROJETO
--------------------
- appteste.py        -> Aplicação principal
- config.json        -> Configuração de chaves e parâmetros
- test_api_keys.py   -> Teste de chaves de API
- test_list_models.py-> Listagem de modelos de IA disponíveis
- teste_csat.py      -> Teste de integração Freshdesk/CSAT
- SolveHub_Log.log   -> Arquivo de log gerado automaticamente
- Assets/            -> Pasta de ícones e imagens (se necessário)

INSTALAÇÃO
----------
1. Instale as dependências necessárias:
   pip install -r requirements.txt

2. Configure o arquivo config.json com suas chaves de API.

3. Execute o programa principal:
   python appteste.py

CONFIGURAÇÃO (config.json)
--------------------------
{
  "API_KEYS": {
    "web_search_api_key": "SUA_CHAVE_SERPAPI"
  },
  "FRESHDESK": {
    "api_key": "SUA_CHAVE_FRESHDESK",
    "domain": "seudominio.freshdesk.com"
  },
  "AI_PROVIDERS": [
    {
      "provider": "google",
      "api_key": "SUA_CHAVE_GOOGLE_GEMINI",
      "model": "gemini-1.5-flash"
    },
    {
      "provider": "openai",
      "api_key": "SUA_CHAVE_OPENAI",
      "model": "gpt-4o"
    }
  ]
}

ONDE OBTER AS CHAVES
--------------------
- Freshdesk: Painel do usuário -> API Key
- Google Gemini: https://aistudio.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys
- SerpAPI: https://serpapi.com/manage-api-key

SCRIPTS DE TESTE
----------------
- test_api_keys.py   -> Testa chaves configuradas
- test_list_models.py-> Lista modelos IA disponíveis
- teste_csat.py      -> Busca ticket específico do Freshdesk

BANCOS DE DADOS
---------------
- tickets.db -> Armazena tickets e satisfação
- users.db   -> Armazena contas de usuário

LICENÇA
-------
Uso interno. Ajuste conforme sua organização.

============================================================
