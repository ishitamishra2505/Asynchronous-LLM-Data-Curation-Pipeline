from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, Any, Optional

class BaseEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


from enum import Enum

# Our strict dropdown menu of allowed file types
class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MD = "md"
    HTML = "html"
    JSON = "json"
    CSV = "csv"
    URL = "url"


class Document(BaseEntity):
    title: str
    content: str
    source: str  # The file path or the website link
    doc_type: DocumentType  # Must be one of the choices from above!
    word_count: int
    char_count: int

class TextChunk(BaseEntity):
    document_id: UUID  # This is the reference tag linking back to the Document!
    content: str
    start_index: int
    end_index: int
    chunk_index: int
    token_count: int

class TaskType(str, Enum):
    QA_GENERATION = "qa_generation"
    CLASSIFICATION = "classification"
    SUMMARIZATION = "summarization"

class TaskTemplate(BaseEntity):
    name: str
    task_type: TaskType
    description: str
    prompt_template: str  # This is where your "what to do/what not to do" goes!
    parameters: dict      # Extra settings, like temperature or max word count

class QualityMetric(str, Enum):
    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    TOXICITY = "toxicity"
    BIAS = "bias"

class TaskResult(BaseEntity):
    task_id: UUID
    input_chunk_id: UUID
    output: str
    confidence: float
    quality_scores: dict  # This is where your accuracy and relevancy grades go!

class TrainingExample(BaseEntity):
    input_text: str
    output_text: str
    task_type: TaskType
    source_document_id: UUID

class Dataset(BaseEntity):
    name: str
    examples: list[TrainingExample] # A list holding all our perfect examples!