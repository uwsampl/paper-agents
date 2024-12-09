import argparse
import json
import os
import pathlib
import logging
from .polisher import polish
from .sanitizer import sanitize
from .reviewer import review
from .revisioner import revise

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

agents = {
    "polish": polish,
    "sanitize": sanitize,
    "review": review,
    "revise": revise,
}

parser = argparse.ArgumentParser("Paper writing agents.")
parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration file.")
parser.add_argument("--output_dir", type=str, default="tmp", help="Path to the output directory.")
parser.add_argument("--role", type=str, default="sanitizer", help="Role of the agent.")
parser.add_argument("--apply", action="store_true", help="Apply the changes.")
parser.add_argument("--undo", action="store_true", help="Undo the changes.")
args = parser.parse_args()

if args.apply and args.undo:
    raise ValueError("Cannot apply and undo at the same time.")

with open(args.config, "r") as f:
    config = json.load(f)

output_dir = pathlib.Path(args.output_dir)

if args.undo:
    for source in map(pathlib.Path, config["sources"]):
        patch_file = pathlib.Path(f"{source}.patch")
        if patch_file.exists():
            logging.info(f"Undoing changes for {source}...")
            os.system(f"patch -R {source} < {patch_file}")
            # remove the patch file
            patch_file.unlink()
        else:
            logging.info(f"No changes to undo for {source}.")
else:
    # empty the output directory
    if pathlib.Path(args.output_dir).exists():
        for file in output_dir.iterdir():
            if file.is_file():
                file.unlink()
    else:
        pathlib.Path(args.output_dir).mkdir

    agents[args.role](config, output_dir)

    if args.apply:
        logging.info("Applying changes...")
        for source in map(pathlib.Path, config["sources"]):
            new_source = output_dir / source

            # use diff to generate patch
            patch = pathlib.Path(f"{source}.patch")
            diff = f"diff -u {source} {new_source} > {patch}"
            logging.info(f"Generating patch {patch}...")
            logging.info(diff)
            os.system(diff)

            # apply patch
            apply_patch = f"patch {source} < {patch}"
            logging.info(f"Applying patch {patch}...")
            logging.info(apply_patch)
            os.system(apply_patch)
