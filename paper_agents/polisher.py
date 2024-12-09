import pathlib
import logging
from openai import OpenAI
from typing import Dict

def polish(config: Dict, output_dir: pathlib.Path):
    sources = config["sources"]
    bibtex = config["bibtex"]
    model = config["model"]
    client = OpenAI()

    context = "<<<begin>>>\n\n"
    for source in map(pathlib.Path, sources):
        with open(source, "r") as f:
            text = f.read()
        
        context += f"{source.name}\n{text}\n\n"
    
    polisher_role = r"""You should spell check and grammar check the tex file, you should improve the coherence of the text, and make sure the text is clear and easy to understand. Your generation should contain a section starts with ```latex and ends with ``` to indicate the polished latex file. Please do not remove any content, only polish the text. """

    for source in map(pathlib.Path, sources):
        logging.info(f"Generating polished tex file for {source}...")

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"{config["prompt"]} {context}\n\n <<<end>>> \n\n {polisher_role} now please polish the tex file {source.name}: "}
            ],
        )

        polished_text = completion.choices[0].message.content

        polished_text = polished_text.split("```latex")[1].split("```")[0].strip()

        output_file_path = output_dir / source
        output_file_dir = output_file_path.parent

        if not output_file_dir.exists():
            output_file_dir.mkdir(parents=True)

        with open(output_file_path, "w") as f:
            f.write(polished_text)
