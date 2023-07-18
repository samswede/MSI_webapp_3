from pydantic import BaseModel
from typing import List, Dict

# Define a Pydantic model for diseases, drugs, and GraphRequest
class Disease(BaseModel):
    value: str
    name: str

class Drug(BaseModel):
    value: str
    name: str

class DiseaseDrugCandidatesRequest(BaseModel):
    disease_label: str

class GraphRequest(BaseModel):
    disease_label: str
    drug_label: str
    k1: int
    k2: int
