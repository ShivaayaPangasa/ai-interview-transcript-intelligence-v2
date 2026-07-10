from transformers import GPT2LMHeadModel
from transformers import GPT2TokenizerFast

import torch
import math


print("Loading GPT-2 model...")

tokenizer = GPT2TokenizerFast.from_pretrained(
    "gpt2"
)

model = GPT2LMHeadModel.from_pretrained(
    "gpt2"
)

model.eval()


def calculate_perplexity(text):

    if not text.strip():
        return 0

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model(
            **inputs,
            labels=inputs["input_ids"]
        )

    loss = outputs.loss

    perplexity = math.exp(
        loss.item()
    )

    return round(
        perplexity,
        2
    )