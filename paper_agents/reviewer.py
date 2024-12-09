import pathlib
import logging
from openai import OpenAI
from typing import Dict

def review(config: Dict, output_dir: pathlib.Path):
    sources = config["sources"]
    bibtex = config["bibtex"]
    model = config["model"]
    client = OpenAI()

    context = "<<<begin>>>\n\n"
    for source in map(pathlib.Path, sources):
        with open(source, "r") as f:
            text = f.read()
        
        context += f"{source.name}\n{text}\n\n"
    
    for reviewer_id, reviewer_desc in enumerate(config["reviewers"]):
        logging.info(f"Generating review for reviewer {reviewer_id}...")
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"{config["prompt"]} {context}\n\n <<<end>>> \n\n {reviewer_desc}, now generate your review: "}
            ],
        )

        review = completion.choices[0].message.content
        with open(output_dir / f"reviewer_{reviewer_id}.txt", "w") as f:
            f.write(review)
