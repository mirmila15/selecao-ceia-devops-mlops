from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional # Removido o 'tuple' daqui
import time
import logging

# Definimos os tipos para o Pylance e o Python 3.9
CategoriasLiterais = Literal["pergunta", "relato", "reclamacao"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mini-text-service")

app = FastAPI(title="Mini Text Service", version="1.0.0")

class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    strategy: Optional[Literal["rules"]] = "rules"

class ClassifyResponse(BaseModel):
    category: CategoriasLiterais
    confidence: float
    strategy: str
    elapsed_ms: int
    model_version: str 

@app.get("/health")
def health():
    return {"status": "ok"}

# Em Python 3.9+, usamos o tuple minúsculo direto aqui sem importar
def classify_rules(text: str) -> tuple[CategoriasLiterais, float]:
    t = text.strip().lower()
    if "?" in t or t.startswith(("como ", "por que ", "pq ", "qual", "quais ")):
        return "pergunta", 0.85
    if any(k in t for k in ["não funciona", "erro", "ruim", "problema", "insatisfeito", "reclama"]):
        return "reclamacao", 0.75
    return "relato", 0.60

@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    start = time.time()
    text = (req.text or "").strip()
    
    if not text:
        raise HTTPException(status_code=400, detail="text must be non-empty")
    if req.strategy != "rules":
        raise HTTPException(status_code=400, detail="unsupported strategy")
    
    category, confidence = classify_rules(text)
    elapsed_ms = int((time.time() - start) * 1000)
    
    logger.info(f"text='{text[:30]}...' category={category}")
    
    return ClassifyResponse(
        category=category,
        confidence=confidence,
        strategy=str(req.strategy),
        elapsed_ms=elapsed_ms,
        model_version="v1-heuristics"
    )