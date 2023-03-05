from fastapi import APIRouter, BackgroundTasks, HTTPException
from .models import GenerateTextReponse, GenerateTextRequest, TextGenerationJobStatus
from .generator_gpt2 import generator
from typing import List, Dict, Tuple
import uuid

router_v1 = APIRouter(
    prefix="/v1"
)

DB: Dict[str, Tuple[str, List[GenerateTextReponse]]] = {}


def generate_text(text_generation_id: str, text_generation_request: GenerateTextRequest) -> List[GenerateTextReponse]:
    DB[text_generation_id] = (TextGenerationJobStatus.IN_PROGRESS.name, [])
    text_generations = []
    generations = generator(text_generation_request.text_prompt,
                                           max_length=text_generation_request.max_len,
                                           num_return_sequences=text_generation_request.num_return_sequences)
    for generation in generations:
        text_generations.append(GenerateTextReponse(generated_text=generation['generated_text']))
    DB[text_generation_id] = (TextGenerationJobStatus.COMPLETED.name, text_generations)


@router_v1.post('/generatetext')
def trigger_generate_text(text_generation_request: GenerateTextRequest, background_tasks: BackgroundTasks):
    text_generation_id = str(uuid.uuid4())
    background_tasks.add_task(generate_text, text_generation_id, text_generation_request)
    return {
        "id": text_generation_id
    }

@router_v1.get('/generatetext/{id}')
def get_text(id: str) -> Tuple[str, List[GenerateTextReponse]]:
    if id not in DB:
        raise HTTPException(404, detail='Provided ID is not present')
    return DB[id]
