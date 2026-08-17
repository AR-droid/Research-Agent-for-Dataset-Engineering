from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Schemas for ResearchPlanner
class ResearchPlannerInput(BaseModel):
    objective: str = Field(..., description="The overall research objective")
    scope: Optional[str] = Field(None, description="Scope of the research")

class ResearchPlannerOutput(BaseModel):
    research_plan: str = Field(..., description="The generated research plan")
    tasks: List[str] = Field(..., description="List of tasks to execute")

# Schemas for ResearchDiscovery
class ResearchDiscoveryInput(BaseModel):
    task: str = Field(..., description="The specific discovery task to execute")
    queries: List[str] = Field(..., description="Search queries to use")

class ResearchDiscoveryOutput(BaseModel):
    discovered_sources: List[Dict[str, Any]] = Field(..., description="List of discovered sources with metadata")

# Schemas for SourceAnalyst
class SourceAnalystInput(BaseModel):
    source_url: str = Field(..., description="URL of the source to analyze")
    extraction_goal: str = Field(..., description="What to extract from the source")

class SourceAnalystOutput(BaseModel):
    extracted_information: List[Dict[str, Any]] = Field(..., description="Information extracted from the source")
    relevance_score: float = Field(..., description="Relevance score of the source to the goal")

# Schemas for EvidenceSynthesizer
class EvidenceSynthesizerInput(BaseModel):
    extracted_information: List[Dict[str, Any]] = Field(..., description="Information to synthesize")
    synthesis_goal: str = Field(..., description="Goal of the synthesis")

class EvidenceSynthesizerOutput(BaseModel):
    synthesized_evidence: str = Field(..., description="The synthesized evidence")
    claims: List[Dict[str, Any]] = Field(..., description="Claims generated from the evidence")

# Schemas for DatasetSchemaDesigner
class DatasetSchemaDesignerInput(BaseModel):
    research_objective: str = Field(..., description="The research objective")
    sample_data: List[Dict[str, Any]] = Field(..., description="Sample data to inform schema design")

class DatasetSchemaDesignerOutput(BaseModel):
    schema_definition: Dict[str, Any] = Field(..., description="The proposed JSON schema for the dataset")

# Schemas for DatasetBuilder
class DatasetBuilderInput(BaseModel):
    schema_definition: Dict[str, Any] = Field(..., description="The JSON schema to follow")
    claims: List[Dict[str, Any]] = Field(..., description="Claims to build records from")

class DatasetBuilderOutput(BaseModel):
    dataset_records: List[Dict[str, Any]] = Field(..., description="The generated dataset records")

# Schemas for DatasetQualityValidator
class DatasetQualityValidatorInput(BaseModel):
    dataset_records: List[Dict[str, Any]] = Field(..., description="Records to validate")
    schema_definition: Dict[str, Any] = Field(..., description="Schema to validate against")

class DatasetQualityValidatorOutput(BaseModel):
    is_valid: bool = Field(..., description="Whether the dataset is valid")
    errors: List[str] = Field(..., description="List of validation errors")

# Schemas for ProvenanceValidator
class ProvenanceValidatorInput(BaseModel):
    dataset_records: List[Dict[str, Any]] = Field(..., description="Records to validate for provenance")

class ProvenanceValidatorOutput(BaseModel):
    citations_valid: bool = Field(..., description="Whether all citations are valid")
    issues: List[Dict[str, Any]] = Field(..., description="Provenance issues found")

# Schemas for ResearchCritic
class ResearchCriticInput(BaseModel):
    research_plan: str = Field(..., description="The research plan to review")
    current_results: Dict[str, Any] = Field(..., description="Current results to review")

class ResearchCriticOutput(BaseModel):
    feedback: str = Field(..., description="Feedback on the research and results")
    suggestions: List[str] = Field(..., description="Suggestions for improvement")
