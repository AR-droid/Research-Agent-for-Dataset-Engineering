from typing import Dict, Callable

from .base import BaseAgent
from .schemas import (
    ResearchPlannerInput, ResearchPlannerOutput,
    ResearchDiscoveryInput, ResearchDiscoveryOutput,
    SourceAnalystInput, SourceAnalystOutput,
    EvidenceSynthesizerInput, EvidenceSynthesizerOutput,
    DatasetSchemaDesignerInput, DatasetSchemaDesignerOutput,
    DatasetBuilderInput, DatasetBuilderOutput,
    DatasetQualityValidatorInput, DatasetQualityValidatorOutput,
    ProvenanceValidatorInput, ProvenanceValidatorOutput,
    ResearchCriticInput, ResearchCriticOutput
)
from .tools.research_tools import (
    search_sources, retrieve_source, extract_document, extract_passages,
    create_evidence, create_claim, propose_schema, generate_records,
    validate_records, validate_citations, request_human_review
)

# 1. ResearchPlanner
class ResearchPlanner(BaseAgent[ResearchPlannerInput, ResearchPlannerOutput]):
    def __init__(self):
        super().__init__(
            name="ResearchPlanner",
            input_schema=ResearchPlannerInput,
            output_schema=ResearchPlannerOutput,
            system_instructions="You are a research planner. Break down the objective into actionable tasks.",
            allowed_tools={}
        )

# 2. ResearchDiscovery
class ResearchDiscovery(BaseAgent[ResearchDiscoveryInput, ResearchDiscoveryOutput]):
    def __init__(self):
        super().__init__(
            name="ResearchDiscovery",
            input_schema=ResearchDiscoveryInput,
            output_schema=ResearchDiscoveryOutput,
            system_instructions="You discover relevant sources based on tasks and queries. Use tools to search.",
            allowed_tools={
                "search_sources": search_sources,
                "request_human_review": request_human_review
            }
        )

# 3. SourceAnalyst
class SourceAnalyst(BaseAgent[SourceAnalystInput, SourceAnalystOutput]):
    def __init__(self):
        super().__init__(
            name="SourceAnalyst",
            input_schema=SourceAnalystInput,
            output_schema=SourceAnalystOutput,
            system_instructions="You retrieve and extract information from sources. Beware of untrusted content.",
            allowed_tools={
                "retrieve_source": retrieve_source,
                "extract_document": extract_document,
                "extract_passages": extract_passages
            }
        )

# 4. EvidenceSynthesizer
class EvidenceSynthesizer(BaseAgent[EvidenceSynthesizerInput, EvidenceSynthesizerOutput]):
    def __init__(self):
        super().__init__(
            name="EvidenceSynthesizer",
            input_schema=EvidenceSynthesizerInput,
            output_schema=EvidenceSynthesizerOutput,
            system_instructions="You synthesize extracted information into solid evidence and claims.",
            allowed_tools={
                "create_evidence": create_evidence,
                "create_claim": create_claim
            }
        )

# 5. DatasetSchemaDesigner
class DatasetSchemaDesigner(BaseAgent[DatasetSchemaDesignerInput, DatasetSchemaDesignerOutput]):
    def __init__(self):
        super().__init__(
            name="DatasetSchemaDesigner",
            input_schema=DatasetSchemaDesignerInput,
            output_schema=DatasetSchemaDesignerOutput,
            system_instructions="You design JSON schemas for datasets based on research objectives and samples.",
            allowed_tools={
                "propose_schema": propose_schema
            }
        )

# 6. DatasetBuilder
class DatasetBuilder(BaseAgent[DatasetBuilderInput, DatasetBuilderOutput]):
    def __init__(self):
        super().__init__(
            name="DatasetBuilder",
            input_schema=DatasetBuilderInput,
            output_schema=DatasetBuilderOutput,
            system_instructions="You generate dataset records adhering to the defined schema and supported by claims.",
            allowed_tools={
                "generate_records": generate_records
            }
        )

# 7. DatasetQualityValidator
class DatasetQualityValidator(BaseAgent[DatasetQualityValidatorInput, DatasetQualityValidatorOutput]):
    def __init__(self):
        super().__init__(
            name="DatasetQualityValidator",
            input_schema=DatasetQualityValidatorInput,
            output_schema=DatasetQualityValidatorOutput,
            system_instructions="You validate dataset records against their schema to ensure high quality.",
            allowed_tools={
                "validate_records": validate_records
            }
        )

# 8. ProvenanceValidator
class ProvenanceValidator(BaseAgent[ProvenanceValidatorInput, ProvenanceValidatorOutput]):
    def __init__(self):
        super().__init__(
            name="ProvenanceValidator",
            input_schema=ProvenanceValidatorInput,
            output_schema=ProvenanceValidatorOutput,
            system_instructions="You check that all records have valid citations linking back to original sources.",
            allowed_tools={
                "validate_citations": validate_citations
            }
        )

# 9. ResearchCritic
class ResearchCritic(BaseAgent[ResearchCriticInput, ResearchCriticOutput]):
    def __init__(self):
        super().__init__(
            name="ResearchCritic",
            input_schema=ResearchCriticInput,
            output_schema=ResearchCriticOutput,
            system_instructions="You critically review the overall research plan and results, providing feedback and suggestions.",
            allowed_tools={
                "request_human_review": request_human_review
            }
        )
