from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional, tuple
import time
import logging

# 1. Definimos o tipo aqui para o Pylance não se perder
CategoriasLiterais = Literal["pergunta", "relato", "reclamacao"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mini-text-service")

app = FastAPI(title="Mini Text Service", version="1.0.0") [cite: 88]

class ClassifyRequest(BaseModel): [cite: 89]
    text: str = Field(..., min_length=1, max_length=2000) [cite: 90]
    strategy: Optional[Literal["rules"]] = "rules" [cite: 90]

class ClassifyResponse(BaseModel): [cite: 91]
    category: CategoriasLiterais [cite: 92]
    confidence: float [cite: 92]
    strategy: str [cite: 93]
    elapsed_ms: int [cite: 94]
    model_version: str 

@app.get("/health") [cite: 95]
def health(): [cite: 96]
    return {"status": "ok"} [cite: 97]

# Ajustamos a função para retornar explicitamente o tipo correto
def classify_rules(text: str) -> tuple[CategoriasLiterais, float]: [cite: 109]
    t = text.strip().lower()
    if "?" in t or t.startswith(("como ", "por que ", "pq ", "qual", "quais ")):
        return "pergunta", 0.85 [cite: 111, 112]
    if any(k in t for k in ["não funciona", "erro", "ruim", "problema", "insatisfeito", "reclama"]): [cite: 113, 114]
        return "reclamacao", 0.75 [cite: 115]
    return "relato", 0.60 [cite: 116]

@app.post("/classify", response_model=ClassifyResponse) [cite: 121]
def classify(req: ClassifyRequest): [cite: 122]
    start = time.time() [cite: 122]
    text = (req.text or "").strip() [cite: 123]
    
    if not text:
        raise HTTPException(status_code=400, detail="text must be non-empty") [cite: 124]
    if req.strategy != "rules": [cite: 125]
        raise HTTPException(status_code=400, detail="unsupported strategy") [cite: 126]
    
    category, confidence = classify_rules(text) [cite: 127]
    elapsed_ms = int((time.time() - start) * 1000) [cite: 127, 130]
    
    logger.info(f"text='{text[:30]}...' category={category}")
    
    return ClassifyResponse(
        category=category,
        confidence=confidence,
        strategy=str(req.strategy), # Forçamos para string para o Pylance aceitar
        elapsed_ms=elapsed_ms,
        model_version="v1-heuristics"
    ) [cite: 129]