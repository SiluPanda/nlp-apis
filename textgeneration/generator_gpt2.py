from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

