import openai
import logging
import pathlib
from typing import Dict

def revise(config: Dict, output_dir: pathlib.Path):
    sources = config["sources"]
    bibtex = config["bibtex"]
    model = config["model"]
    client = OpenAI()

    context = "<<<begin>>>\n\n"
    for source in map(pathlib.Path, sources):
        with open(source, "r") as f:
            text = f.read()
        
        context += f"{source.name}\n{text}\n\n"
    
    for reviewer_id in enumerate(config["reviewers"]):
        with open(output_dir / f"reviewer_{reviewer_id}.txt", "r") as f:
            review = f.read()
        
        context += f"reviewer_{reviewer_id}\n{review}\n\n"

    revisioner_role = r"""You should address the comments from the reviewers, make sure you address all the comments, and make sure your revision is clear and easy to understand. Your generation should contain a section starts with ```latex and ends with ``` to indicate the revised latex file. When you need more inputs from the authors, please leave a highlighted note for the authors (use some color and starts with "Notes(AI):"). When you are not confident about some revision, please leave a highlighted note for suggested revision (use some color and starts with "Suggestion(AI):"). """

    for source in map(pathlib.Path, sources):
        logging.info(f"Generating revised tex file for {source}...")

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"{config["prompt"]} {context}\n\n <<<end>>> \n\n {revisioner_role} now please revise the tex file {source.name}: "}
            ],
        )

        revised_text = completion.choices[0].message.content

        revised_text = revised_text.split("```latex")[1].split("```")[0].strip()

        output_file_path = output_dir / source
        output_file_dir = output_file_path.parent

        if not output_file_dir.exists():
            output_file_dir.mkdir(parents=True)
        
        with open(output_file_path, "w") as f:
            f.write(revised_text)
