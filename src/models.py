from pydantic import BaseModel, Field
from typing import List

class ProductInput(BaseModel):
    disease: str
    intended_use: str
    biomarkers: List[str] = Field(default_factory=list)
    therapy_linked: bool
    specimen_type: str
    platform: str
    software_involved: bool

class ProductClassification(BaseModel):
    product_type: str
    likely_cdx: bool
    likely_tumor_profiling: bool
    likely_investigational_use: bool
    rationale: str

class RegulatoryAssessment(BaseModel):
    probable_route: str
    evidence_gaps: List[str]
    key_risks: List[str]
    next_steps: List[str]
    summary: str

class MemoOutput(BaseModel):
    title: str
    executive_summary: str
    product_assessment: str
    evidence_gaps: List[str]
    recommended_actions: List[str]
    citations: List[str]
