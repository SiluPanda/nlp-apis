from pydantic import BaseModel
from typing import Optional
from enum import Enum

class GenerateTextRequest(BaseModel):
    text_prompt: str
    max_len: Optional[int] = 20
    num_return_sequences: Optional[int] = 1

class GenerateTextReponse(BaseModel):
    generated_text: str

class TextGenerationJobStatus(Enum):
    IN_PROGRESS = 1
    COMPLETED = 2
