import pathlib
import logging
from openai import OpenAI
from typing import Dict

def sanitize(config: Dict, output_dir: pathlib.Path):
    sources = config["sources"]
    bibtex = config["bibtex"]
    model = config["model"]
    client = OpenAI()

    context = "<<<begin>>>\n\n"
    for source in map(pathlib.Path, sources):
        with open(source, "r") as f:
            text = f.read()
        
        context += f"{source.name}\n{text}\n\n"
    
    with open(bibtex, "r") as f:
        bibtex = f.read()
    
    if not output_dir.exists():
        output_dir.mkdir()

    context += f"bibtex\n{bibtex}\n\n"
    
    sanitizer_role = r"""You should also check the format of the latex file, each cite reference should be ~\cite{...}, make sure that all references are in the correct format, and make sure there is not invalid reference. The bibtex is provided to you for cross-checking, if you are confident about some error fix, just fix them directly, otherwise, please leave a highlighted note for suggested fix (use use some color and starts with "Suggestion(AI):"). Your generation should contain a section starts with ```latex and ends with ``` to indicate the sanitized latex file. """

    for source in map(pathlib.Path, sources):
        logging.info(f"Generating sanitized tex file for {source}...")
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"{config["prompt"]} {context}\n\n <<<end>>> \n\n {sanitizer_role} now let's sanitize the tex file {source.name}: "}
            ],
        )
        sanitized_text = completion.choices[0].message.content

        # parse the sanitized text and save it to the output directory
        sanitized_text = sanitized_text.split("```latex")[1].split("```")[0].strip()

        output_file_path = output_dir / source
        output_file_dir = output_file_path.parent

        if not output_file_dir.exists():
            output_file_dir.mkdir(parents=True)

        with open(output_file_path, "w") as f:
            f.write(sanitized_text)
