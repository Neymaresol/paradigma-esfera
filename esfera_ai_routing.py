"""Optional OpenAI intent routing. Never invent offers or expose API keys."""
import os
import re
import unicodedata
import httpx

FRONTS = ("educacao", "servicos", "comercio", "expansao")
TERMS = {
    "educacao": ("curso", "aprender", "estudar", "formacao", "certificacao", "aula", "treinamento"),
    "servicos": ("consultoria", "servico", "implementar", "automacao", "chatbot", "integracao"),
    "comercio": ("comprar", "preco", "placa", "computador", "ferramenta", "software", "produto"),
    "expansao": ("internacional", "mercado", "idioma", "parceria", "exportar", "empresa"),
}
def normalize(value):
    return "".join(c for c in unicodedata.normalize("NFKD", value.lower()) if not unicodedata.combining(c))
def fallback(query):
    q = normalize(query)
    matched = [front for front, words in TERMS.items() if any(re.search(r"\b"+re.escape(w)+r"\b",q) for w in words)]
    return {"theme":query.strip()[:120], "fronts":matched or ["educacao"], "engine":"keywords", "commercial_verified":False}
def classify(query):
    result = fallback(query)
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key or not query.strip():
        return result
    model = os.getenv("ESFERA_OPENAI_MODEL", "gpt-4.1-mini")
    try:
        response = httpx.post(
            "https://api.openai.com/v1/responses",
            headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},
            json={"model":model,"store":False,"max_output_tokens":160,
                  "instructions":"Classifique a intenção de busca de cursos e serviços. Responda SOMENTE com os nomes das frentes, separados por vírgula, escolhidos dentre: educacao, servicos, comercio, expansao. Nunca inclua ofertas ou links. Priorize educacao para interesse em cursos.",
                  "input":query[:120]},
            timeout=6.0,
        )
        response.raise_for_status()
        data=response.json()
        output=" ".join(item.get("text","") for part in data.get("output",[]) for item in part.get("content",[]) if item.get("type")=="output_text").lower()
        fronts=[front for front in FRONTS if re.search(r"\b"+front+r"\b",output)]
        if fronts:
            result["fronts"]=fronts
            result["engine"]="openai"
    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        pass
    return result
